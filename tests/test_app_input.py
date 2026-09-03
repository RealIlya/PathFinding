import unittest

import App


class VertexPairInputTests(unittest.TestCase):
    def test_parses_two_existing_vertex_indexes(self):
        self.assertEqual(App.parse_vertex_pair("0 2", 3), (0, 2))

    def test_rejects_malformed_input(self):
        invalid_values = (None, "", "1", "0 1 2", "first second")

        for value in invalid_values:
            with self.subTest(value=value):
                self.assertIsNone(App.parse_vertex_pair(value, 3))

    def test_rejects_vertex_indexes_outside_graph(self):
        for value in ("-1 1", "0 3"):
            with self.subTest(value=value):
                self.assertIsNone(App.parse_vertex_pair(value, 3))


if __name__ == "__main__":
    unittest.main()
