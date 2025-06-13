#!/usr/bin/env python3
import glob
import sys
from argparse import ArgumentParser

import mwxml
import mwparserfromhell
from mwparserfromhell.nodes.external_link import ExternalLink
from mwparserfromhell.nodes.tag import Tag


def external_links(path, namespace_names):
    dump = mwxml.Dump.from_file(path)
    namespace_ids = [
        namespace.id
        for namespace in dump.site_info.namespaces
        if namespace_names is None or namespace.name in namespace_names
    ]
    all_urls = set()
    for page in dump:
        for revision in page:
            if page.namespace in namespace_ids and revision.text is not None:
                wikicode = mwparserfromhell.parse(revision.text)
                for n in wikicode.ifilter(recursive=True):
                    if isinstance(n, ExternalLink):
                        url = n.url.strip_code()
                        if url not in all_urls:
                            print(url)
                            all_urls.add(url)
                    elif isinstance(n, Tag):
                        if n.tag.strip_code() == 'a':
                            for attr in n.attributes:
                                if attr.name.strip_code() == 'href':
                                    url = attr.value.strip_code()
                                    if url not in all_urls:
                                        print(url)
                                        all_urls.add(url)


def print_pages(path, namespace_names):
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
                the_text = ' '.join(t.value for t in wikicode.filter_text())


def create_parser():
    parser = ArgumentParser(prog=sys.argv[0])
    parser.add_argument('operation', metavar='OPERATION',
                        choices=['links', 'pages', 'ingest'])
    parser.add_argument('path', metavar='PATH',
                        help='Path to the dump file')
    parser.add_argument('--namespace', '-n', metavar='NAMES', nargs='*',
                        help='Give one or more namespace names')
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    if args.operation == 'links':
        external_links(args.path, args.namespace)
    elif args.operation == 'pages':
        print_pages(args.path, args.namespace)
    else:
        print_pages(args.path, args.namespace)


if __name__ == '__main__':
    main()

