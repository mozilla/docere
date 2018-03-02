from jinja2 import Template
import os


with open('templates/index.html', 'r') as infile:
    TEMPLATE = Template(infile.read())


def build_index(reports, directory='.'):
    index = TEMPLATE.render(reports=reports)

    with open(os.path.join(directory, 'index.html'), 'w') as outfile:
        outfile.write(index)
