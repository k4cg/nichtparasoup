#!/usr/bin/env python

####################


tag_stripOnBuild = 'striponbuild'


#####################

import sys
from os import path
import re
from bs4 import BeautifulSoup, NavigableString, Comment
import html5lib   # used by BeautifulSoup


def src_is_external(source):
    return source.find('://') > -1


if __name__ == '__main__':

    file = sys.argv[1]
    if not file and not path.isfile(file):
        sys.stderr.write("no such file")
        sys.exit(1)

    directory = path.dirname(file)

    doc = BeautifulSoup(open(file, 'r'), "html5lib")

    for strip in doc.find_all(tag_stripOnBuild):
        strip.extract()

    for comment in doc.find_all(text=lambda text: isinstance(text, Comment)):
        comment.extract()

    for node in doc.find_all(text=True):
        if isinstance(node, NavigableString) and node.parent.name != "[document]":
            node_string = re.sub(r"[ \t\n\r]+", " ", node.string, flags=re.MULTILINE).strip()
            if node_string == "":
                node.extract()
            else:
                node.replace_with(node_string)

    for script in doc.find_all('script', {'src': True}):
        src = script['src']
        if src and not src_is_external(src):
            srcPath = path.join(directory, src)
            if path.isfile(srcPath):
                del script['src']
                script.string = "\n" + open(srcPath, 'r').read() + "\n"
            else:
                script.extract()

    for link in doc.find_all('link', {'rel': 'stylesheet', 'href': True}):
        src = link['href']
        if src and not src_is_external(src):
            srcPath = path.join(directory, src)
            if path.isfile(srcPath):
                style_inline = doc.new_tag("style", type="text/css")
                style_inline.string = "\n" + open(srcPath, 'r').read() + "\n"
                link.replace_with(style_inline)
            else:
                link.extract()

    ##### debug
    #print(doc.prettify())
    #sys.exit(0)
    #####

    doc_string_part_clean = ""
    doc_string_parts_clean = []
    for doc_string_part_raw in doc.prettify().split("\n"):
        doc_string_part_raw = doc_string_part_raw.strip()
        if len(doc_string_part_clean) + len(doc_string_part_raw) > 120:
            doc_string_parts_clean.append(doc_string_part_clean)
            doc_string_part_clean = doc_string_part_raw
        else:
            doc_string_part_clean += doc_string_part_raw
    doc_string_parts_clean.append(doc_string_part_clean)

    print("\n".join(str(part) for part in doc_string_parts_clean))
