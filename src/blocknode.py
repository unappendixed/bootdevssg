import re
from functools import reduce

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_ul = "unordered_list"
block_type_ol = "ordered_list"


class BlockNode:
    def __init__(
        self,
        inner_text: str,
        block_type: str,
        heading_level: int | None = None,
    ):
        self.inner_text = inner_text.strip()
        self.block_type = block_type
        self.heading_level = heading_level

    def __repr__(self) -> str:
        return f"TextBlock({self.inner_text}, {self.block_type})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BlockNode):
            return False

        if other.inner_text == self.inner_text and other.block_type == self.block_type:
            return True

        return False


def str_to_block(input: str) -> BlockNode:
    lines = input.splitlines()

    # Code blocks
    if lines[0].startswith("```") and lines[-1].endswith("```"):
        lines[0] = lines[0].replace("```", "")
        lines[-1] = lines[-1].replace("```", "")
        return BlockNode("\n".join(lines), block_type_code)

    # Quote blocks
    if all([x.startswith("> ") for x in lines]):
        # stripped = re.sub(r"^> ", "", input, 1)
        stripped = "\n".join([re.sub(r"^> ", "", x) for x in lines])
        return BlockNode(stripped, block_type_quote)

    # Headings
    if lines[0].startswith("#"):
        count = len(re.findall(r"^#{0,8}", lines[0])[0])
        stripped = re.sub(r"^#* ", "", input)
        return BlockNode(stripped, block_type_heading, count)

    # Unordered Lists
    if input.startswith("- ") or input.startswith("* "):
        input = input[2:]
        stripped = input.split("\n- ")
        stripped = reduce(list.__add__, [x.split("\n* ") for x in stripped])
        stripped = [x.replace("\n", " ") for x in stripped]
        return BlockNode("\n".join(stripped), block_type_ul)

    # Ordered Lists
    if re.match(r"^[0-9]+\. .*", input) is not None:
        input = re.sub(r"(^|\n)[0-9]+\. ", "\n__", input)
        stripped = input.split("\n__")
        stripped = [x.replace("\n", " ") for x in stripped]
        return BlockNode("\n".join(stripped), block_type_ol)

    # Paragraph
    return BlockNode(input, block_type_paragraph)
