import os

import click

from release_exporter.exceptions import UnknownRepo
from release_exporter.formatter import github
from release_exporter.formatter import gitlab


@click.group()
@click.option('--provider', help='github or gitlab.')
@click.option('--repo', help='Your repository name.')
@click.option('--token', help='Token number if its a private repository.', default=None)
@click.option('--tags', help='Range of tags.', default='all')
@click.option('--url',
              help="URL of your repository. This is optional if your current directory has .git folder with remote url.")
@click.option('--location', help='Where do you want to save your file.', default=os.getcwd())
@click.pass_context
def cli(ctx, provider, repo, token, tags, url, location):
    ctx.obj['provider'] = provider
    ctx.obj['repo'] = repo
    ctx.obj['token'] = token
    ctx.obj['tags'] = tags
    ctx.obj['repo_url'] = url
    ctx.obj['location'] = location


@cli.command(help='Creates .rex file.')
def init():
    pass


@cli.command(help='Creates markdown file.')
@click.pass_context
def markdown(ctx):
    github_format(force=True, token="c7933996ed553368b1928d1d1c4d78a5c850675f", location=ctx.obj['location'], url='github.com:akshaybabloo/gollahalli-com').process()
    if "github" in get_repo_url_info(location=ctx.obj['location'], repo_url=ctx.obj['repo_url']).resource:
    elif "gitlab" in get_repo_url_info(location=ctx.obj['location'], repo_url=ctx.obj['repo_url']).resource:
    else:
        raise UnknownRepo("Sorry, couldn't find the repository. Trying giving the repository URL by adding --url flag.")


@cli.command(help='Creates JSON file.')
@click.pass_context
def json(ctx):
    pass
    if "github" in get_repo_url_info(location=ctx.obj['location'], repo_url=ctx.obj['repo_url']).resource:

        pass

    elif "gitlab" in get_repo_url_info(location=ctx.obj['location'], repo_url=ctx.obj['repo_url']).resource:

        pass

    else:
        raise UnknownRepo("Sorry, couldn't find the repository. Trying giving the repository URL by adding --url flag.")
