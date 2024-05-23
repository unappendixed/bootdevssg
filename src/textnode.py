class TextNode:
    def __init__(self, text: str, text_type: str, url: str | None = None):
        self.text = text.strip()
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
