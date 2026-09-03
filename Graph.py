class Graph:
    def __init__(self, vertices):
        self.n = vertices

        self.edges = []

    def add_edge(self, a, b, weight):
        self.edges.append([a, b, weight])

    def find_shortest_path(self, source, destination):
        if not 0 <= source < self.n or not 0 <= destination < self.n:
            raise ValueError("Source and destination must be existing vertex indexes")

        distance = [float("inf")] * self.n
        predecessor = [None] * self.n
        distance[source] = 0

        for _ in range(self.n - 1):
            changed = False
            for a, b, weight in self.edges:
                if distance[a] != float("inf") and distance[a] + weight < distance[b]:
                    distance[b] = distance[a] + weight
                    predecessor[b] = a
                    changed = True

            if not changed:
                break

        for a, b, weight in self.edges:
            if distance[a] != float("inf") and distance[a] + weight < distance[b]:
                return None, None

        if distance[destination] == float("inf"):
            return [], distance[destination]

        path = []
        current = destination
        while current is not None:
            path.append(current)
            current = predecessor[current]

        return path[::-1], distance[destination]
