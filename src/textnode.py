# from typing import Optional
from htmlnode import HTMLNode
from leafnode import LeafNode
import re


class TextNode:
    def __init__(self, text: str, text_type: str, url: str | None = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value):
        return (
            value.text == self.text
            and value.text_type == self.text_type
            and value.url == self.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: str
) -> list[TextNode]:
    output_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != "text":
            continue
        parts = node.text.split(delimiter)
        if len(parts) == 1:
            # doesn't contain delim
            continue
        if len(parts) % 2 == 0:
            raise ValueError("invalid markdown")

        for i, p in enumerate(parts):
            if i % 2 == 1:
                output_nodes.append(TextNode(p, text_type))
            else:
                output_nodes.append(TextNode(p, "text"))
    return output_nodes


def extract_markdown_images(text: str) -> list[TextNode]:
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches: list[tuple[str, str]] = re.findall(pattern, text)
    out_images: list[TextNode] = []
    for match in matches:
        alt = match[0]
        src = match[1]
        out_images.append(TextNode(alt, "image", src))
    return out_images

def extract_markdown_links(text: str) -> list[TextNode]:
    pattern = r"\[(.*?)\]\((.*?)\)"
    matches: list[tuple[str, str]] = re.findall(pattern, text)
    out_images: list[TextNode] = []
    for match in matches:
        anchor = match[0]
        href = match[1]
        out_images.append(TextNode(anchor, "link", href))
    return out_images


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case "text":
            return LeafNode(None, text_node.text)
        case "bold":
            return LeafNode("b", text_node.text)
        case "italic":
            return LeafNode("i", text_node.text)
        case "code":
            return LeafNode("code", text_node.text)
        case "link":
            if text_node.url is None:
                raise ValueError("TextNode of type 'link' must include url")
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case "image":
            if text_node.url is None:
                raise ValueError("TextNode of type 'image' must include url")
            return LeafNode(
                "img", "", {"src": text_node.url, "alt": (text_node.text or "")}
            )
        case _:
            raise NotImplemented
