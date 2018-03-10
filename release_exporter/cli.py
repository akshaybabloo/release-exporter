import os

import click

from release_exporter.exceptions import UnknownRepo
from release_exporter.formatter import github
from release_exporter.formatter import gitlab
from release_exporter.utils import get_repo_url_info
from release_exporter.version import __version__


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(__version__)
    ctx.exit()


@click.group()
@click.option('--token', help='Token number if its a private repository.', default=None)
@click.option('--url',
              help="URL of your repository. This is optional if your current directory has .git folder with remote url.",
              default=None)
@click.option('--location', help='Local location of your repository.', default=os.getcwd())
@click.option('--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True)
@click.pass_context
def cli(ctx, token, url, location):
    ctx.obj['token'] = token
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
               file_type='markdown').write()

    elif "gitlab" in get_repo_url_info(location=ctx.obj['location'], repo_url=ctx.obj['repo_url']).resource:
        print('GitLab detected. \n')

        gitlab(force=True, token=ctx.obj['token'], location=ctx.obj['location'], repo_url=ctx.obj['repo_url'],
               file_type='markdown').write()

    else:
        raise UnknownRepo("Sorry, couldn't find the repository. Trying giving the repository URL by adding --url flag.")


@cli.command(help='Creates JSON file.')
@click.pass_context
def json(ctx):
    if os.name == 'nt':
        ctx.obj['location'] = r'{}'.format(ctx.obj['location'])

    if "github" in get_repo_url_info(location=ctx.obj['location'], repo_url=ctx.obj['repo_url']).resource:
        click.echo('GitHub detected. \n')

        github(force=True, token=ctx.obj['token'], location=ctx.obj['location'], repo_url=ctx.obj['repo_url'],
               file_type='json').write()

    elif "gitlab" in get_repo_url_info(location=ctx.obj['location'], repo_url=ctx.obj['repo_url']).resource:
        click.echo('GitLab detected. \n')

        gitlab(force=True, token=ctx.obj['token'], location=ctx.obj['location'], repo_url=ctx.obj['repo_url'],
               file_type='json').write()

    else:
        raise UnknownRepo("Sorry, couldn't find the repository. Trying giving the repository URL by adding --url flag.")


@cli.command(help='Creates reStructuredText file. Coming soon.')
@click.pass_context
def rst(ctx):
    # if os.name == 'nt':
    #     ctx.obj['location'] = r'{}'.format(ctx.obj['location'])
    #
    # if "github" in get_repo_url_info(location=ctx.obj['location'], repo_url=ctx.obj['repo_url']).resource:
    #     click.echo('GitHub detected. \n')
    #
    #     github(force=True, token=ctx.obj['token'], location=ctx.obj['location'], repo_url=ctx.obj['repo_url'],
    #            file_type='rst').write()
    #
    # elif "gitlab" in get_repo_url_info(location=ctx.obj['location'], repo_url=ctx.obj['repo_url']).resource:
    #     click.echo('GitLab detected. \n')
    #
    #     gitlab(force=True, token=ctx.obj['token'], location=ctx.obj['location'], repo_url=ctx.obj['repo_url'],
    #            file_type='rst').write()
    #
    # else:
    #     raise UnknownRepo("Sorry, couldn't find the repository. Trying giving the repository URL by adding --url flag.")
    raise NotImplementedError("Coming soon.")


@cli.command('all', help='Creates change log for all formats.')
@click.pass_context
def all_format(ctx):
    if os.name == 'nt':
        ctx.obj['location'] = r'{}'.format(ctx.obj['location'])

    if "github" in get_repo_url_info(location=ctx.obj['location'], repo_url=ctx.obj['repo_url']).resource:
        # Creates for GitHub
        print("Creating change logs for GitHub.")
        github(force=True, token=ctx.obj['token'], location=ctx.obj['location'], repo_url=ctx.obj['repo_url'],
               file_type='json').write()
        github(force=True, token=ctx.obj['token'], location=ctx.obj['location'], repo_url=ctx.obj['repo_url'],
               file_type='markdown').write()
        # github(force=True, token=ctx.obj['token'], location=ctx.obj['location'], repo_url=ctx.obj['repo_url'],
        #        file_type='rst').write()
    else:
        # Creates for GitLab
        print("Creating change logs for GitLab.")
        gitlab(force=True, token=ctx.obj['token'], location=ctx.obj['location'], repo_url=ctx.obj['repo_url'],
               file_type='json').write()
        gitlab(force=True, token=ctx.obj['token'], location=ctx.obj['location'], repo_url=ctx.obj['repo_url'],
               file_type='markdown').write()
        # gitlab(force=True, token=ctx.obj['token'], location=ctx.obj['location'], repo_url=ctx.obj['repo_url'],
        #        file_type='rst').write()


def main():
    cli(obj={})
