#!/usr/bin/env python3
"""Database migration script."""

import subprocess
import sys
from pathlib import Path


def run_command(command):
    """Run a command and return the result."""
    try:
        result = subprocess.run(
            command, shell=True, check=True, capture_output=True, text=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return False


def main():
    """Main migration function."""
    if len(sys.argv) < 2:
        print("Usage: python migrate.py <command>")
        print("Commands:")
        print("  upgrade    - Run all pending migrations")
        print("  downgrade  - Rollback one migration")
        print("  current    - Show current migration")
        print("  history    - Show migration history")
        print("  create     - Create new migration")
        sys.exit(1)

    command = sys.argv[1]

    # Ensure migrations directory exists
    migrations_dir = Path("migrations")
    if not migrations_dir.exists():
        print("Error: migrations directory not found")
        sys.exit(1)

    if command == "upgrade":
        upgrade()

    elif command == "downgrade":
        downgrade()

    elif command == "current":
        run_command("alembic current")

    elif command == "history":
        run_command("alembic history --verbose")

    elif command == "create":
        create()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


def upgrade():
    """Upgrade migrations."""
    print("Running database migrations...")
    success = run_command("alembic upgrade head")
    if success:
        print("✅ Database migration completed successfully")
    else:
        print("❌ Database migration failed")
        sys.exit(1)


def downgrade():
    """Downgrade migrations."""
    print("Rolling back migration...")
    success = run_command("alembic downgrade -1")
    if success:
        print("✅ Migration rollback completed")
    else:
        print("❌ Migration rollback failed")
        sys.exit(1)


def create():
    """Create migrations."""
    if len(sys.argv) < 3:
        print("Usage: python migrate.py create <migration_message>")
        sys.exit(1)
    message = " ".join(sys.argv[2:])
    print(f"Creating new migration: {message}")
    success = run_command(f'alembic revision --autogenerate -m "{message}"')
    if success:
        print("✅ Migration created successfully")
        print("Don't forget to review the generated migration file!")
    else:
        print("❌ Migration creation failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
