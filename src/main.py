from textnode import *
from block import *
import os
import shutil
import sys

#print("Hello World")
def main():
    basepath = ""
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    print(f"basepath: {basepath}")

    del_contents(os.path.abspath("docs"))
    copy_contents(os.path.abspath("static"),os.path.abspath("docs")) 
    generate_pages_recursive("content","template.html","docs",basepath)

def copy_contents(source, destination):
    
    for file in os.listdir(source):
        source_file_path = os.path.join(source,file)
        source_file_path = os.path.abspath(source_file_path)
        dest_file_path = os.path.join(destination,file)
        dest_file_path = os.path.abspath(dest_file_path)
        #print(source_file_path)
        #print(dest_file_path)
        if os.path.isfile(source_file_path):
            shutil.copy(source_file_path,dest_file_path)
        elif os.path.isdir(source_file_path):
                os.mkdir(dest_file_path)
                copy_contents(source_file_path,dest_file_path)
                
def del_contents(destination):

    for file in os.listdir(destination):
        file_path = os.path.join(destination,file)
        if os.path.isfile(file_path):
            os.remove(file_path)
        if os.path.isdir(file_path):
            del_contents(file_path)
            os.rmdir(file_path)

def extract_tile(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("#"):
            return line[2:].strip()
    raise ValueError("Missing Header")

def generate_page(from_path,template_path, dest_path,basepath):
    #from_path = os.path.join(from_path,template_path)
    from_path = os.path.abspath(from_path)
    #from_path = os.path.join(from_path,"index.md")
    template_path = os.path.abspath(template_path)
    
    dest_path = os.path.abspath(dest_path)
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = ""
    with open(from_path,'r') as markdown_file:
        markdown = markdown_file.read()

    #########################
    #markdown_lines = markdown.split("\n")
    #for line in markdown_lines:
            #print(line)

    html_nodes = markdown_to_html_node(markdown)
    html_str = html_nodes.to_html()
    title = extract_tile(markdown)
    
    with open(template_path,'r') as templatefile:
        tmp_html_template = templatefile.read()
    
    tmp_html_template = tmp_html_template.replace("{{ Title }}",title)
    tmp_html_template = tmp_html_template.replace("{{ Content }}",html_str)
    tmp_html_template = tmp_html_template.replace('href="/',f'href="{basepath}')
    tmp_html_template = tmp_html_template.replace('src="/',f'src="{basepath}')

    #print(tmp_html_template)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path,exist_ok=True)
    
    dest_path = os.path.join(dest_path,"index.html")
    #print(f"dest: {dest_path}")
    with open(dest_path,"w") as new_html_template:
        new_html_template.write(tmp_html_template)

def generate_pages_recursive(dir_path_content,template_path,dest_dir_path,basepath):
    dir_path_content = os.path.abspath(dir_path_content)
    template_path = os.path.abspath(template_path)
    dest_dir_path = os.path.abspath(dest_dir_path)
    #print(f"Generating page from {dir_path_content} to {dest_dir_path} using {template_path}")

    for file in os.listdir(dir_path_content):
        #path to content and subfolders
        content_path = os.path.join(dir_path_content,file)
        
        # file found, send to generate page
        if os.path.isfile(content_path):
            generate_page(content_path,template_path,dest_dir_path,basepath)

        # directory found, make new directory, send new directory address through again
        elif os.path.isdir(content_path):
            dest_path = os.path.join(dest_dir_path,file)
            if dest_dir_path != "":
                os.makedirs(dest_path,exist_ok=True)
            #print(f"directory: {content_path} -> {os.path.join(dest_dir_path,file)}")
            generate_pages_recursive(content_path,template_path,os.path.join(dest_dir_path,file),basepath)
        

if __name__ == "__main__":
    main()
    #exit()