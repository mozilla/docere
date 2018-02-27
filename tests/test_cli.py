import tempfile
import shutil
import os
from contextlib import contextmanager
from click.testing import CliRunner
from docere.cli import render


@contextmanager
def isolated_knowledge_repo(kr_path, iso_path):
    """Sets up an isolated filesystem containing the example knowledge_repo

    Similar to click's isolated_filesystem:
    https://github.com/pallets/click/blob/master/click/testing.py
    """
    cwd = os.getcwd()
    tmp = tempfile.mkdtemp()
    try:
        shutil.copytree('tests/data/kr', os.path.join(tmp, iso_path))
        os.chdir(tmp)
        yield
    finally:
        os.chdir(cwd)
        shutil.rmtree(tmp, ignore_errors=True)


def test_render():
    runner = CliRunner()
    with isolated_knowledge_repo('tests/data/kr', 'kr'):
        runner.invoke(render, ['--knowledge-repo', 'kr'])
        assert os.path.isfile('output/user_count/index.html')
        assert os.path.isfile('output/user_count/post.json')


def test_index():
    runner = CliRunner()
    with isolated_knowledge_repo('tests/data/kr', 'kr'):
        runner.invoke(render, ['--knowledge-repo', 'kr'])
        assert os.path.isfile('output/index.html')

        with open('output/index.html', 'r') as infile:
            index = infile.read()

        assert "user_count/index.html" in index
