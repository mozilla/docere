import click
from .render import main


@click.group()
def cli():
    pass


@cli.command()
@click.option('--knowledge-repo', default='kr', help='Path to knowledge repo')
@click.option(
    '--external-reports',
    default='external',
    help="Path within the KR that holds external report definitions"
)
@click.option('--outdir', default='output',
              help='Desired path for rendered documentation')
def render(knowledge_repo, external_reports, outdir):
    main(knowledge_repo, external_reports, outdir)


if __name__ == "__main__":
    cli()
