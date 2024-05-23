from blocknode import BlockNode, block_type_code
from parentnode import ParentNode
from inlinetextconv import text_to_textnodes, text_node_to_html_node


def block_to_html_code(block_node: BlockNode) -> ParentNode:
    if block_node.block_type != block_type_code:
        raise ValueError(
            f"cannot convert block of type {block_node.block_type} to code"
        )
    children = text_to_textnodes(block_node.inner_text)
    children = [text_node_to_html_node(x) for x in children]
    inner_wrap = ParentNode("code", children)
    outer_wrap = ParentNode("pre", [inner_wrap])
    return outer_wrap


def block_to_html_quote(block_node: BlockNode) -> ParentNode:
    raise NotImplemented


def block_to_html_heading(block_node: BlockNode) -> ParentNode:
    raise NotImplemented


def block_to_html_ul(block_node: BlockNode) -> ParentNode:
    raise NotImplemented


def block_to_html_ol(block_node: BlockNode) -> ParentNode:
    raise NotImplemented


def block_to_html_paragraph(block_node: BlockNode) -> ParentNode:
    raise NotImplemented
