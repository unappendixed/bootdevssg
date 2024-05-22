class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props_to_html()})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HTMLNode):
            return False
        if (
            other.tag == self.tag
            and other.value == self.value
            and other.props == self.props
            and other.children == self.children
        ):
            return True
        else:
            return False

    def to_html(self) -> str:
        raise NotImplemented

    def props_to_html(self):
        output = ""
        if self.props is None:
            return None
        for k, v in self.props.items():
            output += f'{k}="{v}" '
        return output.strip()
