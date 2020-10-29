from docere.render import _get_reports, tmp_cd
import os


def compare_report_lists(this, that):
    return (
        all([report in this for report in that]) and
        all([report in that for report in this])
    )


def test_get_reports():
    actual = _get_reports('tests/data/kr')
    expected = [
        {
            "title": "Crash Count",
            "publish_date": "2018-01-01",
            "author": "Joseph Blowseph",
            "file": "not_index.html",
            "path": "tests/data/kr/crash_count/not_index.html",
            "dir": "tests/data/kr/crash_count",
            "abstract": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        },
        {
            "title": "User Count",
            "publish_date": "2018-01-02",
            "author": "Joe Blow",
            "file": "index.html",
            "path": "tests/data/kr/user_count/index.html",
            "dir": "tests/data/kr/user_count",
        },
        {
            "title": "Mozilla Manifesto",
            "publish_date": "2018-01-01",
            "author": "Mitchell Baker",
            "file": "index.html",
            "link": "https://www.mozilla.org/en-US/about/manifesto/",
            "path": "https://www.mozilla.org/en-US/about/manifesto/",
            "abstract": "The open, global internet is the most powerful communication and collaboration resource we have ever seen."
        },
        {
            "title": "My First TOML Report",
            "publish_date": "2018-01-02",
            "author": "Tom",
            "file": "index.html",
            "path": "tests/data/kr/toml_report/index.html",
            "dir": "tests/data/kr/toml_report",
            "tags": ["first_tag"]
        },
        {
            "title": "Just Another JSON Report",
            "publish_date": "2018-01-02",
            "author": "Joe Blow",
            "file": "index.html",
            "path": "tests/data/kr/json_toml_report/index.html",
            "dir": "tests/data/kr/json_toml_report",
        },
    ]

    assert compare_report_lists(actual, expected)


def test_tmp_cd():
    basewd = os.getcwd()
    with tmp_cd('tests'):
        assert os.getcwd() != basewd

    assert os.getcwd() == basewd
