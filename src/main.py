from markdown_blocks import markdown_to_html_node, extract_title
import os, shutil, sys

basepath = "/"
if len(sys.argv) > 1:
    basepath = sys.argv[1]


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
    destination_dir = "docs"

    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)

    os.mkdir(destination_dir)
    copy_contents_from_source_to_destination(source_dir, destination_dir)


def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")

    with open(f"{from_path}", "r") as from_path_content, open(f"{template_path}", "r") as template_path_content:
        content_html = from_path_content.read()
        template_path_content = template_path_content.read()

    from_path_content = markdown_to_html_node(content_html).to_html()
    title = extract_title(content_html)
    final_html = template_path_content.replace("{{ Title }}", title).replace("{{ Content }}", from_path_content)
    final_html = final_html.replace('href="/', f'href="{base_path}')
    final_html = final_html.replace('src="/', f'src="{base_path}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(f"{dest_path}", "w") as dest_path_content:
        dest_path_content.write(final_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    print(f"Generating page from {dir_path_content} to {dest_dir_path} using {template_path}.")

    list_source_dir = os.listdir(dir_path_content)

    for item in list_source_dir:
        source_full_path = os.path.join(dir_path_content, item)
        destination_full_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(source_full_path):
            if item.endswith(".md"):
                dest_filename = item.replace(".md", ".html")
                dest_path = os.path.join(dest_dir_path, dest_filename)
                generate_page(source_full_path, template_path, dest_path, base_path)
        else:
            generate_pages_recursive(source_full_path, template_path, destination_full_path, base_path)


def main():
    start_copy()
    generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()
