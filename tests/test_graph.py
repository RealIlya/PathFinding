import unittest

from Graph import Graph


class GraphShortestPathTests(unittest.TestCase):
    def test_finds_shortest_path_with_negative_edge(self):
        graph = Graph(4)
        graph.add_edge(0, 1, 5)
        graph.add_edge(0, 2, 2)
        graph.add_edge(2, 1, -1)
        graph.add_edge(1, 3, 2)
        graph.add_edge(2, 3, 8)

        self.assertEqual(graph.find_shortest_path(0, 3), ([0, 2, 1, 3], 3))

    def test_reports_unreachable_destination(self):
        graph = Graph(3)
        graph.add_edge(0, 1, 4)

        self.assertEqual(graph.find_shortest_path(0, 2), ([], float("inf")))

    def test_reports_reachable_negative_cycle(self):
        graph = Graph(3)
        graph.add_edge(0, 1, 1)
        graph.add_edge(1, 2, -2)
        graph.add_edge(2, 1, 1)

        self.assertEqual(graph.find_shortest_path(0, 2), (None, None))

    def test_reports_negative_cycle_when_source_is_destination(self):
        graph = Graph(3)
        graph.add_edge(0, 1, 1)
        graph.add_edge(1, 2, -2)
        graph.add_edge(2, 1, 1)

        self.assertEqual(graph.find_shortest_path(0, 0), (None, None))

    def test_path_from_vertex_to_itself_uses_that_vertex(self):
        graph = Graph(4)

        self.assertEqual(graph.find_shortest_path(2, 2), ([2], 0))

    def test_rejects_negative_vertex_index(self):
        graph = Graph(3)

        with self.assertRaises(ValueError):
            graph.find_shortest_path(-1, 1)

    def test_rejects_vertex_index_outside_graph(self):
        graph = Graph(3)

        with self.assertRaises(ValueError):
            graph.find_shortest_path(0, 3)


if __name__ == "__main__":
    unittest.main()
