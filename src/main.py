from textnode import TextNode, split_nodes_image


def main():
    node = TextNode(
        "I ain't the ![sharpest tool](assets/spoon.png) in the ![shed](assets/outhouse.png)",
        "text",
    )
    expected = [
        TextNode("I ain't the ", "text"),
        TextNode("sharpest tool", "image", "assets/spoon.png"),
        TextNode(" in the ", "text"),
        TextNode("shed", "image", "assets/outhouse.png"),
    ]
    print(split_nodes_image([node]))
    print("=====")
    print(expected)


if __name__ == "__main__":
    main()
