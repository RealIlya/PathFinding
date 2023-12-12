class Vertex:

    def __init__(self, tag):
        # pointN, N - point number
        self.tag = tag

    def __eq__(self, vertex: object) -> bool:
        if self.tag == vertex.tag:
            return True

        return False

    def get_number(self):
        return int(''.join(s for s in self.tag if s.isdigit()))
