import math
import cv2
import numpy as np

class Graph:
    def __init__(self, base_img):
        self._base_img = base_img
        self._nodes = set()
        self._positions = dict()
        self._colors = dict()
        self.front_seats = set()

    def add_node(self, new_node, position, fill=(0, 0, 255), stroke=(0, 0, 0), accent=False, front_seat=False):
        self._nodes.add(new_node)
        self._positions[new_node] = position
        self._colors[new_node] = (fill, stroke, accent)
        if front_seat:
            self.front_seats.add(new_node)

    def set_color(self, node, fill, stroke, accent=False):
        self._colors[node] = (fill, stroke, accent)

    def get_nodes(self):
        return self._nodes.copy()

    def get_weight(self, node_a, node_b):
        p0 = self._positions[node_a]
        p1 = self._positions[node_b]
        return math.sqrt((p0[0] - p1[0]) ** 2 + (p0[1] - p1[1]) ** 2)

    def get_direction_vector(self, node_a, node_b):
        p0 = self._positions[node_a]
        p1 = self._positions[node_b]
        return p0[0] - p1[0], p0[1] - p1[1]

    def show_graph(self):
        cv2.imshow("Result", self.get_graph_image())
        cv2.waitKey(0)

    def get_graph_image(self):
        img = cv2.imread(self._base_img)
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        for node in self._nodes:
            position = self._positions[node]
            fill = self._colors[node][0]
            stroke = self._colors[node][1]
            accent = self._colors[node][2]

            if fill is not None:
                img_hsv = cv2.circle(img_hsv, position, 20, fill, -1)

            if stroke is not None:
                img_hsv = cv2.circle(img_hsv, position, 20, stroke, 3)

            if accent:
                img_hsv = cv2.circle(img_hsv, position, 5, (0, 0, 0), -1)

        img = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)
        img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return img

def init_rouge_wave_graph(image_file):
    graph = Graph(image_file)
    row = 60
    row_increment = 95

    graph.add_node("H1", (row, 86))
    graph.add_node("H2", (row, 146))
    graph.add_node("H3", (row, 206))
    graph.add_node("H4", (row, 352))
    graph.add_node("H5", (row, 412))
    graph.add_node("H6", (row, 472))

    row += row_increment
    graph.add_node("G1", (row, 86))
    graph.add_node("G2", (row, 146))
    graph.add_node("G3", (row, 206))
    graph.add_node("G4", (row, 352))
    graph.add_node("G5", (row, 412))
    graph.add_node("G6", (row, 472))

    row += row_increment
    graph.add_node("F1", (row, 86))
    graph.add_node("F2", (row, 146))
    graph.add_node("F3", (row, 206))
    graph.add_node("F4", (row, 352))
    graph.add_node("F5", (row, 412))
    graph.add_node("F6", (row, 472))

    row += row_increment
    graph.add_node("E1", (row, 86))
    graph.add_node("E2", (row, 146))
    graph.add_node("E3", (row, 206))
    graph.add_node("E4", (row, 352))
    graph.add_node("E5", (row, 412))
    graph.add_node("E6", (row, 472))

    row += row_increment
    graph.add_node("D1", (row, 86))
    graph.add_node("D2", (row, 146))
    graph.add_node("D3", (row, 206))
    graph.add_node("D4", (row, 352))
    graph.add_node("D5", (row, 412))
    graph.add_node("D6", (row, 472))

    row += row_increment
    graph.add_node("C1", (row, 86))
    graph.add_node("C2", (row, 146))
    graph.add_node("C3", (row, 206))
    graph.add_node("C4", (row, 352))
    graph.add_node("C5", (row, 412))
    graph.add_node("C6", (row, 472))

    row += row_increment
    graph.add_node("B1", (row, 146), front_seat=True)
    graph.add_node("B2", (row, 206), front_seat=True)
    graph.add_node("B3", (row, 352), front_seat=True)
    graph.add_node("B4", (row, 412), front_seat=True)

    row += row_increment
    graph.add_node("A1", (row, 146), front_seat=True)
    graph.add_node("A2", (row, 206), front_seat=True)
    graph.add_node("A3", (row, 352), front_seat=True)
    graph.add_node("A4", (row, 412), front_seat=True)

    return graph


