#!/usr/bin/env python
"""Dev entrypoint."""

import os
import sys


def main() -> None:
    """Main function.

    It does several things:
    1. Sets default settings module, if it is not set
    2. Warns if Django is not installed
    3. Executes any given command
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

    try:
        from django.core import management  # noqa: WPS433, PLC0415
    except ImportError as err:
        raise ImportError(
            ' '.join([
                "Couldn't import Django. Are you sure it's installed and",
                'available on your PYTHONPATH environment variable? Did you',
                'forget to activate a virtual environment?',
            ])
        ) from err

    management.execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
