# -*- coding: utf-8 -*-

import markdown
import codecs

def transform_one_page():
    with codecs.open('lesson-01.md', 'r', 'utf-8') as inf:
        content = inf.read()
    with codecs.open('page_template.html', 'r', 'utf-8') as inf:
        from jinja2 import Template
        template = Template(inf.read())
    md = markdown.markdown(content, ['fenced_code', 'codehilite', 'def_list', 'footnotes', 'tables', 'nl2br', 'toc', 'smart_strong'])
    with codecs.open('prova.html', 'w', 'utf-8') as outf:
        outf.write(template.render(content=md))

if __name__ == '__main__':
    transform_one_page()
