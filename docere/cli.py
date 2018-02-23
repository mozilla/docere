import click
from .render import main


@click.group()
def cli():
    pass

@cli.command()
@click.option('--knowledge-repo', default='kr', help='Path to knowledge repo')
@click.option('--outdir', default='output',
              help='Desired path for rendered documentation')
def render(knowledge_repo, outdir):
    main(knowledge_repo, outdir)
