#!/usr/bin/env python3
"""Read bundled original guidance. Exact filters, no ranking or network calls."""
import argparse
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / 'skills/social-media-engine/assets/design-patterns.json'


def retrieve(*, intent=None, format=None, pattern_id=None):
    document = json.loads(DATA.read_text(encoding='utf-8'))
    patterns = document['patterns']
    # Validate filters so a typo cannot silently broaden the result.
    for value, allowed, label in (
        (intent, {tag for p in patterns for tag in p['intents']}, 'intent'),
        (format, {tag for p in patterns for tag in p['formats']}, 'format'),
        (pattern_id, {p['id'] for p in patterns}, 'id'),
    ):
        if value is not None and value not in allowed:
            raise ValueError(f'Unknown {label}: {value}. Choose from: {", ".join(sorted(allowed))}')
    document['patterns'] = [p for p in patterns
        if (intent is None or intent in p['intents'])
        and (format is None or format in p['formats'])
        and (pattern_id is None or pattern_id == p['id'])]
    document['retrieval'] = {'method': 'exact intersection; original file order; not a suitability score',
                             'intent': intent, 'format': format, 'id': pattern_id,
                             'count': len(document['patterns'])}
    return document


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--intent')
    parser.add_argument('--format')
    parser.add_argument('--id', dest='pattern_id')
    args = parser.parse_args()
    try:
        result = retrieve(**vars(args))
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
