"""Hermes-owned Fly Company worker.

Run this process where Hermes authentication is available. It can use the
Railway PostgreSQL database through DATABASE_URL while Railway hosts only the
web service.
"""
import argparse
import os
import threading
import time
from pathlib import Path

MEETING_TIMEOUT_SECONDS = 15 * 60

import backend
from local_provider import HermesProvider


def load_worker_env():
    """Load the desktop worker env without overwriting existing secrets."""
    default_path = Path.home() / 'Desktop' / 'FlyCompany-Hermes.env'
    env_path = Path(os.environ.get('FLYCOMPANY_ENV_FILE', default_path))
    if not env_path.is_file():
        return env_path
    for raw in env_path.read_text(encoding='utf-8').splitlines():
        line = raw.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        key, value = key.strip(), value.strip().strip('"').strip("'")
        if key and value and key not in os.environ:
            os.environ[key] = value
    return env_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--once', action='store_true', help='run one meeting and exit')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    env_path = load_worker_env()
    if not os.environ.get('DATABASE_URL') or os.environ['DATABASE_URL'].startswith('PASTE_'):
        raise SystemExit('Set DATABASE_URL in ' + str(env_path) + ' using Railway DATABASE_PUBLIC_URL')
    provider = HermesProvider()
    if not provider.verify():
        raise SystemExit('Hermes model access is unavailable: ' + provider.reason)
    app = backend.App(root / 'data' / 'company.sqlite3', provider)
    if args.once:
        app.start_meeting()
        deadline = time.monotonic() + MEETING_TIMEOUT_SECONDS
        while app.worker and app.worker.is_alive() and time.monotonic() < deadline:
            app.worker.join(timeout=1)
        if app.worker and app.worker.is_alive():
            with app.lock:
                state = app.load()
                for meeting in state.get('meetings', []):
                    if meeting.get('status') == 'running':
                        meeting.update(status='interrupted', endedAt=backend.now(), summary='Meeting timed out before completion. No tweet was attempted.')
                app.save(state)
            raise SystemExit('Fly Company Hermes cycle timed out after 15 minutes')
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