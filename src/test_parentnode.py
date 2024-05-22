import unittest
from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            "div",
            [
                LeafNode("p", "paragraph one"),
                LeafNode("p", "paragraph two"),
                LeafNode("p", "paragraph three"),
            ],
        )
        expected = """<div><p>paragraph one</p><p>paragraph two</p><p>paragraph three</p></div>"""
        self.assertEqual(node.to_html(), expected)
