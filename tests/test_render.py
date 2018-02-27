from docere.render import _get_posts, tmp_cd
import os


def compare_post_lists(this, that):
    return (
        all([post in this for post in that]) and
        all([post in that for post in this])
    )


def test_get_posts():
    actual = _get_posts('tests/data/kr')
    expected = [
        {
            "title": "Crash Count",
            "publish_date": "2018-01-01",
            "author": "Joseph Blowseph",
            "file": "not_index.html",
            "path": "tests/data/kr/crash_count/not_index.html",
            "dir": "tests/data/kr/crash_count",
        },
        {
            "title": "User Count",
            "publish_date": "2018-01-02",
            "author": "Joe Blow",
            "file": "index.html",
            "path": "tests/data/kr/user_count/index.html",
            "dir": "tests/data/kr/user_count",
        },
    ]

    assert compare_post_lists(actual, expected)


def test_tmp_cd():
    basewd = os.getcwd()
    with tmp_cd('tests'):
        assert os.getcwd() != basewd

    assert os.getcwd() == basewd
