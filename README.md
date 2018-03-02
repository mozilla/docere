# Introduction

Docere is a workflow and set of tools for publishing data analyses.

Docere sounds like "dose air"

# Design Principles

* Analysts should have total control of their report presentation
* Analysts should be able to get their work reviewed
* Tools should be simple and do one thing well
* Changes to reports should be tracked,
  but reproducibility is the responsibility of the analyst (not the tool)

# High Level Workflow

## Generate a report

Docere starts with a `report` representing an analysis or a unit of knowledge.
An analyst can generate their report using any tools they like.
The only requirement is that their analysis result in a static HTML document.

## Submit report to a knowledge-repo

All reports are stored in a central git repository, called the `knowledge repository`.
To submit a new report,
open a pull request against the knowledge repository.
Store your report as an `index.html` file in an appropriately named directory.

Add a `report.json` file next to the `index.html` file so docere knows it's a report.
The `report.json` file is technically optional.
Docere will still include your report in the rendered documentation.
However, your report will not be included in any of the metadata pages
so your report will be difficult to find.

At a minimum, your `report.json` file should include the following fields:

* `title`: The title of the report
* `publish_date`: YYYY-MM-DD format
* `author`: The author's name

If desired, this is the time to get review for your analysis.

## Render content

You should configure CI to trigger docere when PRs are merged to master.
Docere will then:

* Copy the knowledge-repo to a new directory named `output`
* Gather metadata for all known reports
* Pass the metadata to the `metadata generators` to create the necessary `metadata pages`

`Metadata pages` are auto-generated documents produced to make reports more discoverable.
For example, docere will generate a homepage that lists all reports in anti-chronological order.
Other `metadata pages` could include: RSS feeds, topic pages, or reports by a specific contributor.

I intend most `metadata generators` be implemented as plugins to this system.
For now, I'm including some very simple `metadata generators` by default.

## Upload content

Docere does not handle uploading the rendered site to a server.
We recommend configuring this through your CI provider.
We've included an example `.travis.yml` in this repository.
You can view the rendered documentation 
[here](http://docere-test.s3-website-us-east-1.amazonaws.com/).

# Advantages and Weaknesses

## HTML is difficult to review in GitHub

A docere `knowledge repository` stores raw HTML files.
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
* Implement the upload-to-S3 tooling (done! Use travis)
* Add CI for automatically deploying the static site (done! see .travis.yml)
* Add tooling for a metadata page with a report index (done!)
* Spec out report-level metadata (done!)
* Add access control to the S3 bucket 
  (See: [Bug 1439982](https://bugzilla.mozilla.org/show_bug.cgi?id=1439982))


# Appendix

## FAQ 

### Another static site generator?

_Why_ are you building _another_ static site generator, Ryan?
Why!

I just couldn't find any other static site generator
that let's the analyst have total control over the report.
Docere, on the other hand, just aggregates reports.
It **doesn't render them**.

For example, checkout
[this prototype using pelican](https://github.com/harterrt/dpel).
We're storing HTML files,
but everything is squeezed into the default pelican theme.
I decided it would take more work to build a minimal template for pelican
than to just start over.

### Why use `report.json` config files?

Many static site generators prefer using front-matter to store metadata.
In my experience adding front-matter to a report is an unnecessary pain.

If you already have a working toolchain for creating reports,
modifying your templates to include front-matter is frustrating.
It's much easier to compose these toolchains if you use an external config file.

For example, you could create a simple bash script that
starts a branch in the knowledge-repo,
copies your report to the knowledge-repo,
and copies a boilerplate `report.json` config to the right directory.
Now imagine if that config needed to reside inside the HTML file.

### Buy why JSON? Why not YAML or INI?

For docere's purposes, these formats are very similar.

The `report.json` files get copied to the rendered directory as well.
I expect it will be useful to reference the report.html file for a given report. 
Browsers generally understand what a JSON file is
and do a good job of displaying the contents.
This is not true of YAML or INI

I also had some trouble with PyYAML when testing across different versions of Python.


[knowledge-repo]: https://github.com/airbnb/knowledge-repo
