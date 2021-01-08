from collections import Counter
from jinja2 import Environment, FileSystemLoader
import os
import re
import shutil

this_dir, this_filename = os.path.split(__file__)

ENV = Environment(loader=FileSystemLoader(
    os.path.join(this_dir, 'templates/')
))
TEMPLATE = ENV.get_template('index.html')


def build_index(reports, directory='.'):
    rollup = {
        "products": Counter(),
        "areas": Counter(),
        "artifacts": Counter(),
        "tags": Counter(),
    }
    for report in reports:
        for k in rollup:
            rollup[k].update(getattr(report, k))
    index = TEMPLATE.render(reports=reports, slugify=slugify, directory=rollup)

    with open(os.path.join(directory, 'index.html'), 'w') as outfile:
        outfile.write(index)

    shutil.copytree(
        os.path.join(this_dir, 'skeleton/css'),
        os.path.join(directory, 'css')
    )

    shutil.copytree(
        os.path.join(this_dir, 'assets'),
        os.path.join(directory, 'assets')
    )


def slugify(report):
    # Returns a string representing the slug for the report.
    report_title = re.sub(r'[^A-Za-z0-9]+', '', report.title)[:32]
    slug = report_title + "_" + report.publish_date.strftime("%Y-%m-%d")
    return slug
