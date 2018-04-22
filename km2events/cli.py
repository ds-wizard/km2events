import json
import os
import sys
import uuid

import click

from km2events.core_loader import CoreLoader
from km2events.events import EventsBuilder
from km2events.exceptions import KM2EventsError


def _get_chapter_files(root):
    return [
        os.path.join(root, filename) for filename in os.listdir(root)
        if os.path.isfile(os.path.join(root, filename)) and
           filename.startswith('chapter') and
           filename.endswith('.json')
    ]


def _load_chapter_from_file(loader, chapter_file):
    with open(chapter_file) as f:
        loader.add_chapter(json.load(f))


@click.command()
@click.version_option(version='0.1', prog_name='DS KM-to-Events transformer')
@click.argument('dskm-root', type=click.Path(exists=True, readable=True,
                                             dir_okay=True, file_okay=False))
# @click.option('-n', '--name', help='Name of Knowledge Model')
# @click.option('-u', '--uuid', help='UUID of Knowledge Model)
def cli(dskm_root):
    core_root = os.path.join(dskm_root, 'core')

    loader = CoreLoader(str(uuid.uuid4()), 'Testing km2events')

    try:
        for chapter_file in _get_chapter_files(core_root):
            _load_chapter_from_file(loader, chapter_file)
    except KM2EventsError as e:
        click.secho(e.message, fg='red')
        sys.exit(e.return_code)

    eb = EventsBuilder()
    eb.add_km(loader.km)
    print(json.dumps(eb.events, indent=4))
