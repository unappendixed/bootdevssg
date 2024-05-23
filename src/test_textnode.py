import unittest
from leafnode import LeafNode
from textnode import (
    TextNode,
    extract_markdown_links,
    split_nodes_delimiter,
    text_node_to_html_node,
    extract_markdown_images
)


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

    def test_text_node_to_html_node_italic(self):
        node = TextNode("some text here", "italic")
        expected = LeafNode("i", "some text here")
        self.assertEqual(text_node_to_html_node(node), expected)

    def test_text_node_to_html_node_bold(self):
        node = TextNode("some text here", "bold")
        expected = LeafNode("b", "some text here")
        self.assertEqual(text_node_to_html_node(node), expected)

    def test_text_node_to_html_node_image(self):
        node = TextNode("a beautiful sunrise", "image", "images/sunrise.png")
        expected = LeafNode(
            "img", "", {"src": "images/sunrise.png", "alt": "a beautiful sunrise"}
        )
        self.assertEqual(text_node_to_html_node(node), expected)

    def test_text_node_to_html_node_link(self):
        node = TextNode(
            "click here to purchase", "link", "https://buystuff.store/some-product"
        )
        expected = LeafNode(
            "a",
            "click here to purchase",
            {"href": "https://buystuff.store/some-product"},
        )
        self.assertEqual(text_node_to_html_node(node), expected)

    def test_split_nodes_delimiter_single_bold(self):
        node = TextNode("this **is** a test.", "text")
        expected = [
            TextNode("this ", "text"),
            TextNode("is", "bold"),
            TextNode(" a test.", "text"),
        ]
        self.assertEqual(split_nodes_delimiter([node], "**", "bold"), expected)

    def test_split_nodes_delimiter_single_italic(self):
        node = TextNode("this *is* a test.", "text")
        expected = [
            TextNode("this ", "text"),
            TextNode("is", "italic"),
            TextNode(" a test.", "text"),
        ]

        self.assertEqual(split_nodes_delimiter([node], "*", "italic"), expected)

    def test_split_nodes_delimiter_single_code(self):
        node = TextNode("initialize the value `url` first", "text")
        expected = [
            TextNode("initialize the value ", "text"),
            TextNode("url", "code"),
            TextNode(" first", "text"),
        ]

        self.assertEqual(split_nodes_delimiter([node], "`", "code"), expected)

    def test_split_nodes_delimiter_double_italic(self):
        node = TextNode("this *is* a test with *gusto* for a change.", "text")
        expected = [
            TextNode("this ", "text"),
            TextNode("is", "italic"),
            TextNode(" a test with ", "text"),
            TextNode("gusto", "italic"),
            TextNode(" for a change.", "text"),
        ]

        self.assertEqual(split_nodes_delimiter([node], "*", "italic"), expected)

    def test_extract_markdown_images_single(self):
        text = "This is some ![markdown text](images/snippet.png) with an image."
        expected = [TextNode("markdown text", "image", "images/snippet.png")]
        self.assertEqual(extract_markdown_images(text), expected)
        pass

    def test_extract_markdown_links_single(self):
        text = "Check out this [website](https://links.biz/nice-one) for more."
        expected = [TextNode("website", "link", "https://links.biz/nice-one")]
        self.assertEqual(extract_markdown_links(text), expected)
        pass

if __name__ == "__main__":
    unittest.main()
