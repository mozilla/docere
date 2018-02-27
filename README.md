# Introduction

Docere is a workflow for publishing data analyses.

Docere sounds like "dose air"

# Design Principles

* Analysts should have total control of their report presentation
* Analysts should be able to get their work reviewed
* Tools should be simple and do one thing well
* Changes to reports should be tracked,
  but reproducibility is the responsibility of the analyst not the tool

# Workflow

Docere starts with a `report` representing an analysis or a unit of knowledge.
An analyst can generate their report using any tools they like.
The only requirement is that their analysis result in a static HTML document.

All reports are stored in a central git repository, called the `knowledge repository`.
To submit a new report,
an analyst should open a pull request against the knowledge repository.
The report should be stored as an `index.html` in an appropriately named directory.
If desired, this is the time to get review for the analysis.

When the PR is merged, a static site generator will:

* Gather all of the reports from the `knowledge repository`
* Generate the necessary `metadata pages`
* Upload the `reports` and `metadata pages` to a protected S3 bucket

`Metadata pages` are auto-generated documents produced to make reports more discoverable.
For example, Docere will generate a homepage that lists all reports in anti-chronological order.
Other `metadata pages` could include: RSS feeds, topic pages, or reports by a specific contributor.

# Advantages and Weaknesses

## HTML is difficult to review in GitHub

A Docere `knowledge repository` stores raw HTML files.
This gives the analyst complete control over the format of the report,
but comes with some notable disadvantages.

HTML diffs are often cluttered with boilerplate.
Even worse, GitHub doesn't allow you to review the rendered HTML page in your browser.
It would be much nicer if we could store markdown documents in the `knowledge repository`
and render these to HTML when generating the static site.
In fact, this is what AirBnB's [knowledge-repo] does.

We decided against storing markdown because it takes control away from the analyst.
Presenting data in a meaningful and compelling format is a difficult task.
Different reports need different formats.
It is **not this tool's job to be opinionated**.

## `reports` aren't inherently reproducible

This tool does not save any of the code used to generate a report.
Instead, **the analyst is responsible for making their results reproducible**.
This can be done by linking to a commit in a GitHub repository
or by including the code itself in the `report's` directory in the `knowledge repository`.

## Requires interacting with Git

Using Git to store `reports` makes it easy to get review and track changes.
However, some users will not be comfortable interacting with Git.
For now, these users are out of luck.

We may eventually explore a simpler front end,
but this is not current on our roadmap.
Docere is build to be composable,
so it should be easy to roll your own interface if you so desire!


# Roadmap

## 2018-Q1

* Scope out ideal workflow (done!)
* Implement the upload-to-S3 tooling
* Add CI for automatically deploying the static site
* Add access control to the S3 bucket
* Add tooling for a metadata page with a report index
* Spec out report-level metadata

[knowledge-repo]: https://github.com/airbnb/knowledge-repo

# Appendix

_Why_ are you building _another_ static site generator, Ryan?
Why!

I just couldn't find any other static site generator
that let's the analyst have total control over the report.
For example, checkout
[this prototype using pelican](https://github.com/harterrt/dpel).
We're storing HTML files,
but everything is squeezed into the default pelican theme.
I decided it would take more work to build a minimal template for pelican
than to just start over.
