from math import sqrt

# --------------------------------------------------------- #
#                                                           #
#                   Useful Datatypes                        #
#                                                           #
# --------------------------------------------------------- #


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def set_coords(self, x, y):
        self.x = x
        self.y = y

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y


class BoundingBox:
    def __init__(self, point1: Point, point2: Point):
        self.min = point1
        self.max = point2


class Arc:
    def __init__(self, point, prev_arc=None, next_arc=None):
        self.point = point
        self.prev = prev_arc
        self.next = next_arc
        self.event = None
        self.edge1 = None
        self.edge2 = None


class Event:
    def __init__(self, x, point: Point, arc: Arc, is_site: bool):
        self.is_site = is_site
        self.x = x
        self.point = point
        self.arc = arc
        self.valid = True


class Edge:
    def __init__(self, point: Point):
        self.start = point
        self.end = None
        self.done = False

    def complete(self, point: Point):
        if self.done:
            return
        self.end = point
        self.done = True

# --------------------------------------------------------- #
#                                                           #
#                   Utility Functions                       #
#                                                           #
# --------------------------------------------------------- #


def intersect(point: Point, arc: Arc):
    """
    Checks if a new parabola with focus point intersects with an existing parabola arc

    :param point: Focus of new parabola
    :param arc: Existing parabola
    :return: Intersection with arc or None if no intersection
    """
    if arc is None or arc.point.x == point.x:
        return False, None
    a = 0.0
    b = 0.0
    if arc.prev is not None:
        a = (intersection(arc.prev.point, arc.point, 1.0 * point.x)).y
    if arc.next is not None:
        b = (intersection(arc.point, arc.next.point, 1.0 * point.x)).y
    if (arc.prev is None or a <= point.y) and (arc.next is None or point.y <= b):
        px = 1.0 * (arc.point.x ** 2 + (arc.point.y - point.y) ** 2 - point.x ** 2) / (2 * arc.point.x - 2 * point.x)
        return True, Point(px, point.y)
    return False, None


def intersection(point1, point2, dist):
    """
    Finds intersection between two parabolic arcs.

    :param point1: First Focus
    :param point2: Second Focus
    :param dist: Distance x
    :return: Point of intersection or None if no intersection
    """
    p = point1
    if point1.x == point2.x:
        py = (point1.y + point2.y) / 2.0
    elif point2.x == dist:
        py = point2.y
    elif point1.x == dist:
        py = point1.y
        p = point2
    else:
        # use quadratic formula
        z0 = 2.0 * (point1.x - dist)
        z1 = 2.0 * (point2.x - dist)

        a = 1.0 / z0 - 1.0 / z1
        b = -2.0 * (point1.y / z0 - point2.y / z1)
        c = 1.0 * (point1.y ** 2 + point1.x ** 2 - dist ** 2) / z0 - 1.0 * (point2.y ** 2 + point2.x ** 2 - dist ** 2) / z1

        py = 1.0 * (-b - sqrt(b * b - 4 * a * c)) / (2 * a)

    px = 1.0 * (p.x ** 2 + (p.y - py) ** 2 - dist ** 2) / (2 * p.x - 2 * dist)
    res = Point(px, py)
    return res


def circle(a, b, c):
    """
    CCW and finding center of circle defined by three points

    :param a: First point
    :param b: Second point
    :param c: Third point
    :return: Bool for degenerate cases, CCW, and center of circle
    """
    if ((b.x - a.x) * (c.y - a.y) - (c.x - a.x) * (b.y - a.y)) > 0:
        return False, None, None

    # Algorithm from O'Rourke 2ed p. 189
    A = b.x - a.x
    B = b.y - a.y
    C = c.x - a.x
    D = c.y - a.y
    E = A * (a.x + b.x) + B * (a.y + b.y)
    F = C * (a.x + c.x) + D * (a.y + c.y)
    G = 2 * (A * (c.y - b.y) - B * (c.x - b.x))

    if G == 0:
        return False, None, None  # Points are co-linear

    # point o is the center of the circle
    ox = 1.0 * (D * E - B * F) / G
    oy = 1.0 * (A * F - C * E) / G

    # o.x plus radius equals max x coord
    x = ox + sqrt((a.x - ox) ** 2 + (a.y - oy) ** 2)
    o = Point(ox, oy)

    return True, x, o
