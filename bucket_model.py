import graph


class Bucket:
    def __init__(self, row, is_front):
        self.size = 0
        self.is_front = is_front
        self.row = row
        self.nodes = list()

    def __lt__(self, other):
        return self.row < other.row

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other):
        return self.row > other.row

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    def __eq__(self, other):
        return self.row == other.row

    def __ne__(self, other):
        return self.row != other.row

    def add_seat(self, node):
        self.nodes.append(node)
        self.size += 1


class BucketModel(graph.Graph):

    def __init__(self, base_img):
        super().__init__(base_img)
        self._port_buckets = list()
        self._stbd_buckets = list()

    def get_bucket_lists(self):
        self._port_buckets.sort()
        self._stbd_buckets.sort()
        return tuple(self._port_buckets), tuple(self._stbd_buckets)

    def add_node(self, new_node, position, fill=(0, 0, 255), stroke=(0, 0, 0), accent=False, front_seat=False,
                 row=0, is_port=False, ):
        super().add_node(new_node, position, fill=fill, stroke=stroke, accent=accent, front_seat=front_seat)

        found_row = False
        if is_port:
            for bucket in self._port_buckets:
                if bucket.row == row:
                    bucket.add_seat(new_node)
                    found_row = True
                    break

            if not found_row:
                new_bucket = Bucket(row, front_seat)
                new_bucket.add_seat(new_node)
                self._port_buckets.append(new_bucket)

        else:
            for bucket in self._stbd_buckets:
                if bucket.row == row:
                    bucket.nodes.append(new_node)
                    found_row = True
                    break

            if not found_row:
                new_bucket = Bucket(row, front_seat)
                new_bucket.add_seat(new_node)
                self._stbd_buckets.append(new_bucket)

        self._port_buckets.sort()
        self._stbd_buckets.sort()


def init_rouge_wave_graph(image_file):
    buckets = BucketModel(image_file)
    row = 60
    row_increment = 95

    buckets.add_node("H1", (row, 86),  row=8, is_port=True)
    buckets.add_node("H2", (row, 146), row=8, is_port=True)
    buckets.add_node("H3", (row, 206), row=8, is_port=True)
    buckets.add_node("H4", (row, 352), row=8, is_port=False)
    buckets.add_node("H5", (row, 412), row=8, is_port=False)
    buckets.add_node("H6", (row, 472), row=8, is_port=False)

    row += row_increment
    buckets.add_node("G1", (row, 86),  row=7, is_port=True)
    buckets.add_node("G2", (row, 146), row=7, is_port=True)
    buckets.add_node("G3", (row, 206), row=7, is_port=True)
    buckets.add_node("G4", (row, 352), row=7, is_port=False)
    buckets.add_node("G5", (row, 412), row=7, is_port=False)
    buckets.add_node("G6", (row, 472), row=7, is_port=False)

    row += row_increment
    buckets.add_node("F1", (row, 86),  row=6, is_port=True)
    buckets.add_node("F2", (row, 146), row=6, is_port=True)
    buckets.add_node("F3", (row, 206), row=6, is_port=True)
    buckets.add_node("F4", (row, 352), row=6, is_port=False)
    buckets.add_node("F5", (row, 412), row=6, is_port=False)
    buckets.add_node("F6", (row, 472), row=6, is_port=False)

    row += row_increment
    buckets.add_node("E1", (row, 86),  row=5, is_port=True)
    buckets.add_node("E2", (row, 146), row=5, is_port=True)
    buckets.add_node("E3", (row, 206), row=5, is_port=True)
    buckets.add_node("E4", (row, 352), row=5, is_port=False)
    buckets.add_node("E5", (row, 412), row=5, is_port=False)
    buckets.add_node("E6", (row, 472), row=5, is_port=False)

    row += row_increment
    buckets.add_node("D1", (row, 86),  row=4, is_port=True)
    buckets.add_node("D2", (row, 146), row=4, is_port=True)
    buckets.add_node("D3", (row, 206), row=4, is_port=True)
    buckets.add_node("D4", (row, 352), row=4, is_port=False)
    buckets.add_node("D5", (row, 412), row=4, is_port=False)
    buckets.add_node("D6", (row, 472), row=4, is_port=False)

    row += row_increment
    buckets.add_node("C1", (row, 86),  row=3, is_port=True)
    buckets.add_node("C2", (row, 146), row=3, is_port=True)
    buckets.add_node("C4", (row, 352), row=3, is_port=False)
    buckets.add_node("C5", (row, 412), row=3, is_port=False)
    buckets.add_node("C6", (row, 472), row=3, is_port=False)

    row += row_increment
    buckets.add_node("B1", (row, 146), row=2, is_port=True,  front_seat=True)
    buckets.add_node("B2", (row, 206), row=2, is_port=True,  front_seat=True)
    buckets.add_node("B3", (row, 352), row=2, is_port=False,  front_seat=True)
    buckets.add_node("B4", (row, 412), row=2, is_port=False,  front_seat=True)

    row += row_increment
    buckets.add_node("A1", (row, 146), row=1, is_port=True, front_seat=True)
    buckets.add_node("A2", (row, 206), row=1, is_port=True, front_seat=True)
    buckets.add_node("A3", (row, 352), row=1, is_port=False, front_seat=True)
    buckets.add_node("A4", (row, 412), row=1, is_port=False, front_seat=True)

    return buckets


