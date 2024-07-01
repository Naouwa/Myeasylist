from app import app, create_db

if __name__ == "__main__":
    create_db()
    app.run()
