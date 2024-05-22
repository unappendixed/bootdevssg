from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    #  (tag: str | None = None, value: str | None = None, children: list[HTMLNode] | None = None, props: dict[str, str] | None = None) -> None
    def __init__(
        self, tag: str | None, value: str, props: dict[str, str] | None = None
    ):
        self.value = value
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.tag is None:
            return self.value
        elif self.props is not None:
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"
