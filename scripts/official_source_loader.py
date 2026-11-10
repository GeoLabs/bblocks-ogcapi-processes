"""Shared HTTP cache state, including when the audit is run as __main__."""
import hashlib
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from threading import RLock
from urllib.parse import unquote, urldefrag

import requests
import yaml

DEFAULT_OUTPUT = Path(__file__).resolve().parents[1] / 'build-local/official-audit'


class SourceLoader(yaml.SafeLoader):
    """Preserve the YAML 1.2 string '=' without modifying source bytes."""


SourceLoader.add_constructor('tag:yaml.org,2002:value',
                             lambda loader, node: loader.construct_scalar(node))


class SourceCache:
    def __init__(self, output=DEFAULT_OUTPUT, refresh=False, offline=False):
        self.output = Path(output)
        self.refresh = refresh
        self.offline = offline
        self.loaded = set()
        self.lock = RLock()

    def load(self, url):
        base, fragment = urldefrag(url)
        cache = self.output / 'http' / (hashlib.sha256(base.encode()).hexdigest() + '.yaml')
        with self.lock:
            missing = not cache.is_file() or not cache.stat().st_size
            if missing or (self.refresh and base not in self.loaded):
                if self.offline:
                    raise ValueError(f'Offline cache miss: {base}; populate the selected cache first')
                response = requests.get(base, timeout=90)
                response.raise_for_status()
                # Validate before replacing a usable cached snapshot.
                yaml.load(response.content, Loader=SourceLoader)
                cache.parent.mkdir(parents=True, exist_ok=True)
                with NamedTemporaryFile(dir=cache.parent, delete=False) as temporary:
                    temporary.write(response.content)
                temporary_path = Path(temporary.name)
                try:
                    temporary_path.replace(cache)
                finally:
                    temporary_path.unlink(missing_ok=True)
            self.loaded.add(base)
            value = yaml.load(cache.read_text(encoding='utf-8'), Loader=SourceLoader)
        if fragment:
            if not fragment.startswith('/'):
                raise ValueError(f'Unsupported JSON pointer: {fragment}')
            for token in unquote(fragment)[1:].split('/'):
                token = token.replace('~1', '/').replace('~0', '~')
                value = value[int(token)] if isinstance(value, list) else value[token]
        return value


_cache = SourceCache(os.environ.get('OFFICIAL_SOURCE_OUTPUT', DEFAULT_OUTPUT),
                     offline=os.environ.get('OFFICIAL_SOURCE_OFFLINE') == '1')


def configure_cache(output=DEFAULT_OUTPUT, refresh=False, offline=False):
    global _cache
    if refresh and offline:
        raise ValueError('--refresh and --offline are mutually exclusive')
    _cache = SourceCache(output, refresh, offline)


def load(url):
    return _cache.load(url)