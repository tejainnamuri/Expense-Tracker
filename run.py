"""Entry point to run the Expense Tracker API locally.

Data is persisted to data.json in the project root so expenses survive
a server restart. Delete data.json to start with a clean slate.
"""
from src.app import create_app

if __name__ == "__main__":
    app = create_app(persist_path="data.json")
    app.run(host="0.0.0.0", port=5000, debug=True)
