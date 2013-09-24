# :coding: utf-8
# :copyright: Copyright (c) 2013 Martin Pengelly-Phillips
# :license: See LICENSE.txt.

import re
from collections import defaultdict

from ._version import __version__
from .collection import Collection
from .error import CollectionError


#: Pattern for matching an index with optional padding.
DIGITS_PATTERN = '(?P<index>(?P<padding>0*)\d+)'

_DIGITS_REGEX = re.compile(DIGITS_PATTERN)

#: Common patterns that can be passed to :py:func:`~clique.assemble`.
PATTERNS = {
    'frames': '\.{0}\.\D+\d?$'.format(DIGITS_PATTERN),
    'versions': 'v{0}'.format(DIGITS_PATTERN)
}


def assemble(iterable, patterns=None, minimum_items=2):
    '''Assemble items in *iterable* into discreet collections.

    *patterns* may be specified as a list of regular expressions to limit
    the returned collection possibilities. Use this when interested in
    collections that only match specific patterns. Each pattern must contain
    the expression from :py:data:`DIGITS_PATTERN` exactly once.

    A selection of common expressions are available in :py:data:`PATTERNS`.

    .. note::

        If a pattern is supplied as a string it will be automatically compiled
        to a :py:class:`re.RegexObject` instance for convenience.

    When *patterns* is not specified, collections are formed by examining all
    possible groupings of the items in *iterable* based around common numerical
    components.

    *minimum_items* dictates the minimum number of items a collection must have
    in order to be included in the result. The default is 2, filtering out
    single item collections.

    Return list of assembled :py:class:`~clique.collection.Collection`
    instances.

    '''
    collection_map = defaultdict(set)
    collections = []

    # Compile patterns.
    compiled_patterns = []

    if patterns is not None:
        if not patterns:
            return collections

        for pattern in patterns:
            if isinstance(pattern, basestring):
                compiled_patterns.append(re.compile(pattern))
            else:
                compiled_patterns.append(pattern)

    else:
        compiled_patterns.append(_DIGITS_REGEX)

    # Process iterable.
    for item in iterable:
        for pattern in compiled_patterns:
            for match in pattern.finditer(item):
                index = match.group('index')

                head = item[:match.start('index')]
                tail = item[match.end('index'):]

                padding = match.group('padding')
                if padding:
                    padding = len(index)
                else:
                    padding = 0

                key = (head, tail, padding)
                collection_map[key].add(int(index))

    # Form collections.
    merge_candidates = []
    for (head, tail, padding), indexes in collection_map.items():
            collection = Collection(head, tail, padding, indexes)
            collections.append(collection)

            if collection.padding == 0:
                merge_candidates.append(collection)

    # Merge together collections that align on padding boundaries. For example,
    # 0998-0999 and 1000-1001 can be merged into 0998-1001. Note that only
    # indexes within the padding width limit are merged. If a collection is
    # entirely merged into another then it will not be included as a separate
    # collection in the results.
    fully_merged = []
    for collection in collections:
        if collection.padding == 0:
            continue

        for candidate in merge_candidates:
            if (candidate.head == collection.head and
                candidate.tail == collection.tail):

                merged_index_count = 0
                for index in candidate.indexes:
                    if len(str(abs(index))) == collection.padding:
                        collection.indexes.add(index)
                        merged_index_count += 1

                if merged_index_count == len(candidate.indexes):
                    fully_merged.append(candidate)

    # Filter out fully merged collections.
    collections = [collection for collection in collections
                   if collection not in fully_merged]

    # Filter out collections that do not have at least as many indexes as
    # minimum_items
    collections = [collection for collection in collections
                   if len(collection.indexes) >= minimum_items]

    return collections

