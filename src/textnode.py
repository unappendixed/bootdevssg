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


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: str
) -> list[TextNode]:
    output_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != "text":
            output_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) == 1:
            # doesn't contain delim
            output_nodes.append(node)
            continue
        if len(parts) % 2 == 0:
            raise ValueError("invalid markdown")

        for i, p in enumerate(parts):
            if p == "":
                continue
            if i % 2 == 1:
                output_nodes.append(TextNode(p, text_type))
            else:
                output_nodes.append(TextNode(p, "text"))
    return output_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    output_nodes: list[TextNode] = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            output_nodes.append(node)
            continue
        link = links[0]
        parts = node.text.split(f"[{link[0]}]({link[1]})", maxsplit=1)
        head = split_nodes_link([TextNode(parts[0], "text")])
        body = TextNode(link[0], "link", link[1])
        tail = split_nodes_link([TextNode(parts[1], "text")])
        if parts[0] != "":
            output_nodes.extend(head)
        output_nodes.extend([body])
        if parts[1] != "":
            output_nodes.extend(tail)
    return output_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    output_nodes: list[TextNode] = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            output_nodes.append(node)
            continue
        image = images[0]
        parts = node.text.split(f"![{image[0]}]({image[1]})", maxsplit=1)
        head = split_nodes_image([TextNode(parts[0], "text")])
        body = TextNode(image[0], "image", image[1])
        if parts[0] != "":
            output_nodes.extend(head)
        output_nodes.extend([body])
        if parts[1] != "":
            tail = split_nodes_image([TextNode(parts[1], "text")])
            output_nodes.extend(tail)
    return output_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches: list[tuple[str, str]] = re.findall(pattern, text)
    out_images: list[tuple[str, str]] = []
    for match in matches:
        alt = match[0]
        src = match[1]
        out_images.append((alt, src))
    return out_images


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    pattern = r"\[(.*?)\]\((.*?)\)"
    matches: list[tuple[str, str]] = re.findall(pattern, text)
    out_images: list[tuple[str, str]] = []
    for match in matches:
        anchor = match[0]
        href = match[1]
        out_images.append((anchor, href))
    return out_images


def text_to_textnodes(text: str) -> list[TextNode]:
    node = TextNode(text, "text")
    node = split_nodes_delimiter([node], "**", "bold")
    node = split_nodes_delimiter(node, "*", "italic")
    node = split_nodes_delimiter(node, "`", "code")
    node = split_nodes_image(node)
    node = split_nodes_link(node)

    return node

def markdown_to_blocks(markdown: str) -> list[str]:

    def flattenBuffer(buffer: list[str]) -> str:
         output = " ".join(x for x in buffer if x.strip() != "").strip()
         if output != "":
             return output
         else:
             return ""

    lines = markdown.splitlines(True)
    output_list: list[str] = []
    buffer_list: list[str] = []
    for line in lines:
        if line == "\n" or line == "\r\n":
            new_block = flattenBuffer(buffer_list)
            if new_block != "":
                output_list.append(new_block)
            buffer_list = []
        else:
            buffer_list.append(line.strip())

    if len(buffer_list) != 0:
        final = flattenBuffer(buffer_list)
        if final != "":
            output_list.append(final)
    return output_list


