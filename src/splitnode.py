"""This module contains the functions to create TextNodes from raw Markdown strings."""
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


def split_nodes_image(old_nodes):
    new_nodes: list = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        image_markdown = extract_markdown_images(node.text)

        # If the node doesn't have any images
        if len(image_markdown) == 0:
            new_nodes.append(node)
            continue

        for alt, url in image_markdown:
            images = f"![{alt}]({url})"
            sections = remaining_text.split(images, 1)

            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.PLAIN_TEXT))

            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            remaining_text = sections[1]

        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.PLAIN_TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes: list = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        link_markdown = extract_markdown_links(node.text)

        # If the node doesn't have any links
        if len(link_markdown) == 0:
            new_nodes.append(node)
            continue

        for alt, url in link_markdown:
            links = f"[{alt}]({url})"
            sections = remaining_text.split(links, 1)

            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.PLAIN_TEXT))

            new_nodes.append(TextNode(alt, TextType.LINK, url))
            remaining_text = sections[1]

        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.PLAIN_TEXT))

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.PLAIN_TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC_TEXT)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []

    for block in blocks:
        stripped_block = block.strip()

        if stripped_block != "":
            new_blocks.append(stripped_block)

    return new_blocks
