from collections import namedtuple
from functional import seq
from shutil import copytree, rmtree
from contextlib import contextmanager
from .plugins.index import build_index
import os
import json

REPORT_CONFIG_FILE = 'report.json'
REPORT_DEFAULTS = {
    'file': 'index.html'
}

Directory = namedtuple('Directory', ['path', 'dirnames', 'filenames'])


def _load_report_config(directory):
    """Take Directory object containing a config file and return the contents

    Returns a dictionary containing the config contents. The only guarunteed
    keys are "path" and any keys listed in REPORT_DEFAULTS
    """
    # Load config File
    config_path = os.path.join(directory.path, REPORT_CONFIG_FILE)
    with open(config_path, 'r') as infile:
        config = json.load(infile)

    # Set defaults
    out = REPORT_DEFAULTS.copy()
    for (key, value) in config.items():
        out[key] = value

    # Add directory in which config file was found
    out['dir'] = directory.path
    out['path'] = os.path.join(directory.path, out['file'])

    return out


def _get_reports(path='.'):
    return (
        seq(os.walk(path))
        .map(lambda d: Directory(*d))
        .filter(lambda d: REPORT_CONFIG_FILE in d.filenames)
        .map(_load_report_config)
        .to_list()
    )


@contextmanager
def tmp_cd(path):
    """Temporarily change working directory"""
    curdir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(curdir)


def main(kr, outdir):
    metadata_generators = [
        build_index,
    ]

    # Replace output directory with copy of knowledge repo
    rmtree(outdir, ignore_errors=True)
    copytree(kr, outdir)
    with tmp_cd(outdir):
        reports = _get_reports()

        for meta_gen in metadata_generators:
            meta_gen(reports)
