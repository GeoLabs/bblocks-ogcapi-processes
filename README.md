# OGC API Processes Building Blocks

This repository hosts the definitions for **both editions** of OGC API - Processes
Part 1: Core, in one GeoLabs register, for reuse and contribution.

## Part and version separation (2026-11-09)

| Edition | Sources | Identifier namespace | Blocks |
| --- | --- | --- | --- |
| [Part 1 version 1.0, OGC 18-062r2](https://docs.ogc.org/is/18-062r2/18-062r2.html) | [_sources/part1/v1](_sources/part1/v1) | `ogc.api.processes.part1.v1.*` | 73 |
| [Part 1 version 2.0 draft, OGC 18-062r3](https://docs.ogc.org/DRAFTS/18-062r3.html) | [_sources/part1/v2](_sources/part1/v2) | `ogc.api.processes.part1.v2.*` | 102 |

Both trees retain independent metadata, contexts and example resources. Schema
and OpenAPI components **embed official definitions in readable, space-indented
YAML**, not reference-only wrappers or copies of the other edition. References
to represented components use same-edition building block identifiers. Other
official resources remain absolute external URLs.
The single register at
<https://geolabs.github.io/bblocks-ogcapi-processes/build/register.json>
contains 175 source blocks. Its `identifier-prefix` is `ogc.api.processes.`;
the source paths supply the independent part and edition segments.

The original Part 1 version 1.0 register remains
<https://ogcincubator.github.io/bblocks-ogcapi-processes/build/register.json>
with its historical `ogc.api.processes.v1.*` identifiers. This fork creates no
aliases in that historical namespace. Block `version` fields describe the
standard editions: every Part 1 v1 block has `version: "1.0"`, and every Part 1
v2 block has `version: "2.0"`. This metadata convention does not change the
embedded OpenAPI `info.version`. Dependency labels omit decorative trailing
`parameter`, `path`, `response` and `schema` words and the `Schema for ` prefix;
discovered `Official ...` labels use the leaf identifier, retaining prefixes
such as `rAPI` and meaningful names such as `schema`, `response` and `Dismiss Job`.

### Official source alignment (2026-11-09)

The original metadata/context import came from
[ogcincubator commit ca0b1523344dfe56ad1de9b285d63c56a432f341](https://github.com/ogcincubator/bblocks-ogcapi-processes/tree/ca0b1523344dfe56ad1de9b285d63c56a432f341/_sources/v1).
Its schema definitions are no longer treated as authoritative copies:

- **v1:** definitions from the published
	<https://schemas.opengis.net/ogcapi/processes/part1/1.0/openapi/> resources.
- **v2:** raw official repository resources pinned to
	[0f9c3d88ccdb1802f6356fd39e7963df7b8dadae](https://github.com/opengeospatial/ogcapi-processes/tree/0f9c3d88ccdb1802f6356fd39e7963df7b8dadae/openapi),
	not moving `master` URLs. The v2 API is a Part 1-only composition of that
	multi-part API's path components, not a byte-identical complete upstream API.

[scripts/align_official_sources.py](scripts/align_official_sources.py) plans embedded
documents from the explicit mapping in
[scripts/audit_official_sources.py](scripts/audit_official_sources.py).
It is read-only unless `--write` is specified; `--patch` emits reviewable changes.
Schemas use local schema artifacts; parameters, responses, operations and paths
use local OpenAPI artifacts. Metadata no longer bypasses the embedded schemas.
No official constraint is silently fixed or relaxed. Recognized local JSON-LD
annotations at schema positions and existing ancillary files are preserved. Both `$ref` and
`externalValue` are resolved against their original official document URL;
external examples stay absolute URLs, never building block references.

For standalone schema documents only, the producer adds the minimal root
`$schema: http://json-schema.org/draft-04/schema#` declaration when the official
document omits a dialect and contains an actual boolean `exclusiveMinimum` or
`exclusiveMaximum` bound. Scanning all 175 artifacts identifies three documents:
v1 `schemas/schema`, v1 `schemas/swagger/schema`, and the legacy-v1-only v2
`schemas/swagger/schema`. The current v2 Core schemas are not marked Draft4;
existing official dialect declarations are never overwritten. All official
constraints, including `minimum: 0` plus `exclusiveMinimum: true`, remain intact.
This is a local dialect annotation, not an upstream constraint correction.
For standalone schemas, the parsed official content is preserved except for
reference normalization, this conditional declaration and local JSON-LD
annotations; YAML formatting is not byte-identical upstream content. The
independent audit requires exactly the eligible declaration and still rejects
removed or changed constraints, other dialects and nested dialect additions.

The 175-block inventory classifies 152 official components, four operation views
(Job GET and DismissJob DELETE), four external common resources, seven compatibility
aliases, one Part 1 API composition, and seven **legacy-v1-only** compatibility
components. These seven v2-namespace blocks are `transmissionMode`, the four
`schemas/swagger/*` components, `responses/swagger/ProcessDescription`, and
`responses/NotSupported`; their v1 provenance is explicit, not a v2 source claim.

v2 compatibility schema names map as follows: `binaryInputValue` → `binaryValue`,
`inlineOrRefData` → `inlineOrRefValue`, `inputValue` → `value`,
`inputValueNoObject` → `valueNoObject`, `qualifiedInputValue` → `qualifiedValue`,
and `output` → `outputSelection`. Common-core names are also mapped explicitly.
Parameter aliases `jobId`, `processIdPathParam`, and `processIdQueryParam` point
to official `jobID`, `processID-path`, and `processID-query` respectively.

Attribution and terms remain those of the upstream OGC material: the API document
retains its **OGC license** notice and <http://www.ogc.org/legal/> link. The pinned
upstream tree has no standalone LICENSE file; this import does not invent a
replacement license or remove any source notice. Upstream response examples
referencing the absent shared `examples/json/ProcessDescription.json` retain their
official absolute target; no missing example is fabricated or downloaded as a
local replacement. URL normalization does not assert target availability.

### Validation and integration limits

The v2 definitions now expose the official richer input/output descriptions,
data classes, data access APIs, execution-unit requirements and collection values.
Both official editions require `links` in `processList`. Official duration
parameters differ: v1 `minDuration`/`maxDuration` are arrays; v2 are integers.
The audit tests integer, array and string inputs for all four parameters.

[scripts/build_official_sources.py](scripts/build_official_sources.py), used by
[build.sh](build.sh), adapts only PyYAML's YAML 1.1 interpretation of the bare
CQL2 `=` scalar to the intended string. Remote bytes, references and constraints
are unchanged. This is a parser integration adapter, not an upstream schema fix.
The inherited v2 reference-only input schema example violates the pinned official
subset requiring `type` and `properties`: a valid object example replaces it,
and its original form is retained in a negative regression fixture.

The source-only validation after embedding is described in
[scripts/README.md](scripts/README.md).
It parses all 175 artifacts, reverses reference normalization independently of
the producer, and verifies API graph reachability and edition isolation.
Regression tests include deliberately corrupted constraints, missing API paths,
cross-edition edges, relative external example URLs and dialect mutations.
All schema artifacts are checked against their selected metaschema, and each
boolean-bound document is independently checked with `Draft4Validator.check_schema`
and positive/zero/negative bound regression inputs. Reports from the source
audit are generated under `build-local/official-audit` (or `--output`).

Earlier wrapper-based builds passed **151/151 Part 1**, **17/17 Part 2** and
**52/52 standard** blocks. Those are historical results, not validation of the
175-block embedded tree. The embedded Part 1 tree was rebuilt on 2026-11-10:
**175/175 blocks pass**, with SPARQL uploads and template updates disabled.
The generated register exposes all nine path blocks as dependencies of each API;
the source graph reaches 52 blocks for v1 and 81 for v2. The local v1 viewer's
OpenAPI document and API dependency list were checked in the browser.
The downstream Part 2 and combined-standard builds have not been repeated for
this embedding change; their earlier results must not be presented as current.
Post-build integration checks belong to downstream validation workflows,
outside the scope of these Python scripts; this repository no longer provides
a cross-workspace integration launcher.
Successful source tests do not establish runtime or full-standard conformance.

### Python development and CI

Python **3.10 or later** is required. Install [requirements-dev.txt](requirements-dev.txt)
in a virtual environment. Tests use standard-library `unittest`, not pytest.
Run `python scripts/run_unit_tests.py` for offline tests: the runner creates an
empty temporary cache and denies HTTP/socket connections. Source integration
tests are skipped unless `OFFICIAL_SOURCE_TESTS=1` is set. Reproducible opt-in
commands and cache policy are in [scripts/README.md](scripts/README.md).

The audit compares a **cached snapshot** by default, fetching only cache misses;
it does not claim that mutable published v1/common endpoints are current.
Use `--refresh` to refetch each used URL once, or `--offline` to fail on cache
misses. `--output` controls every audit cache load, discovery and report.
The v2 commit stays pinned even during refresh; v1/common URLs remain mutable.

[.github/workflows/python-scripts.yml](.github/workflows/python-scripts.yml)
adds read-only offline tests on Python 3.10 and 3.14, including a scalar-adapter
regression. The inherited PR/publication workflows remain unchanged: they call
the stock processor, **not** the local YAML adapter. Inspection of the remote
reusable workflows on 2026-11-10 confirmed `before_postprocess` is a host-shell
hook, not a Python entry-point override for the processor container. Publication
compatibility with bare CQL2 `=` remains pending an upstream adapter or a separately
reviewed container integration. Offline test success does not resolve that gap.

### Publication

This is a breaking identifier and source-path migration. Publish this dual-edition
register first, then Part 2 v1 (which explicitly uses only `part1.v1`), then the
combined standard register (whose Part 1 requirements use `part1.v2`).
Until publication, the combined repository uses ignored local URL mappings and
read-only import mounts; Part 2 likewise maps this register's `build/` and root
URLs to its sibling's `build-local/` and source tree. Consumers outside those three repositories are not
automatically migrated. Local validation disables SPARQL uploads and template
updates; no commit or push is part of this migration.
