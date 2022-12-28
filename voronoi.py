# Inspired by https://www.cs.hmc.edu/~mbrubeck/voronoi.html
from queue import PriorityQueue

from utils import *


class Voronoi:
    def __init__(self, sites):
        # self.event_queue = CustomPriorityQueue()  # Priority queue of events
        self.event_queue = PriorityQueue()
        self.beach_line = None  # root of binary tree of parabolic arcs
        self.output = []

        # bounding box
        x1 = 0.0
        x2 = 0.0
        y1 = 0.0
        y2 = 0.0

        # insert points to site event
        for site in sites:
            event = Event(site.x, site, None, True)
            self.event_queue.put((event.x, event))
            # keep track of bounding box size
            if site.x < x1:
                x1 = site.x
            if site.y < y1:
                y1 = site.y
            if site.x > x2:
                x2 = site.x
            if site.y > y2:
                y2 = site.y

        # add margins to the bounding box
        dx = (x2 - x1 + 1) / 5.0
        dy = (y2 - y1 + 1) / 5.0
        x1 = x1 - dx
        x2 = x2 + dx
        y1 = y1 - dy
        y2 = y2 + dy

        self.bbox = BoundingBox(Point(x1, y1), Point(x2, y2))

    def compute(self):
        while not self.event_queue.empty():
            next_event = self.event_queue.get()[1]
            if next_event.is_site:
                self.handle_site(next_event.point)
            else:
                self.handle_event(next_event)
        self.complete_edges()

    def handle_site(self, point):
        self.insert_arc(point)

    def handle_event(self, event):
        if event.valid:
            # start new edge
            edge = Edge(event.point)
            self.output.append(edge)

            # remove associated arc (parabola)
            arc = event.arc
            if arc.prev is not None:
                arc.prev.next = arc.next
                arc.prev.edge2 = edge
            if arc.next is not None:
                arc.next.prev = arc.prev
                arc.next.edge1 = edge

            # finish the edges before and after a
            if arc.edge1 is not None:
                arc.edge1.complete(event.point)
            if arc.edge2 is not None:
                arc.edge2.complete(event.point)

            # recheck circle events on either side of p
            if arc.prev is not None:
                self.check_circle_event(arc.prev)
            if arc.next is not None:
                self.check_circle_event(arc.next)

    def insert_arc(self, point: Point):
        if self.beach_line is None:
            self.beach_line = Arc(point)
        else:
            arc = self.beach_line
            while arc is not None:
                flag, z = intersect(point, arc)
                if flag:
                    flag, zz = intersect(point, arc.next)
                    if arc.next is not None and not flag:
                        arc.next.prev = Arc(arc.point, arc, arc.next)
                        arc.next = arc.next.prev
                    else:
                        arc.next = Arc(arc.point, arc)
                    arc.next.edge2 = arc.edge2
                    arc.next.prev = Arc(point, arc, arc.next)
                    arc.next = arc.next.prev
                    arc = arc.next

                    edge1 = Edge(z)
                    self.output.append(edge1)
                    arc.prev.edge2 = arc.edge1 = edge1

                    edge2 = Edge(z)
                    self.output.append(edge2)
                    arc.next.edge1 = arc.edge2 = edge2

                    self.check_circle_event(arc)
                    self.check_circle_event(arc.prev)
                    self.check_circle_event(arc.next)
                    return
                arc = arc.next
            arc = self.beach_line
            while arc.next is not None:
                arc = arc.next
            arc.next = Arc(point, arc)
            start = Point(self.bbox.min.x, (arc.next.point.y + arc.point.y) / 2.0)

            edge = Edge(start)
            arc.edge2 = arc.next.edge1 = edge
            self.output.append(edge)

    def check_circle_event(self, arc: Arc):
        if arc.event is not None and arc.event.x != self.bbox.min.x:
            arc.event.valid = False
        arc.event = None
        if arc.prev is None or arc.next is None:
            return
        flag, x, center = circle(arc.prev.point, arc.point, arc.next.point)
        if flag and x > self.bbox.min.x:
            arc.event = Event(x, center, arc, False)
            self.event_queue.put((arc.event.x, arc.event))

    def complete_edges(self):
        dist = self.bbox.max.x + (self.bbox.max.x - self.bbox.min.x) + (self.bbox.max.y - self.bbox.min.y)
        arc = self.beach_line
        while arc.next is not None:
            if arc.edge2 is not None:
                point = intersection(arc.point, arc.next.point, dist * 2.0)
                arc.edge2.complete(point)
            arc = arc.next

    def print_output(self):
        for edge in self.output:
            point1 = edge.start
            point2 = edge.end
            print(point1.x, point1.y, point2.x, point2.y)

    def get_output(self):
        output = []
        for edge in self.output:
            point1 = edge.start
            point2 = edge.end
            output.append((point1.x, point1.y, point2.x, point2.y))
        return output
