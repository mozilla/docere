from jinja2 import Template
import os


with open('templates/index.html', 'r') as infile:
    TEMPLATE = Template(infile.read())


def build_index(posts, directory='.'):
    index = TEMPLATE.render(posts=posts)

    with open(os.path.join(directory, 'index.html'), 'w') as outfile:
        outfile.write(index)
