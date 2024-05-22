from leafnode import LeafNode
import unittest

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("a", "this is a link", {"href": "https://google.com"})
        expected = "<a href=\"https://google.com\">this is a link</a>"
        self.assertEqual(node.to_html(), expected)
