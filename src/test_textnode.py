import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_eq_with_none_url(self):
        node = TextNode("Text 123", "bold", None)
        node2 = TextNode("Text 123", "bold", None)
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("Seventeenth of Juuuuuuly", "italic", "http://google.com")
        expected = "TextNode(Seventeenth of Juuuuuuly, italic, http://google.com)"
        self.assertEqual(node.__repr__(), expected)


if __name__ == "__main__":
    unittest.main()
