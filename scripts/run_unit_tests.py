"""Run offline unittest discovery with a new empty cache and blocked networking."""
import os
from pathlib import Path
import socket
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import requests

from official_source_loader import configure_cache


def main():
    with TemporaryDirectory(prefix='official-offline-') as directory:
        configure_cache(directory, offline=True)
        with patch.dict(os.environ, {'OFFICIAL_SOURCE_TESTS': '0'}), \
                patch.object(socket.socket, 'connect', side_effect=AssertionError('Network denied')), \
                patch.object(socket, 'create_connection', side_effect=AssertionError('Network denied')), \
                patch.object(requests.sessions.Session, 'request', side_effect=AssertionError('HTTP denied')):
            suite = unittest.defaultTestLoader.discover(str(Path(__file__).parent), pattern='test_*.py')
            result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(not result.wasSuccessful())


if __name__ == '__main__':
    main()