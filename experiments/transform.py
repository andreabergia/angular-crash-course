# -*- coding: utf-8 -*-

import markdown
import codecs
import os
import shutil
import pygments

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

def transform():
    """Transforms everything"""
    prepare('out')
    copy_assets('assets', 'out')
    for in_page in os.listdir('pages'):
        out_page = os.path.splitext(in_page)[0] + '.html'
        out_page = os.path.join('out', out_page)
        transform_one_page(os.path.join('pages', in_page), out_page, 'titolo')

if __name__ == '__main__':
    transform()
