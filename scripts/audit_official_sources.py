"""Read-only audit of every Part 1 block against its declared official source.

Run with the development dependencies installed. Reports and HTTP cache use
build-local by default, or --output. No source or generator is rewritten.
"""
import argparse
import hashlib
import json
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urljoin

import jsonschema
import requests
import yaml
from official_source_loader import DEFAULT_OUTPUT, configure_cache, load

ROOT = Path(__file__).resolve().parents[1]
PIN = '0f9c3d88ccdb1802f6356fd39e7963df7b8dadae'
V1 = 'https://schemas.opengis.net/ogcapi/processes/part1/1.0/openapi/'
V2 = f'https://raw.githubusercontent.com/opengeospatial/ogcapi-processes/{PIN}/openapi/'
FEATURES = 'https://schemas.opengis.net/ogcapi/features/part1/1.0/openapi/schemas/'
OUT = DEFAULT_OUTPUT
PATHS = {'LandingPage': '/', 'Conformance': '/conformance',
         'ProcessList': '/processes', 'ProcessDescription': '/processes/{processID}',
         'Execution': '/processes/{processID}/execution', 'JobList': '/jobs',
         'Job': '/jobs/{jobId}', 'DismissJob': '/jobs/{jobId}',
         'JobResult': '/jobs/{jobId}/results'}
V2_PATHS = {'LandingPage': 'common-core/pLandingPage', 'Conformance': 'common-core/pConformance',
            'ProcessList': 'processes-core/pProcessList',
            'ProcessDescription': 'processes-core/pProcessDescription',
            'Execution': 'processes-core/pExecution', 'JobList': 'processes-core/pJobsList',
            'Job': 'processes-core/pJob', 'DismissJob': 'processes-core/pJob',
            'JobResult': 'processes-core/pJobResults'}
RENAMES = {'binaryInputValue': 'binaryValue', 'inlineOrRefData': 'inlineOrRefValue',
           'inputValue': 'value', 'inputValueNoObject': 'valueNoObject',
           'qualifiedInputValue': 'qualifiedValue', 'output': 'outputSelection'}
PARAMETERS = {'datetime': 'common-geodata/datetime', 'jobId': 'processes-core/jobID',
              'processIdPathParam': 'processes-core/processID-path',
              'processIdQueryParam': 'processes-core/processID-query'}
RESPONSES = {'ConformanceDeclaration': 'common-core/rConformance',
             'LandingPage': 'common-core/rLandingPage',
             **{n: f'common-core/r{n}' for n in ('InvalidParameter', 'NotAllowed', 'NotFound', 'ServerError')}}


def source_for(version, relative):
    """Explicit correspondence, not an assertion that legacy names still exist."""
    if version not in ('v1', 'v2'):
        raise ValueError(f'Unsupported edition: {version}')
    parts = relative.split('/')
    kind, name = parts[0], parts[-1]
    if version == 'v1':
        if kind == 'api':
            return V1 + 'ogcapi-processes-1.yaml', 'official'
        if kind == 'paths':
            pointer = PATHS[name].replace('~', '~0').replace('/', '~1')
            return V1 + 'ogcapi-processes-1.yaml#/paths/' + pointer, 'operation-view' if name in ('Job', 'DismissJob') else 'official'
        if relative == 'schemas/timeStamp':
            return FEATURES + 'timeStamp.yaml', 'external-common'
        if relative in ('schemas/common-core/confClasses', 'schemas/common-core/exception'):
            return FEATURES + name + '.yaml', 'external-common'
        if relative.startswith('schemas/common-core/'):
            return V1 + 'schemas/' + name + '.yaml', 'compatibility-alias'
        return V1 + relative + '.yaml', 'official'
    if kind == 'api':
        return V2 + 'ogcapi-processes.yaml', 'part1-composition'
    if kind == 'paths':
        return V2 + 'paths/' + V2_PATHS[name] + '.yaml', 'operation-view' if name in ('Job', 'DismissJob') else 'official'
    if kind == 'operations':
        return V2 + 'paths/processes-core/operations/' + name + '.yaml', 'official'
    if (kind in ('schemas', 'parameters', 'responses') and len(parts) == 3
            and parts[1] in ('common-core', 'common-geodata', 'processes-core', 'unspecified')):
        return V2 + relative + '.yaml', 'official'
    if kind == 'parameters':
        return V2 + 'parameters/' + PARAMETERS.get(name, 'processes-core/' + name) + '.yaml', 'official'
    if name == 'transmissionMode' or relative.startswith(('schemas/swagger/', 'responses/swagger/')) or relative == 'responses/NotSupported':
        return V1 + relative + '.yaml', 'legacy-v1-only'
    if kind == 'responses':
        return V2 + 'responses/' + RESPONSES.get(name, 'processes-core/r' + name) + '.yaml', 'official'
    if name in ('confClasses', 'exception', 'landingPage'):
        return V2 + 'schemas/common-core/' + name + '.yaml', 'compatibility-alias' if len(parts) > 2 else 'official'
    if name == 'timeStamp':
        return V2 + 'schemas/common-geodata/timeStamp.yaml', 'external-common'
    return V2 + 'schemas/processes-core/' + RENAMES.get(name, name) + '.yaml', 'compatibility-alias' if name in RENAMES else 'official'


