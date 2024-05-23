import unittest
from leafnode import LeafNode
from textnode import (
    TextNode,
    extract_markdown_links,
    extract_markdown_images,
    split_nodes_delimiter,
    split_nodes_link,
    split_nodes_image,
    text_node_to_html_node,
    text_to_textnodes,
    markdown_to_blocks,
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
        expected = [("markdown text", "images/snippet.png")]
        self.assertEqual(extract_markdown_images(text), expected)
        pass

    def test_extract_markdown_links_single(self):
        text = "Check out this [website](https://links.biz/nice-one) for more."
        expected = [("website", "https://links.biz/nice-one")]
        self.assertEqual(extract_markdown_links(text), expected)
        pass

    def test_split_nodes_image_single(self):
        node = TextNode(
            "Somebody ![once](assets/once-upon-a-time.png) told me.", "text"
        )
        expected = [
            TextNode("Somebody ", "text"),
            TextNode("once", "image", "assets/once-upon-a-time.png"),
            TextNode(" told me.", "text"),
        ]
        self.assertEqual(split_nodes_image([node]), expected)

    def test_split_nodes_image_ending(self):
        node = TextNode(
            "the world was gonna ![roll me](assets/rolling-barrel.png)", "text"
        )
        expected = [
            TextNode("the world was gonna ", "text"),
            TextNode("roll me", "image", "assets/rolling-barrel.png"),
        ]
        self.assertEqual(split_nodes_image([node]), expected)

    def test_split_nodes_image_double(self):
        node = TextNode(
            "![I](assets/eyeball.jpg) ain't the ![sharpest tool](assets/spoon.png) in the ![shed](assets/outhouse.png)",
            "text",
        )
        expected = [
            TextNode("I", "image", "assets/eyeball.jpg"),
            TextNode(" ain't the ", "text"),
            TextNode("sharpest tool", "image", "assets/spoon.png"),
            TextNode(" in the ", "text"),
            TextNode("shed", "image", "assets/outhouse.png"),
        ]
        self.assertEqual(split_nodes_image([node]), expected)

    def test_split_nodes_link_single(self):
        node = TextNode(
            "there is a [house](https://wikipedia.org/House) in New Orleans", "text"
        )
        expected = [
            TextNode("there is a ", "text"),
            TextNode("house", "link", "https://wikipedia.org/House"),
            TextNode(" in New Orleans", "text"),
        ]
        self.assertEqual(split_nodes_link([node]), expected)

    def test_split_nodes_link_ending(self):
        node = TextNode(
            "rats, rats, we are [the rats](https://youtube.com/watch?v=123asdf)", "text"
        )
        expected = [
            TextNode("rats, rats, we are ", "text"),
            TextNode("the rats", "link", "https://youtube.com/watch?v=123asdf"),
        ]
        self.assertEqual(split_nodes_link([node]), expected)

    def test_split_nodes_link_double(self):
        node = TextNode(
            "[celebrating](https://wikipedia.org/Celebration) yet another [birthday bash](https://wikipedia.org/Party)",
            "text",
        )
        expected = [
            TextNode("celebrating", "link", "https://wikipedia.org/Celebration"),
            TextNode(" yet another ", "text"),
            TextNode("birthday bash", "link", "https://wikipedia.org/Party"),
        ]
        self.assertEqual(split_nodes_link([node]), expected)

    def test_text_to_textnodes(self):
        text = "This *is* some **markdown** text. It supports `code`, ![images](assets/image.jpg), and [hyperlinks](https://google.fun)"
        expected = [
            TextNode("This ", "text"),
            TextNode("is", "italic"),
            TextNode(" some ", "text"),
            TextNode("markdown", "bold"),
            TextNode(" text. It supports ", "text"),
            TextNode("code", "code"),
            TextNode(", ", "text"),
            TextNode("images", "image", "assets/image.jpg"),
            TextNode(", and ", "text"),
            TextNode("hyperlinks", "link", "https://google.fun"),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_markdown_to_blocks(self):
        input = """
        This is some very nice markdown text.
        This is part of the same paragraph.

        This is not.
        """
        expected = [
            "This is some very nice markdown text. This is part of the same paragraph.",
            "This is not."
        ]
        self.assertEqual(markdown_to_blocks(input), expected)


if __name__ == "__main__":
    unittest.main()
