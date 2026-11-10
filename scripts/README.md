# Embedded official Part 1 sources

The source register has **175 blocks: 73 v1 and 102 v2**. Every block has one
readable block-style YAML artifact, with space indentation. Schemas are embedded
locally instead of bypassed by a metadata URL. Existing contexts, examples,
test fixtures and JSON-LD annotations remain local assets.

## Allowed transformations

1. Copy the official object from the published v1 endpoint or the pinned v2
   commit `0f9c3d88ccdb1802f6356fd39e7963df7b8dadae`.
2. Resolve references against that original URL. Route represented components
   to `bblocks://ogc.api.processes.part1.<edition>.*` in the same edition;
  retain other references as absolute official URLs. Represented self references
  also use the canonical `bblocks://` identifier, never local `#`: the annotator
  descends local cycles before marking them visited. Preserve each JSON pointer
  relative to the represented source, including extracted source subtrees;
  references outside a subtree must not lose their document-level pointer.
  Compatibility aliases do not displace canonical names.
3. Make every relative OpenAPI `externalValue` an absolute official URL,
   without converting it into a building block reference. Missing upstream
   examples are not fabricated; their availability is not a source-equality test.
4. Project the multipart v2 root onto the Part 1 paths, including `/api`, while
   preserving upstream API information, license notices, servers and definitions.
   Drop unused multipart components. Keep the Job GET and DELETE views separate
   and expose both operations from the API without JSON Schema `allOf` on paths.
5. Preserve recognized local JSON-LD annotations at schema keyword positions.
   The exact allowlist is in [schema_annotations.py](schema_annotations.py).
   Named properties/components and instance data are never annotations just
   because their names begin with `x-jsonld`. Unknown keys are compared normally.
   Do not repair upstream constraints, defaults, spelling or example content.
6. On standalone schema documents only, declare Draft4 at the root if upstream
   omits `$schema` and a schema position contains a boolean `exclusiveMinimum`
   or `exclusiveMaximum`. Preserve the bound and every other constraint exactly.
   This currently affects v1 `schemas/schema`, v1 `schemas/swagger/schema` and
   legacy-v1-only v2 `schemas/swagger/schema`, not the current v2 Core schemas.
   An existing official dialect is never replaced.

Seven v2-namespace compatibility blocks still have **legacy-v1-only** provenance.
Their external v1 resource URLs are deliberate; they never reference v1 building
block identifiers. This is namespace isolation, not a claim that legacy content
became part of official v2.

## Producer and independent verification

- [official_materializer.py](official_materializer.py)
  discovers reachable v2 Core operations and grouped schemas/parameters/responses,
  and renders `yaml.safe_dump` block YAML. Discovery is closed when a subsequent
  inventory finds the same identifiers and source URLs.
- [align_official_sources.py](align_official_sources.py)
  is a read-only planner by default. `--patch` produces reviewable changes;
  `--write` is an explicit regeneration mode, not part of validation.
- [check_embedded_sources.py](check_embedded_sources.py)
  compares local artifacts with upstream content using separate transformation
  logic. It shares the explicit source map, HTTP loader and annotation-position
  rules with the producer; this is not fully independent source discovery.
  It does **not** call
  the producer's `embedded`, `rewrite` or `official_document`. It reverses local
  references to original URLs, expands Path Item/Operation references separately,
  applies its own declared API projection, and compares full parsed objects
  except for local JSON-LD annotations and the independently determined minimal
  root Draft4 declaration above. No schema keywords or constraints are removed
  during normalization. Schemas are not dereferenced recursively.
- [validate_embedded_sources.py](validate_embedded_sources.py)
  also parses every schema/OpenAPI artifact (including orphan files), enforces a
  single mapping document, checks each standalone schema against its selected
  metaschema and checks the optional ancillary SHA-256 manifest.
- [test_official_materializer.py](test_official_materializer.py)
  contains source regressions and in-memory mutation tests. It checks actual
  local duration parameter types and the required `processList.links` property.
  It scans every artifact for boolean bounds, independently checks affected
  documents with `Draft4Validator.check_schema`, exercises the exclusive bound,
  and rejects lost constraints or unjustified/changed dialect declarations.

## Reproducible checks (Python >=3.10)

Python >=3.10 and [../requirements-dev.txt](../requirements-dev.txt) are required.
Run all commands from the repository root, in that Python environment.

Offline unit tests use [run_unit_tests.py](run_unit_tests.py), which creates an
empty temporary cache, denies HTTP/socket connections and skips source integration
tests regardless of the caller's `OFFICIAL_SOURCE_TESTS` setting:

```sh
python scripts/run_unit_tests.py
```

To opt into source integration tests, first populate a dedicated cache with the
audit, then reuse it without network access for validation and tests:

```sh
export OFFICIAL_SOURCE_OUTPUT="$(mktemp -d)"
python scripts/audit_official_sources.py --output "$OFFICIAL_SOURCE_OUTPUT" --refresh
export OFFICIAL_SOURCE_OFFLINE=1
python scripts/validate_embedded_sources.py
OFFICIAL_SOURCE_TESTS=1 python -m unittest discover -s scripts -p 'test_*.py' -v
```

Retain the selected cache to reproduce the same snapshot. To check a retained
cache without refreshing it, run the audit with `--output` pointing to that
directory and `--offline` instead of `--refresh`. Use actual runner output to
distinguish executed regressions from skipped source tests; no fixed test total
is asserted here.

The audit CLI's `--output` selects the shared cache and report for every load.
Default mode checks cached snapshots, not the current state of mutable upstream
URLs. `--refresh` refetches each used URL once and does not fall back on HTTP
failure; `--offline` forbids cache misses. v2 stays pinned to its commit in all
modes. v1/common endpoints are mutable; retain their cache for reproducibility.

Annotation parsing is strict: one YAML mapping, no malformed JSON+YAML recovery
and no tab expansion. Annotated lists must match structurally after reference
mapping, otherwise regeneration fails with a reconciliation message. Removed
or retyped annotated structures also fail rather than lose their annotations.

The ancillary manifest is a migration-time external baseline, not a file
regenerated by the validation. Without it, source equality and graph checks still
run, but byte preservation cannot be asserted. `--closure` on the audit optionally
checks all transitive official references/pointers; it does not fetch external
example payloads. HTTP cache and audit reports may be written outside source files.

Each API must directly reach all nine historical path blocks, then reach
responses and schemas from each path and parameters at API level. Both Job
methods and the newly discovered operation blocks are covered. Cross-edition,
unresolved and invalid-pointer building block edges fail validation.

## Validation scope

Source checks validate embedded artifacts and dependency graphs, not runtime or
full-standard conformance. Post-build and downstream integration checks remain
separate; historical build results do not validate a changed source tree.

Standalone Python CI tests the adapter without publication. The inherited
PR/publication workflows still use the stock processor, not the local adapter;
the remote host `before_postprocess` hook is not a container entry-point
override. Bare CQL2 `=` compatibility there remains pending upstream support
or a separately reviewed container integration. See the
[main README](../README.md#python-development-and-ci) for CI and publication limits.