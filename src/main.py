from functools import reduce
from typing import Callable
import os
import shutil
from blocknode import str_to_block
from blocktextconv import markdown_to_html_node, block_type_heading
from inlinetextconv import text_to_textnodes
from textnode import markdown_to_blocks


def readfile(file_path: str) -> str:
    output = ""
    with open(file_path, "r") as f:
        output = f.read()

    return output


def extract_title(markdown: str) -> str:
    blocks = [str_to_block(x) for x in markdown_to_blocks(markdown)]
    heading_block = None
    for block in blocks:
        if block.block_type == block_type_heading and block.heading_level == 1:
            heading_block = block
    if heading_block is None:
        raise ValueError("invalid markdown: file must contain a single h1 heading")
    return heading_block.inner_text


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    txt = ""
    with open(from_path, "r") as f:
        txt = f.read()
    html = markdown_to_html_node(txt)
    title = extract_title(txt)

    template = ""
    with open(template_path, "r") as f:
        template = f.read()

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html.to_html())

    with open(dest_path, "w") as f:
        f.write(template)


def recurse_apply_fn(
    src: str, dest_dir: str, fn: Callable[[str, str], None]
) -> list[str]:
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.mkdir(dest_dir)

    copied: list[str] = []

    for file in os.listdir(src):
        file_abs = os.path.abspath(src + "/" + file)
        if os.path.isdir(file_abs):
            os.mkdir(dest_dir + f"/{file}")
            rec_list = recurse_apply_fn(file_abs, f"{dest_dir}/{file}", fn)
            copied.extend(rec_list)
        else:
            fn(src + "/" + file, dest_dir)
            copied.append(file_abs)
    return copied


def generate_html():
    # base_dir = os.path.split(os.getcwd())[0]
    # os.chdir(base_dir)

    base_dir = os.getcwd()

    public_dir = base_dir + "/public"
    static_dir = base_dir + "/static"
    content_dir = base_dir + "/content"

    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    os.mkdir(public_dir)

    def copy_file(src: str, dest: str):
        out_path = dest = dest + "/" + os.path.basename(src)
        shutil.copy2(src, out_path)

    output_txt = recurse_apply_fn(static_dir, public_dir, copy_file)
    [print("Copying: " + x.replace(base_dir, "")) for x in output_txt]

    def convert_file(src: str, dest: str):
        out_path = dest + "/" + os.path.basename(src.replace(".md", ".html"))
        generate_page(src, "template.html", out_path)

    output_txt = recurse_apply_fn(content_dir, public_dir, convert_file)
    [print("Converting: " + x.replace(base_dir, "")) for x in output_txt]


def main():
    generate_html()


if __name__ == "__main__":
    main()
