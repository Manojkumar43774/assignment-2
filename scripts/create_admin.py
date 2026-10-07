"""
Bootstrap the first admin account.

The /admin endpoints all require an existing admin's JWT, so the very first
admin has to be promoted directly in the database. Run this once a user has
registered through /auth/register:

    python scripts/create_admin.py <username>

Run it from the project root with the venv active, so the `app` package is
importable.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database import SessionLocal
from app.models import User


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/create_admin.py <username>")
        sys.exit(1)

    username = sys.argv[1]
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            print(f"User '{username}' not found. Register them first via /auth/register.")
            sys.exit(1)

        if user.role == "admin":
            print(f"'{username}' is already an admin.")
            return

        user.role = "admin"
        db.commit()
        print(f"'{username}' is now an admin.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
