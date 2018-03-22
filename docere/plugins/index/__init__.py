from jinja2 import Template
import os

this_dir, this_filename = os.path.split(__file__)


with open(os.path.join(this_dir, 'templates/index.html'), 'r') as infile:
    TEMPLATE = Template(infile.read())


def build_index(reports, directory='.'):
    index = TEMPLATE.render(reports=reports)

    with open(os.path.join(directory, 'index.html'), 'w') as outfile:
        outfile.write(index)
