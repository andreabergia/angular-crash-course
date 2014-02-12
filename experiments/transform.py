# -*- coding: utf-8 -*-

import markdown
import codecs
import os
import shutil
import pygments
import json


def prepare(outf):
    """Clean up the output directory and create it if necessary"""
    if os.path.exists(outf):
        shutil.rmtree(outf)
    os.makedirs(outf)


def copy_assets(inf, outf):
    """Copy assets from the input folder to the output folder"""
    shutil.copytree(os.path.join(inf, 'js'), os.path.join(outf, 'js'))
    shutil.copytree(os.path.join(inf, 'css'), os.path.join(outf, 'css'))
    shutil.copytree(os.path.join(inf, 'fonts'), os.path.join(outf, 'fonts'))


def transform_one_page(in_page, out_page, title):
    """Transforms one markdown page into one html page"""
    with codecs.open(in_page, 'r', 'utf-8') as inf:
        content = inf.read()
    with codecs.open('page_template.html', 'r', 'utf-8') as inf:
        from jinja2 import Template
        template = Template(inf.read())
    md = markdown.markdown(content, ['fenced_code', 'codehilite', 'def_list', 'footnotes', 'tables', 'nl2br', 'toc', 'smart_strong'])
    with codecs.open(out_page, 'w', 'utf-8') as outf:
        outf.write(template.render(content=md, title=title))


def transform_index(pages):
    """Creates the index page"""
    with codecs.open('index_template.html', 'r', 'utf-8') as inf:
        from jinja2 import Template
        template = Template(inf.read())
    with codecs.open(os.path.join('out', 'index.html'), 'w', 'utf-8') as outf:
        outf.write(template.render(pages=pages))


def transform():
    """Transforms everything"""
    prepare('out')
    copy_assets('assets', 'out')
    with open(os.path.join('pages', 'config.json'), 'r') as f:
        pages = json.load(f)

    for page in pages:
        title = page['title']
        in_page = page['filename']
        transform_one_page(os.path.join('pages', in_page) + '.md', os.path.join('out', in_page) + '.html', title)

    transform_index(pages)


if __name__ == '__main__':
    transform()
