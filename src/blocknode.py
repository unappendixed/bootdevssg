from textnode import TextNode
import re

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_ul = "unordered_list"
block_type_ol = "ordered_list"


class BlockNode:
    def __init__(
        self,
        text_nodes: list[TextNode],
        block_type: str,
        heading_level: int | None = None,
    ):
        self.text_nodes = [x for x in text_nodes if x.text != ""]
        self.block_type = block_type
        self.heading_level = heading_level

    def __repr__(self) -> str:
        return f"TextBlock({self.text_nodes}, {self.block_type})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BlockNode):
            return False

        if other.text_nodes == self.text_nodes and other.block_type == self.block_type:
            return True

        return False


def str_to_block(input: str) -> BlockNode:
    lines = input.splitlines()

    # Code blocks
    if lines[0].startswith("```") and lines[-1].endswith("```"):
        lines[0] = lines[0].replace("```", "")
        lines[-1] = lines[-1].replace("```", "")
        return BlockNode([TextNode("\n".join(lines), "text")], block_type_code)

    # Quote blocks
    if all([x.startswith("> ") for x in lines]):
        # stripped = re.sub(r"^> ", "", input, 1)
        stripped = "\n".join([re.sub(r"^> ", "", x) for x in lines])
        return BlockNode([TextNode(stripped, "text")], block_type_quote)

    # Headings
    if lines[0].startswith("#"):
        count = len(re.findall(r"^#{0,8}", lines[0])[0])
        stripped = re.sub(r"^#* ", "", input)
        return BlockNode([TextNode(stripped, "text")], block_type_heading, count)

    # Unordered Lists
    if all([x.startswith("*") or x.startswith("-") for x in lines]):
        # stripped = re.sub(r"^[\*\-]+ ", "", input, 1)
        stripped = [re.sub(r"^[\*\-] ", "", x) for x in lines]
        stripped = [TextNode(x, "text") for x in stripped]
        return BlockNode(stripped, block_type_ul)

    # Ordered Lists
    if all([(re.match(r"^[0-9]+\. .+", x) is not None) for x in lines]):
        stripped = [re.sub(r"^[0-9]+. ", "", x, 1) for x in lines]
        stripped = [TextNode(x, "text") for x in stripped]
        return BlockNode(stripped, block_type_ol)

    # Paragraph
    return BlockNode([TextNode(input, "text")], block_type_paragraph)
