import os

import click

from release_exporter.exceptions import UnknownRepo
from release_exporter.formatter import github
from release_exporter.formatter import gitlab
from release_exporter.utils import get_repo_url_info


@click.group()
@click.option('--repo', help='Your repository name.')
@click.option('--token', help='Token number if its a private repository.', default=None)
@click.option('--tags', help='Range of tags.', default='all')
@click.option('--url',
              help="URL of your repository. This is optional if your current directory has .git folder with remote url.",
              default=None)
@click.option('--location', help='Local location of your repository.', default=os.getcwd())
@click.pass_context
def cli(ctx, repo, token, tags, url, location):
    ctx.obj['repo'] = repo
    ctx.obj['token'] = token
    ctx.obj['tags'] = tags
    ctx.obj['repo_url'] = url
    ctx.obj['location'] = location


# TODO: Implement init as a go to token area.
# @cli.command(help='Creates .rex file.')
# def init():
#     pass


@cli.command(help='Creates markdown file.')
@click.pass_context
def markdown(ctx):

    if os.name == 'nt':
        ctx.obj['location'] = r'{}'.format(ctx.obj['location'])

    if "github" in get_repo_url_info(location=ctx.obj['location'], repo_url=ctx.obj['repo_url']).resource:
        print('GitHub detected. \n')

        github(force=True, token=ctx.obj['token'], location=ctx.obj['location'], repo_url=ctx.obj['repo_url'],
               file_type='markdown').write_markdown()

    elif "gitlab" in get_repo_url_info(location=ctx.obj['location'], repo_url=ctx.obj['repo_url']).resource:
        print('GitLab detected. \n')

        gitlab(force=True, token=ctx.obj['token'], location=ctx.obj['location'], repo_url=ctx.obj['repo_url'],
               file_type='markdown').write_markdown()

    else:
        raise UnknownRepo("Sorry, couldn't find the repository. Trying giving the repository URL by adding --url flag.")


@cli.command(help='Creates JSON file.')
@click.pass_context
def json(ctx):
    if os.name == 'nt':
        ctx.obj['location'] = r'{}'.format(ctx.obj['location'])

    if "github" in get_repo_url_info(location=ctx.obj['location'], repo_url=ctx.obj['repo_url']).resource:
        print('GitHub detected. \n')

        github(force=True, token=ctx.obj['token'], location=ctx.obj['location'], repo_url=ctx.obj['repo_url'],
               file_type='json').write_json()

    elif "gitlab" in get_repo_url_info(location=ctx.obj['location'], repo_url=ctx.obj['repo_url']).resource:
        print('GitLab detected. \n')

        gitlab(force=True, token=ctx.obj['token'], location=ctx.obj['location'], repo_url=ctx.obj['repo_url'],
               file_type='json').write_json()

    else:
        raise UnknownRepo("Sorry, couldn't find the repository. Trying giving the repository URL by adding --url flag.")
