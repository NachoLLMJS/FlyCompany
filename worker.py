"""Hermes-owned Fly Company worker.

Run this process where Hermes authentication is available. It can use the
Railway PostgreSQL database through DATABASE_URL while Railway hosts only the
web service.
"""
import argparse
import os
import threading
from pathlib import Path

import backend
from local_provider import HermesProvider


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--once', action='store_true', help='run one meeting and exit')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    provider = HermesProvider()
    if not provider.verify():
        raise SystemExit('Hermes model access is unavailable: ' + provider.reason)
    app = backend.App(root / 'data' / 'company.sqlite3', provider)
    if args.once:
        app.run_once()
        print('Fly Company Hermes cycle completed', flush=True)
        return
    stop = threading.Event()
    print('Fly Company Hermes worker running', flush=True)
    try:
        app.scheduler_loop(stop)
    except KeyboardInterrupt:
        stop.set()


if __name__ == '__main__':
    main()