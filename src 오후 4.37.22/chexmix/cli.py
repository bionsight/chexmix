"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mchexmix` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``chexmix.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``chexmix.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import logging

import click

logging.basicConfig(format='[%(process)d] %(levelname)s: %(message)s', level=logging.INFO)


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)


@cli.command()
@click.pass_context
@click.argument('target', type=click.STRING)
def do_something(ctx):
    click.echo('Doing something...')


def main():
    cli(obj={})
