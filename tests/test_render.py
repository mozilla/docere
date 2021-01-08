from docere.render import _get_reports, _get_external_reports, tmp_cd, Report
import os


def contains_at_least(actual, expected):
    """Asserts that all reports that appear in `expected` appear in `actual`.
    All fields defined on the expected report must match exactly on the actual report.
    There are allowed to be extra reports in `actual` and the actual reports
    are allowed to have extra fields.
    """
    actual_by_source = {d["source"]: d for d in actual}
    expected_by_source = {d["source"]: d for d in expected}
    assert len(actual_by_source) == len(actual)
    assert len(expected_by_source) == len(expected)
    for source, expected_report in expected_by_source.items():
        assert source in actual_by_source.keys()
        actual_report = actual_by_source[source]
        for key in expected_report:
            assert actual_report[key] == expected_report[key]
    return True


def test_get_reports():
    actual = _get_reports('tests/data/kr')
    expected = [
        {
            "title": "Crash Count",
            "publish_date": "2018-01-01",
            "author": "Joseph Blowseph",
            "file": "not_index.html",
            "source": "tests/data/kr/crash_count/report.json",
            "path": "tests/data/kr/crash_count/not_index.html",
            "dir": "tests/data/kr/crash_count",
            "abstract": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        },
        {
            "title": "User Count",
            "publish_date": "2018-01-02",
            "author": "Joe Blow",
            "file": "index.html",
            "source": "tests/data/kr/user_count/report.json",
            "path": "tests/data/kr/user_count/index.html",
            "dir": "tests/data/kr/user_count",
        },
        {
            "title": "Mozilla Manifesto",
            "publish_date": "2018-01-01",
            "author": "Mitchell Baker",
            "file": "index.html",
            "source": "tests/data/kr/some_external_report/report.json",
            "link": "https://www.mozilla.org/en-US/about/manifesto/",
            "path": "https://www.mozilla.org/en-US/about/manifesto/",
            "abstract": "The open, global internet is the most powerful communication and collaboration resource we have ever seen."  # noqa:E501
        },
        {
            "title": "My First TOML Report",
            "publish_date": "2018-01-02",
            "author": "Tom",
            "file": "index.html",
            "source": "tests/data/kr/toml_report/report.toml",
            "path": "tests/data/kr/toml_report/index.html",
            "dir": "tests/data/kr/toml_report",
        },
        {
            "title": "Just Another JSON Report",
            "publish_date": "2018-01-02",
            "author": "Joe Blow",
            "file": "index.html",
            "source": "tests/data/kr/json_toml_report/report.json",
            "path": "tests/data/kr/json_toml_report/index.html",
            "dir": "tests/data/kr/json_toml_report",
        }
    ]

    assert contains_at_least(actual, expected)

    external = [
        {
            "source": "tests/data/kr/external/test1.toml",
        },
        {
            "source": "tests/data/kr/external/nested/test2.json",
        }
    ]

    assert contains_at_least(_get_external_reports("tests/data/kr/external"), external)


def test_tmp_cd():
    basewd = os.getcwd()
    with tmp_cd('tests'):
        assert os.getcwd() != basewd

    assert os.getcwd() == basewd


def test_report_list_conversions():
    d = {
        "title": "My report",
        "publish_date": "2020-02-02",
        "authors": ["Tim", "Kimmy"],
        "path": ".",
        "tags": ["spam", "eggs"],
        "products": "Fenix",
    }
    report = Report.from_dict(d)
    assert report.products == ["Fenix"]
    assert report.tags == ["spam", "eggs"]
    assert report.artifacts == []
