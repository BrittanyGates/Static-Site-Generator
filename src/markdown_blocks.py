"""This module contains the function to take a raw Markdown string and returns a list of block strings."""
from enum import Enum
from leafnode import LeafNode
from parentnode import ParentNode
from splitnode import text_to_textnodes, markdown_to_blocks
from textnode import text_node_to_html_node
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def text_to_children(text):
    text_objects = text_to_textnodes(text)
    text_list = []
    for item in text_objects:
        converted_node = text_node_to_html_node(item)
        text_list.append(converted_node)
    return text_list


def paragraph_to_html_node(node):
    cleaned_text = " ".join(node.split())
    paragraph_text = text_to_children(cleaned_text)
    return ParentNode("p", paragraph_text)


def heading_to_html_node(node):
    count = 0
    for item in node:
        if item == "#":
            count += 1
        elif item != "#":
            break
    heading_tag_name = f"h{count}"
    cleaned_text = node[count:].strip()
    heading_text = text_to_children(cleaned_text)
    return ParentNode(heading_tag_name, heading_text)


def quote_to_html_node(node):
    lines = node.split("\n")
    cleaned_line = ""
    new_lines = []
    joined_text = ""
    for line in lines:
        cleaned_line = line.strip(">").strip()
        new_lines.append(cleaned_line)
    joined_text = " ".join(new_lines)
    quote_text = text_to_children(joined_text)
    return ParentNode("blockquote", quote_text)


def code_to_html_node(node):
    stripped_text = node.strip("```").strip()
    code_text = LeafNode(None, stripped_text)
    inner_node = ParentNode("code", [code_text])
    outer_node = ParentNode("pre", [inner_node])
    return outer_node


def unordered_list_to_html_node(node):
    lines = node.split("\n")
    li_nodes = []
    cleaned_line = ""
    for line in lines:
        cleaned_line = line.lstrip("-*").strip()
        children = text_to_children(cleaned_line)
        li_node = ParentNode("li", children)
        li_nodes.append(li_node)
    return ParentNode("ul", li_nodes)


def ordered_list_to_html_node(node):
    lines = node.split("\n")
    li_nodes = []
    cleaned_line = ""
    count = 0
    for line in lines:
        count += 1
        cleaned_line = line[len(f"{count}. "):]
        children = text_to_children(cleaned_line)
        li_node = ParentNode("li", children)
        li_nodes.append(li_node)
    return ParentNode("ol", li_nodes)


def block_to_block_type(block):
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith(">") or block.startswith("> "):
        lines = block.split("\n")
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif block.startswith("- "):
        lines = block.split("\n")
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif block.startswith("1. "):
        counter = 0
        lines = block.split("\n")
        for line in lines:
            counter += 1
            if not line.startswith(f"{counter}. "):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    block_list = markdown_to_blocks(markdown)
    html_nodes = []
    for block in block_list:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            node = paragraph_to_html_node(block)
            html_nodes.append(node)
        elif block_type == BlockType.HEADING:
            node = heading_to_html_node(block)
            html_nodes.append(node)
        elif block_type == BlockType.QUOTE:
            node = quote_to_html_node(block)
            html_nodes.append(node)
        elif block_type == BlockType.CODE:
            node = code_to_html_node(block)
            html_nodes.append(node)
        elif block_type == BlockType.UNORDERED_LIST:
            node = unordered_list_to_html_node(block)
            html_nodes.append(node)
        else:
            node = ordered_list_to_html_node(block)
            html_nodes.append(node)
    return ParentNode("div", html_nodes)
