import unittest
from blocknode import BlockNode
from leafnode import LeafNode
from parentnode import ParentNode
from blocktextconv import *


class TestBlockConv(unittest.TestCase):
    def test_block_to_html_code(self):
        sut = BlockNode('console.log("Hello world!");\nexit(0)', "code")
        actual = block_to_html_code(sut)
        expected = ParentNode(
            "pre",
            [
                ParentNode(
                    "code",
                    [
                        LeafNode(None, 'console.log("Hello world!");\nexit(0)'),
                    ],
                )
            ],
        )

        self.assertEqual(actual, expected)

    def test_block_to_html_quote(self):
        sut = BlockNode(
            "There are years when weeks happen and weeks when years happen.",
            block_type_quote,
        )
        actual = block_to_html_quote(sut)
        expected = ParentNode(
            "blockquote",
            [
                LeafNode(
                    None,
                    "There are years when weeks happen and weeks when years happen.",
                )
            ],
        )

        self.assertEqual(actual, expected)

    def test_block_to_html_paragraph(self):
        sut = BlockNode(
            "This is just like a normal paragraph of text or whatever.\nDefinitely nothing weird going on here.",
            block_type_paragraph,
        )
        actual = block_to_html_paragraph(sut)
        expected = ParentNode(
            "p",
            [
                LeafNode(
                    None,
                    "This is just like a normal paragraph of text or whatever. Definitely nothing weird going on here.",
                )
            ],
        )

        self.assertEqual(actual, expected)

    def test_block_to_html_ul(self):
        sut = BlockNode(
            "Bread\nButter\nBeer\nLong lost brother",
            block_type_ul,
        )
        actual = block_to_html_ul(sut)
        expected = ParentNode(
            "ul",
            [
                ParentNode("li", [LeafNode(None, "Bread")]),
                ParentNode("li", [LeafNode(None, "Butter")]),
                ParentNode("li", [LeafNode(None, "Beer")]),
                ParentNode("li", [LeafNode(None, "Long lost brother")]),
            ],
        )

        self.assertEqual(actual, expected)


if "unittest.util" in __import__("sys").modules:
    # Show full diff in self.assertEqual.
    __import__("sys").modules["unittest.util"]._MAX_LENGTH = 999999999

if __name__ == "__main__":
    unittest.main()
