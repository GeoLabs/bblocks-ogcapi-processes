"""Plan embedded official definitions, preserving metadata and ancillary files.

Default: read-only manifest. --patch emits an apply_patch-compatible patch;
--write explicitly regenerates artifacts. Contexts, examples, tests and other
repositories are never modified.
"""
import argparse
import difflib
import json
from pathlib import Path

from official_materializer import ROOT, discover, inventory, rendered_files


def patch_text(files):
    chunks = ['*** Begin Patch\n']
    for target, text in sorted(files.items()):
        if target.exists():
            old = target.read_text()
            if old == text:
                continue
            chunks.append(f'*** Update File: {target}\n')
            diff = list(difflib.unified_diff([line + '\n' for line in old.splitlines()],
                                           [line + '\n' for line in text.splitlines()], n=3))
            for line in diff[2:]:
                chunks.append('@@\n' if line.startswith('@@') else line)
            if not chunks[-1].endswith('\n'):
                chunks[-1] += '\n'
        else:
            chunks.append(f'*** Add File: {target}\n')
            chunks.extend('+' + line + '\n' for line in text.splitlines())
    chunks.append('*** End Patch\n')
    return ''.join(chunks)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--patch', type=Path, help='Write reviewable patch, not source files')
    args = parser.parse_args()
    plans = discover(inventory())
    files = rendered_files(plans)
    if args.patch:
        args.patch.write_text(patch_text(files))
    changes = []
    for target, text in sorted(files.items()):
        changed = not target.exists() or target.read_text() != text
        changes.append({'artifact': str(target.relative_to(ROOT)), 'changed': changed})
        if args.write and changed:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text)
    print(json.dumps({'write': args.write, 'blocks': len(plans),
                      'changed_files': sum(p['changed'] for p in changes), 'items': changes}, indent=2))


if __name__ == '__main__':
    main()