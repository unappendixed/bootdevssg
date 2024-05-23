from blocknode import BlockNode
from parentnode import ParentNode
from leafnode import LeafNode
from inlinetextconv import text_to_textnodes

def block_to_html_code(block_node: BlockNode) -> ParentNode:
    raise NotImplemented

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
