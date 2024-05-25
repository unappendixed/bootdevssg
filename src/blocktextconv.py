from blocknode import (
    BlockNode,
    block_type_code,
    block_type_quote,
    block_type_heading,
    block_type_ul,
    block_type_ol,
    block_type_paragraph,
)

from blocknode import str_to_block

from parentnode import ParentNode
from inlinetextconv import text_to_textnodes, text_node_to_html_node
from functools import reduce

from textnode import markdown_to_blocks


class BlockError(ValueError):
    def __init__(self, invalid_block: BlockNode, dest_type: str):
        super().__init__(
            f"Cannot convert block of type {invalid_block.block_type} to {dest_type}"
        )


def process_string_to_list(str):
    return [text_node_to_html_node(x) for x in text_to_textnodes(str)]


def markdown_to_html_node(markdown: str) -> ParentNode:
    block_strings = markdown_to_blocks(markdown)
    blocks = [str_to_block(s) for s in block_strings]
    html_nodes = []
    for block in blocks:
        if block.block_type == block_type_code:
            html_nodes.append(block_to_html_code(block))
        elif block.block_type == block_type_quote:
            html_nodes.append(block_to_html_quote(block))
        elif block.block_type == block_type_heading:
            html_nodes.append(block_to_html_heading(block))
        elif block.block_type == block_type_ul:
            html_nodes.append(block_to_html_ul(block))
        elif block.block_type == block_type_ol:
            html_nodes.append(block_to_html_ol(block))
        elif block.block_type == block_type_paragraph:
            html_nodes.append(block_to_html_paragraph(block))
        else:
            raise ValueError(f"Invalid block_type: {block.block_type}")
    return ParentNode("div", html_nodes)


def block_to_html_code(block: BlockNode) -> ParentNode:
    if block.block_type != block_type_code:
        raise BlockError(block, "code")
    children = process_string_to_list(block.inner_text)
    inner_wrap = ParentNode("code", children)
    outer_wrap = ParentNode("pre", [inner_wrap])
    return outer_wrap


def block_to_html_quote(block: BlockNode) -> ParentNode:
    if block.block_type != block_type_quote:
        raise BlockError(block, "quote")
    children = process_string_to_list(block.inner_text)
    return ParentNode("blockquote", children)


def block_to_html_heading(block: BlockNode) -> ParentNode:
    if block.block_type != block_type_heading:
        raise BlockError(block, "heading")
    elif block.heading_level is None:
        raise ValueError(f"cannot convert block without heading_level to heading")
    children = process_string_to_list(block.inner_text)
    return ParentNode(f"h{block.heading_level}", children)


def block_to_html_ul(block: BlockNode) -> ParentNode:
    if block.block_type != block_type_ul:
        raise BlockError(block, "unordered list")
    children = block.inner_text.split("\n")
    children = reduce(list.__add__, [process_string_to_list(x) for x in children])
    children = [ParentNode("li", [x]) for x in children]
    return ParentNode("ul", children)


def block_to_html_ol(block: BlockNode) -> ParentNode:
    if block.block_type != block_type_ol:
        raise BlockError(block, "ordered list")
    children = block.inner_text.split("\n")
    children = reduce(list.__add__, [process_string_to_list(x) for x in children])
    children = [ParentNode("li", [x]) for x in children]
    return ParentNode("ol", children)


def block_to_html_paragraph(block: BlockNode) -> ParentNode:
    if block.block_type != block_type_paragraph:
        raise BlockError(block, "paragraph")
    children = process_string_to_list(block.inner_text.replace("\n", " "))
    return ParentNode("p", children)