def refs(value):
    if isinstance(value, dict):
        if isinstance(value.get('$ref'), str):
            yield value['$ref']
        for child in value.values():
            yield from refs(child)
    elif isinstance(value, list):
        for child in value:
            yield from refs(child)


def normalize(value, base, index):
    if isinstance(value, dict):
        return {key: (index.get(child, urljoin(base, child)) if key in ('$ref', 'externalValue') and isinstance(child, str)
                      else normalize(child, base, index)) for key, child in value.items()}
    if isinstance(value, list):
        return [normalize(child, base, index) for child in value]
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', type=Path, help='Read-only pre-change repository backup')
    parser.add_argument('--closure', action='store_true', help='Fetch every transitive reference (may expose upstream defects)')
    parser.add_argument('--output', type=Path, default=OUT,
                        help='Persistent audit directory (outside clean build outputs if desired)')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--refresh', action='store_true', help='Refetch every used URL once, including pinned v2')
    mode.add_argument('--offline', action='store_true', help='Use cached snapshots only; fail on a cache miss')
    args = parser.parse_args()
    configure_cache(args.output, refresh=args.refresh, offline=args.offline)
    args.output.mkdir(parents=True, exist_ok=True)
    # Import here to share the audited source map without import-time cycles.
    from check_embedded_sources import check as check_embedded
    from official_materializer import artifact, discover, inventory
    plans = inventory()
    missing = {p['id'] for p in discover(plans)} - {p['id'] for p in plans}
    for p in plans:
        p['artifact'] = str(artifact(p).relative_to(ROOT))
    index = {'bblocks://ogc.api.processes.part1.' + p['version'] + '.' + p['block'].replace('/', '.'): p['source'] for p in plans}
    errors, graphs = check_embedded(plans)
    errors.extend({'block': ident, 'error': 'Missing reachable official Core component'} for ident in sorted(missing))
    def check(p):
        try:
            official = load(p['source'])
            p['official_sha256'] = hashlib.sha256(json.dumps(official, sort_keys=True).encode()).hexdigest()
            if args.baseline:
                old = args.baseline / (p['artifact'] or '')
                if old.is_file():
                    original = yaml.safe_load(old.read_text())
                    p['baseline_equal_normalized_refs'] = normalize(original, p['source'], index) == normalize(official, p['source'], {})
        except (OSError, ValueError, TypeError, KeyError, yaml.YAMLError, requests.RequestException) as exc:
            errors.append({'block': p['version'] + '/' + p['block'], 'url': p['source'], 'error': str(exc)})
    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(check, plans))
    regressions = []
    for version, base in (('v1', V1), ('v2', V2)):
        for name in ('minDuration', 'maxDuration'):
            url = base + ('parameters/' if version == 'v1' else 'parameters/processes-core/') + name + '.yaml'
            parameter = load(url)
            schema = parameter['schema']
            validator = jsonschema.Draft7Validator(schema)
            expected_type = 'array' if version == 'v1' else 'integer'
            assert schema['type'] == expected_type, (url, schema)
            assert validator.is_valid([5]) == (version == 'v1')
            assert validator.is_valid(5) == (version == 'v2')
            assert not validator.is_valid('5')
            regressions.append({'version': version, 'parameter': name, 'official_type': expected_type,
                                'integer_pass': validator.is_valid(5), 'array_pass': validator.is_valid([5]), 'string_rejected': True})
    closure_errors = []
    visited = set()
    if args.closure:
        todo = {p['source'] for p in plans if p['classification'] != 'part1-composition'}
        while todo:
            batch, todo = todo - visited, set()
            visited.update(batch)
            def dependencies(url):
                try:
                    return {urljoin(url, ref) for ref in refs(load(url)) if not ref.startswith('bblocks://')}
                except (OSError, ValueError, TypeError, KeyError, yaml.YAMLError, requests.RequestException) as exc:
                    closure_errors.append({'url': url, 'error': str(exc)})
                    return set()
            with ThreadPoolExecutor(max_workers=8) as pool:
                for dependencies_set in pool.map(dependencies, batch):
                    todo.update(dependencies_set - visited)
    report = {'master_commit': PIN, 'cache_mode': 'refresh' if args.refresh else 'offline' if args.offline else 'snapshot',
              'mutable_upstream_current': args.refresh,
              'blocks': len(plans), 'versions': dict(Counter(p['version'] for p in plans)),
              'classifications': dict(Counter(p['classification'] for p in plans)),
              'baseline_comparison': dict(Counter(str(p.get('baseline_equal_normalized_refs')) for p in plans)),
              'errors': errors, 'api_graphs': graphs, 'duration_regressions': regressions,
              'transitive_resources': len(visited), 'upstream_reference_errors': closure_errors, 'items': plans}
    # Metadata paths are useful during checks but not JSON report values.
    for p in plans:
        p['metadata'] = str(p['metadata'].relative_to(ROOT))
    (args.output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'items'}, indent=2))
    raise SystemExit(bool(errors or closure_errors))


if __name__ == '__main__':
    main()