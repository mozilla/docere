from jinja2 import Environment, FileSystemLoader
import os
import shutil

this_dir, this_filename = os.path.split(__file__)

ENV = Environment(loader=FileSystemLoader(
    os.path.join(this_dir, 'templates/')
))
TEMPLATE = ENV.get_template('index.html')


def build_index(reports, directory='.'):
    index = TEMPLATE.render(reports=reports)

    with open(os.path.join(directory, 'index.html'), 'w') as outfile:
        outfile.write(index)

    shutil.copytree(
        os.path.join(this_dir, 'skeleton/css'),
        os.path.join(directory, 'css')
    )
