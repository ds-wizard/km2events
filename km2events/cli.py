import configparser
import json
import os
import sys
import uuid

import click

from km2events.core_loader import CoreLoader
from km2events.events import EventsBuilder
from km2events.exceptions import KM2EventsError


def _load_chapter_from_file(loader, root, chapter_file):
    chapter_path = os.path.join(root, chapter_file)
    with open(chapter_path) as f:
        loader.add_chapter(json.load(f))


@click.command()
@click.version_option(version='0.1', prog_name='DS KM-to-Events transformer')
@click.argument('km-root', type=click.Path(exists=True, readable=True,
                                           dir_okay=True, file_okay=False))
@click.option('-c', '--config-file', help='Config file', type=click.File('r'),
              default='./config.ini')
@click.option('-b', '--bsonic', help='Produce Haskellish BSON', is_flag=True)
def cli(km_root, config_file, bsonic):
    config = configparser.ConfigParser()
    config.read_file(config_file)

    root = os.path.join(km_root, 'core')
    package_path = os.path.join(root, 'package.json')
    with open(package_path) as f:
        loader = CoreLoader.create_from_package(json.load(f))
    try:
        for chapter_file in loader.km.chapterFiles:
            _load_chapter_from_file(loader, root, chapter_file)
    except KM2EventsError as e:
        click.secho(e.message, fg='red')
        sys.exit(e.return_code)

    eb = EventsBuilder()
    eb.add_km(loader.km)

    package = eb.make_package(
        name=config.get('package', 'name', fallback=loader.km.name),
        version=config.get('package', 'version', fallback='1.0.0'),
        kmId=config.get('package', 'kmId'),
        organizationId=config.get('package', 'organizationId'),
        parentPackageId=config.get('package', 'parentPackageId', fallback=None),
        description=config.get('package', 'description', fallback=loader.km.description)
    )

    out = json.dumps(package, indent=4)
    if bsonic:
        out = out.replace('{', '[').replace('}', ']')
        out = out.replace(': ', ' BSON.=: ')
    print(out)