def init_gale_force_graph(image_file):
    graph = Graph(image_file)
    row = 60
    row_increment = 95

    graph.add_node("H1", (row, 86))
    graph.add_node("H2", (row, 146))
    graph.add_node("H3", (row, 206))
    graph.add_node("H4", (row, 352))
    graph.add_node("H5", (row, 412))
    graph.add_node("H6", (row, 472))

    row += row_increment
    graph.add_node("G1", (row, 86))
    graph.add_node("G2", (row, 146))
    graph.add_node("G3", (row, 206))
    graph.add_node("G4", (row, 352))
    graph.add_node("G5", (row, 412))
    graph.add_node("G6", (row, 472))

    row += row_increment
    graph.add_node("F1", (row, 86))
    graph.add_node("F2", (row, 146))
    graph.add_node("F3", (row, 206))
    graph.add_node("F4", (row, 352))
    graph.add_node("F5", (row, 412))
    graph.add_node("F6", (row, 472))

    row += row_increment
    graph.add_node("E1", (row, 86))
    graph.add_node("E2", (row, 146))
    graph.add_node("E3", (row, 206))
    graph.add_node("E4", (row, 352))
    graph.add_node("E5", (row, 412))
    graph.add_node("E6", (row, 472))

    row += row_increment
    graph.add_node("D1", (row, 86))
    graph.add_node("D2", (row, 146))
    graph.add_node("D3", (row, 206))
    graph.add_node("D4", (row, 352))
    graph.add_node("D5", (row, 412))
    graph.add_node("D6", (row, 472))

    row += row_increment
    graph.add_node("C1", (row, 86))
    graph.add_node("C2", (row, 146))
    graph.add_node("C3", (row, 206))
    graph.add_node("C4", (row, 352))
    graph.add_node("C5", (row, 412))
    graph.add_node("C6", (row, 472))

    row += row_increment
    graph.add_node("B1", (row, 146), front_seat=True)
    graph.add_node("B2", (row, 206), front_seat=True)
    graph.add_node("B3", (row, 352), front_seat=True)
    graph.add_node("B4", (row, 412), front_seat=True)

    row += row_increment
    graph.add_node("A1", (row, 146), front_seat=True)
    graph.add_node("A2", (row, 206), front_seat=True)
    graph.add_node("A3", (row, 352), front_seat=True)
    graph.add_node("A4", (row, 412), front_seat=True)

    return graph


def init_island_girl_graph(image_file):
    graph = Graph(image_file)
    row = 188
    row_increment = 98

    graph.add_node("E1", (row, 150))
    graph.add_node("E2", (row, 210))
    graph.add_node("E3", (row, 355))
    graph.add_node("E4", (row, 415))

    row += row_increment
    graph.add_node("D1", (row, 150))
    graph.add_node("D2", (row, 210))
    graph.add_node("D3", (row, 355))
    graph.add_node("D4", (row, 415))

    row += row_increment
    graph.add_node("C1", (row, 150))
    graph.add_node("C2", (row, 210))
    graph.add_node("C3", (row, 355))
    graph.add_node("C4", (row, 415))

    row += row_increment
    graph.add_node("B1", (row, 150))
    graph.add_node("B2", (row, 210))
    graph.add_node("B3", (row, 355))
    graph.add_node("B4", (row, 415))

    row += row_increment
    graph.add_node("A1", (row, 150), front_seat=True)
    graph.add_node("A2", (row, 210), front_seat=True)
    graph.add_node("A3", (row, 355), front_seat=True)
    graph.add_node("A4", (row, 415), front_seat=True)

    return graph
