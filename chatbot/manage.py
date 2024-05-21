#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

"""
    Main function that runs administrative tasks for a Django project.
    This function sets the necessary environment variables, checks for the presence of Django,
    and executes command-line arguments to manage the Django project.
"""
def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
