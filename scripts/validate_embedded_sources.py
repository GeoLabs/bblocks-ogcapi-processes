"""Validate source artifacts without Docker or generated registers.

Run with --ancillary-before /tmp/ospd-embedded-ancillary-before.json to check
the pre-migration hashes. No source, context, example or test is written.
The upstream HTTP cache may be populated by the audit loader.
"""
import argparse
import hashlib
import json
from pathlib import Path

import jsonschema
import yaml

from audit_official_sources import ROOT
from check_embedded_sources import check
from official_materializer import artifact, discover, inventory


def validate(ancillary_before=None):
    plans = inventory()
    errors, graphs = check(plans)
    represented = {p['id'] for p in plans}
    missing = {p['id'] for p in discover(plans)} - represented
    errors.extend({'block': ident, 'error': 'Missing reachable Core component'}
                  for ident in sorted(missing))
    expected = {artifact(p) for p in plans}
    actual = {f for name in ('schema.yaml', 'openapi.yaml')
              for f in (ROOT / '_sources/part1').rglob(name)}
    # Parse every artifact, including an orphan not represented by inventory.
    for target in sorted(actual):
        try:
            text = target.read_text()
            if '\t' in text:
                raise ValueError('Tab character in YAML artifact')
            documents = list(yaml.safe_load_all(text))
            if len(documents) != 1 or not isinstance(documents[0], dict):
                raise ValueError('Expected exactly one YAML mapping')
            if target.name == 'schema.yaml':
                schema = documents[0]
                jsonschema.validators.validator_for(schema).check_schema(schema)
            if target not in expected:
                raise ValueError('Artifact absent from block inventory')
        except (OSError, ValueError, yaml.YAMLError, jsonschema.SchemaError) as exc:
            errors.append({'file': str(target.relative_to(ROOT)), 'error': str(exc)})
    checked = 0
    if ancillary_before:
        baseline = json.loads(Path(ancillary_before).read_text())
        for relative, digest in baseline.items():
            target = ROOT / relative
            checked += 1
            if not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest() != digest:
                errors.append({'file': relative, 'error': 'Ancillary hash changed'})
        current = {str(f.relative_to(ROOT)) for f in (ROOT / '_sources/part1').rglob('*')
                   if f.is_file() and (f.name in ('context.jsonld', 'examples.yaml')
                                       or 'tests' in f.relative_to(ROOT).parts)}
        for relative in sorted(current - baseline.keys()):
            errors.append({'file': relative, 'error': 'New ancillary file absent from baseline'})
    return {'blocks': len(plans), 'artifacts_parsed': len(actual),
            'ancillary_hashes_checked': checked, 'api_graphs': graphs,
            'errors': errors, 'passed': not errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ancillary-before', type=Path)
    args = parser.parse_args()
    report = validate(args.ancillary_before)
    print(json.dumps(report, indent=2))
    raise SystemExit(not report['passed'])


if __name__ == '__main__':
    main()