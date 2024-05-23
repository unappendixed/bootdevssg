import unittest
from blocknode import *
from inlinetextconv import markdown_to_blocks


class TestBlockNode(unittest.TestCase):
    def test_str_to_block_paragraph(self):
        text = "This is a regular markdown paragraph.\nIt spans multiple  lines."
        actual = str_to_block(text)
        expected = BlockNode(text, block_type_paragraph)
        self.assertEqual(actual, expected)

    def test_str_to_block_heading(self):
        text = markdown_to_blocks("## Overview")[0]
        actual = str_to_block(text)
        expected = BlockNode("Overview", block_type_heading, 2)

        self.assertEqual(actual, expected)

    def test_str_to_block_code(self):
        text = """
        ```
        console.log("Hello world!");
        ```
        """.strip()

        actual = str_to_block(text)
        expected = BlockNode('console.log("Hello world!");', block_type_code)

        self.assertEqual(actual, expected)

    def test_str_to_block_quote(self):
        text = markdown_to_blocks(
            "> So it goes,\n> Or the way that I was told,\n> There was a king"
        )[0]
        actual = str_to_block(text)
        expected = BlockNode(
            "So it goes,\nOr the way that I was told,\nThere was a king",
            block_type_quote,
        )

        self.assertEqual(actual, expected)

    def test_str_to_block_ol(self):
        text = markdown_to_blocks(
            """
        1. Don't pick up the phone.
        2. Don't let him in.
        3. If you're under him, you're not getting over him.
        """
        )[0]
        actual = str_to_block(text)
        expected = BlockNode(
            "Don't pick up the phone.\nDon't let him in.\nIf you're under him, you're not getting over him.",
            block_type_ol,
        )
        self.assertEqual(actual, expected)

    def test_str_to_block_ul(self):
        text = markdown_to_blocks("""* Eggs\n* Butter\n* Beer\n* Long lost brother""")
        actual = str_to_block(text[0])
        expected = BlockNode(
            "Eggs\nButter\nBeer\nLong lost brother",
            block_type_ul,
        )

        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
