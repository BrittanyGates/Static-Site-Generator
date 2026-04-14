from textnode import TextType, TextNode
import os, shutil


def copy_contents_from_source_to_destination(source, destination):
    list_source_dir = os.listdir(source)

    for item in list_source_dir:
        source_full_path = os.path.join(source, item)
        destination_full_path = os.path.join(destination, item)

        if os.path.isfile(source_full_path):
            shutil.copy(source_full_path, destination_full_path)
        else:
            os.mkdir(destination_full_path)
            copy_contents_from_source_to_destination(source_full_path, destination_full_path)


def start_copy():
    source_dir = "static"
    destination_dir = "public"

    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)

    os.mkdir(destination_dir)
    copy_contents_from_source_to_destination(source_dir, destination_dir)


def main():
    start_copy()

    new_text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(new_text_node)


if __name__ == "__main__":
    main()
