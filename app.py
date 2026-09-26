import sys
from app import create_app, db
from app.cli import init_db, seed, create_admin

app = create_app()

if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else "run"
    with app.app_context():
        if command == "init-db":
            init_db()
        elif command == "seed":
            seed()
        elif command == "create-admin":
            create_admin()
        else:
            app.run(host="127.0.0.1", port=5000, debug=False)
