#!/usr/bin/env python
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_demo_backend.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable?"
        ) from exc

    try:
        if len(sys.argv) >= 2 and sys.argv[1] == 'runserver':
            addr = sys.argv[2] if len(sys.argv) >= 3 and sys.argv[2] and not sys.argv[2].startswith('-') else '127.0.0.1:8000'
            if ':' not in addr:
                addr = f"{addr}:8000"
            host = '127.0.0.1' if addr.startswith('0.0.0.0') else addr.split(':')[0]
            port = addr.split(':')[1]
            print(f"  Frontend → http://{host}:{port}/")
    except Exception:
        pass

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
