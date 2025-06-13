#!/usr/bin/env python3
import glob
import sys
from argparse import ArgumentParser

import mwxml
import mwparserfromhell


def ingest(path, namespace_names):
    dump = mwxml.Dump.from_file(path)
    namespace_ids = [
        namespace.id
        for namespace in dump.site_info.namespaces
        if namespace_names is None or namespace.name in namespace_names
    ]
    for page in dump:
        for revision in page:
            if page.namespace in namespace_ids and revision.text is not None:
                print(f'Page(id: {page.id}, "{page.title}")')
                wikicode = mwparserfromhell.parse(revision.text)
                import pdb
                pdb.set_trace()


def create_parser():
    parser = ArgumentParser(prog=sys.argv[0])
    parser.add_argument('path', metavar='PATH',
                        help='Path to the dump file')
    parser.add_argument('--namespace', '-n', metavar='NAMES', nargs='*',
                        help='Give one or more namespace names')
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    ingest(args.path, args.namespace)


if __name__ == '__main__':
    main()

