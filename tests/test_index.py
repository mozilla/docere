from .test_cli import isolated_knowledge_repo
from docere.render import _get_reports
from docere.plugins.index import build_index
import pytest


KR = 'tests/data/kr'
EARLY_DATE = "2018-01-01"
LATE_DATE = "2018-02-01"


@pytest.fixture
def reports():
    return(_get_reports(KR))


def get_report_order_with_date_change(reports, dates):
    """After changing publish_dates, return index of each report in index.html

    This function is used to verify the index generator is showing reports in
    anti-chronological order. This function changes the `publish_date`s of
    the `reports`, renders and index page, and returns the index of each
    reports `title` in the resulting `index.html` file.
    """
    with isolated_knowledge_repo(KR, 'kr'):
        reports[0]['publish_date'] = dates[0]
        reports[1]['publish_date'] = dates[1]

        build_index(reports)

        with open('index.html', 'r') as infile:
            contents = infile.read()

    return [
        contents.index(reports[0]['title']),
        contents.index(reports[1]['title'])
    ]


def test_index_ordered(reports):
    """If reports are in antichronological order, no change to order"""
    order = get_report_order_with_date_change(reports, [LATE_DATE, EARLY_DATE])

    assert order[0] < order[1]


def test_index_reversed(reports):
    """Reverse reports if in chronological order"""
    order = get_report_order_with_date_change(reports, [EARLY_DATE, LATE_DATE])

    assert order[1] < order[0]
