from collections import namedtuple
from shutil import copytree, rmtree
from contextlib import contextmanager
from .plugins.index import build_index
import attr
import datetime
import os
import json
import sys
import glob
from typing import List, Optional

import toml

REPORT_CONFIG_FILES = {'report.json': json.load, 'report.toml': toml.load}
REPORT_DEFAULTS = {
    'file': 'index.html'
}

Directory = namedtuple('Directory', ['path', 'dirnames', 'filenames'])


@attr.s(auto_attribs=True)
class Report:
    title: str
    publish_date: datetime.date
    authors: List[str]
    path: str
    abstract: Optional[str]
    products: List[str]
    areas: List[str]
    artifacts: List[str]
    tags: List[str]

    @classmethod
    def from_dict(cls, d: dict) -> "Report":
        publish_date = datetime.datetime.strptime(d["publish_date"], "%Y-%m-%d").date()
        authors = d.get("authors") or [d["author"]]
        kwargs = {}
        for key in ("products", "areas", "artifacts", "tags"):
            kwargs[key] = []
            if key in d:
                if isinstance(d[key], str):
                    kwargs[key] = [d[key]]
                else:
                    kwargs[key] = d[key]
        return cls(
            title=d["title"],
            publish_date=publish_date,
            authors=authors,
            path=d["path"],
            abstract=d.get("abstract"),
            **kwargs
        )


def _load_report_directory(directory):
    """Take Directory object containing a config file and return the contents

    Returns a dictionary containing the config contents. The only guarunteed
    keys are "path" and any keys listed in REPORT_DEFAULTS
    """
    # Load config File
    for candidate, loader in REPORT_CONFIG_FILES.items():
        config_path = os.path.join(directory.path, candidate)
        if not os.path.exists(config_path):
            continue
        with open(config_path, 'r') as infile:
            config = loader(infile)
        break
    else:
        raise ValueError(
            f"Thought there was a valid config file in {directory} but couldn't find one"
        )

    # Set defaults
    out = REPORT_DEFAULTS.copy()
    out['source'] = os.path.normpath(config_path)
    for (key, value) in config.items():
        out[key] = value

    if 'link' in config:
        out['path'] = config['link']
    else:
        # Add directory in which config file was found
        out['dir'] = os.path.normpath(directory.path)
        out['path'] = os.path.normpath(os.path.join(directory.path, out['file']))

    return out


def _get_external_reports(base, path):
    # Ensure that relative paths are constructed with respect to the right base
    with tmp_cd(base):
        json_candidates = glob.glob(f"{path}/**/*.json", recursive=True)
        toml_candidates = glob.glob(f"{path}/**/*.toml", recursive=True)
        reports = []
        for filename in json_candidates:
            with open(filename, "r") as f:
                reports.append((filename, json.load(f)))
        for filename in toml_candidates:
            reports.append((filename, toml.load(filename)))

    results = []
    for filename, report in reports:
        if 'link' not in report:
            raise ValueError(f"External report {filename} must contain a `link` property.")
        out = REPORT_DEFAULTS.copy()
        for k, v in report.items():
            out[k] = v
        out['source'] = filename
        out['path'] = report['link']
        results.append(out)
    return results


def _get_reports(path='.'):
    # Ensure that relative paths are constructed with respect to the right base
    with tmp_cd(path):
        dirs = (Directory(*d) for d in os.walk("."))
        with_config = (d for d in dirs if set(d.filenames) & set(REPORT_CONFIG_FILES))
        reports = [_load_report_directory(d) for d in with_config]
    return reports


@contextmanager
def tmp_cd(path):
    """Temporarily change working directory"""
    curdir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(curdir)


def main(kr, external_reports, outdir):
    metadata_generators = [
        build_index,
    ]

    abs_kr = os.path.abspath(kr)
    abs_outdir = os.path.abspath(outdir)
    if os.path.commonprefix([abs_kr, abs_outdir]) == abs_kr:
        print("Outdir cannot be a child of the repository.", file=sys.stderr)
        sys.exit(1)

    # Replace output directory with copy of knowledge repo
    rmtree(outdir, ignore_errors=True)
    copytree(kr, outdir)
    report_dicts = (
        _get_reports(outdir) +
        _get_external_reports(outdir, external_reports)
    )
    reports = [Report.from_dict(r) for r in report_dicts]
    with tmp_cd(outdir):
        for meta_gen in metadata_generators:
            meta_gen(reports)
