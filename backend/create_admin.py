"""Provision a NextGenERP administrator account.

Examples (run from the backend directory):

    .\\venv\\Scripts\\python.exe create_admin.py --username ops-admin
    .\\venv\\Scripts\\python.exe create_admin.py --username ops-admin --email ops@example.com
    .\\venv\\Scripts\\python.exe create_admin.py --username existing-user --promote

The password is read from ADMIN_PASSWORD when set, otherwise prompted without
echo.  It is never printed or written to logs.
"""

from __future__ import annotations

import argparse
import getpass
import os
import sys

from sqlalchemy.orm import Session

from admin_provision import provision_admin
from database.connection import engine


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create or promote a NextGenERP administrator")
    parser.add_argument("--username", default=os.getenv("ADMIN_USERNAME", ""))
    parser.add_argument("--email", default=os.getenv("ADMIN_EMAIL", ""))
    parser.add_argument(
        "--promote",
        action="store_true",
        help="Promote an existing normal user instead of refusing the operation",
    )
    parser.add_argument(
        "--reset-password",
        action="store_true",
        help="Set a new password for an existing administrator",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    username = args.username.strip()
    if not username:
        username = input("Administrator username: ").strip()

    password = os.getenv("ADMIN_PASSWORD", "")
    if not password:
        password = getpass.getpass("Administrator password: ")
        confirmation = getpass.getpass("Confirm password: ")
        if password != confirmation:
            print("Passwords do not match.", file=sys.stderr)
            return 1

    with Session(engine) as db:
        try:
            result = provision_admin(
                db,
                username,
                password,
                args.email or None,
                promote=args.promote,
                reset_password=args.reset_password,
            )
        except ValueError as error:
            print(f"Could not provision administrator: {error}", file=sys.stderr)
            return 1

    action = "Created" if result.created else "Updated"
    print(f"{action} administrator account: {result.user.username}")
    print("Sign in at /admin/login. The password was not printed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
