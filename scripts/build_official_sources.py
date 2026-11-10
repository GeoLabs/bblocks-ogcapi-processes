"""Run bblocks-postprocess with a narrowly scoped YAML 1.2 scalar adapter.

Official CQL2 uses the bare scalar '='. PyYAML's YAML 1.1 resolver assigns
tag:yaml.org,2002:value but SafeLoader has no constructor for it. Registering
the scalar constructor preserves the intended string and all source bytes.
No reference, schema keyword, constraint or validation result is rewritten.
All command-line options are forwarded to the standard entry point.
"""
import runpy

import yaml


def configure_yaml():
    for name in ('SafeLoader', 'CSafeLoader', 'FullLoader', 'CFullLoader'):
        loader = getattr(yaml, name, None)
        if loader is not None:
            loader.add_constructor('tag:yaml.org,2002:value',
                                   lambda parser, node: parser.construct_scalar(node))


if __name__ == '__main__':
    configure_yaml()
    runpy.run_module('ogc.bblocks.entrypoint', run_name='__main__')