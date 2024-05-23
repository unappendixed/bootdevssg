from htmlnode import HTMLNode
from typing import Sequence


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        children: Sequence[HTMLNode],
        props: dict[str, str] | None = None,
    ):
        super().__init__(tag, None, children, props)
        self.children = children
        return

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ParentNode):
            return False
        if (
            other.tag == self.tag
            and other.children == self.children
            and other.props == self.props
        ):
            return True
        return False

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("cannot construct ParentNode html without tag")
        if len(self.children) == 0:
            raise ValueError("cannot construct ParentNode html without children")

        str_builder = ""
        for c in self.children:
            str_builder += c.to_html()
        return f"<{self.tag}>{str_builder.strip()}</{self.tag}>"
