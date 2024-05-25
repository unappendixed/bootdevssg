import os
import shutil
from blocktextconv import markdown_to_html_node

def readfile(file_path: str) -> str:
    output = ""
    with open(file_path, "r") as f:
        output = f.read()

    return output

def move_static_to_public():
    public_dir = f"{os.getcwd()}/public/"
    static_dir = f"{os.getcwd()}/static/"

    [os.remove(public_dir + x) for x in os.listdir("public")]
    [shutil.copy2(static_dir + x, public_dir + x) for x in os.listdir("static")]
    print([x for x in os.listdir("static")])

    # [shutil.copy2(x) for x in os.listdir("static")]

def main():
    move_static_to_public()
    

if __name__ == "__main__":
    main()
