from textnode import TextType, TextNode
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes: list = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue

        split_list: list = node.text.split(delimiter)

        if len(split_list) % 2 == 0:
            raise ValueError(f"Missing matching Markdown tag: {delimiter}")

        for indices in range(len(split_list)):
            if split_list[indices] == "":
                continue
            elif indices % 2 == 0:
                new_nodes.append(TextNode(split_list[indices], TextType.PLAIN_TEXT))
            else:
                new_nodes.append(TextNode(split_list[indices], text_type))

    return new_nodes


def extract_markdown_images(text):
    image_text: list = re.findall(r"!\[(.*?)\]\((.*?\..*?)\)", text)
    return image_text


def extract_markdown_links(text):
    link_text: list = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return link_text
