import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "p", None, None, {"href": "http://google.com", "type": "password"}
        )
        expected = 'href="http://google.com" type="password"'
        self.assertEqual(node.props_to_html(), expected)

    def test_repr(self):
        child = HTMLNode(
            "img", None, None, {"src": "https://images.fun/big_richard.png"}
        )
        node = HTMLNode(
            "p",
            "Something funny",
            [child],
            {"href": "http://google.com", "type": "password"},
        )
        expected = 'HTMLNode(p, Something funny, [HTMLNode(img, None, None, src="https://images.fun/big_richard.png")], href="http://google.com" type="password")'
        self.assertEqual(node.__repr__(), expected)
