import configparser
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
@click.option('-c', '--config-file', help='Config file', type=click.File('r'),
              default='./config.ini')
def cli(dskm_root, config_file):
    config = configparser.ConfigParser()
    config.read_file(config_file)

    loader = CoreLoader(
        config.get('km', 'uuid', fallback=str(uuid.uuid4())),
        config.get('km', 'name')
    )
    core_root = os.path.join(dskm_root, 'core')
    try:
        for chapter_file in _get_chapter_files(core_root):
            _load_chapter_from_file(loader, chapter_file)
    except KM2EventsError as e:
        click.secho(e.message, fg='red')
        sys.exit(e.return_code)

    eb = EventsBuilder()
    eb.add_km(loader.km)

    package = eb.make_package(
        name=config.get('package', 'name'),
        version=config.get('package', 'version', fallback='1.0.0'),
        artifactId=config.get('package', 'artifactId'),
        groupId=config.get('package', 'groupId'),
        parentPackageId=config.get('package', 'parentPackageId', fallback=None),
        description=config.get('package', 'description', fallback='')
    )
    print(json.dumps(package, indent=4))
