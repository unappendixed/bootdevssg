import unittest
from blocknode import BlockNode
from leafnode import LeafNode
from parentnode import ParentNode
from blocktextconv import block_to_html_code


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

if 'unittest.util' in __import__('sys').modules:
    # Show full diff in self.assertEqual.
    __import__('sys').modules['unittest.util']._MAX_LENGTH = 999999999

if __name__ == "__main__":
    unittest.main()
