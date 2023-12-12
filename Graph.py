class Graph:
    def __init__(self, vertices):
        self.n = vertices

        self.edges = []

    def add_edge(self, a, b, weight):
        self.edges.append([a, b, weight])

    def find_shortest_path(self, source, destination):
        distance = [float("inf")] * self.n
        distance[source] = 0

        checked_edges = []

        for _ in range(self.n - 1):
            for a, b, weight in self.edges:
                if distance[a] != float("inf") and distance[a] + weight < distance[b]:
                    checked_edges.append([a, b, weight])
                    distance[b] = distance[a] + weight

        for a, b, weight in self.edges:
            if distance[a] != float("inf") and distance[a] + weight < distance[b]:
                return None, None

        start_index = 0
        buffer = 0
        for i, e in enumerate(checked_edges[::-1]):
            if e[1] == destination:
                start_index = i
                buffer = destination
                break

        passed_vertices = [buffer]

        for i in range(len(checked_edges) - start_index - 1, -1, -1):
            if checked_edges[i][1] == buffer:
                buffer = checked_edges[i][0]
                passed_vertices.append(buffer)

        return passed_vertices[::-1], distance[destination]
