"""Flask application for the Smart Expense Tracker API."""
from flask import Flask, jsonify, request

from src.models import ValidationError, validate_expense_payload
from src.storage import ExpenseStore


def create_app(persist_path=None):
    """Application factory. Pass persist_path=None to keep everything in memory
    (used by the test suite so tests never touch a real data file)."""
    app = Flask(__name__)
    store = ExpenseStore(persist_path=persist_path)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.post("/expenses")
    def add_expense():
        payload = request.get_json(silent=True)
        try:
            title, amount, category, date = validate_expense_payload(payload)
        except ValidationError as err:
            return jsonify({"error": err.message}), 400
        expense = store.add(title, amount, category, date)
        return jsonify(expense), 201

    @app.get("/expenses")
    def list_expenses():
        category = request.args.get("category")
        expenses = store.filter_by_category(category) if category else store.list_all()
        return jsonify(expenses), 200

    @app.get("/expenses/search")
    def search_expenses():
        query = request.args.get("q", "")
        if not query.strip():
            return jsonify({"error": "Query parameter 'q' is required."}), 400
        return jsonify(store.search(query)), 200

    @app.get("/expenses/summary")
    def summary():
        category = request.args.get("category")
        if category:
            return jsonify({"category": category, "total": store.total(category)}), 200
        return jsonify({
            "total": store.total(),
            "by_category": store.total_by_category(),
        }), 200

    @app.get("/expenses/<expense_id>")
    def get_expense(expense_id):
        expense = store.get(expense_id)
        if expense is None:
            return jsonify({"error": "Expense not found."}), 404
        return jsonify(expense), 200

    @app.delete("/expenses/<expense_id>")
    def delete_expense(expense_id):
        deleted = store.delete(expense_id)
        if not deleted:
            return jsonify({"error": "Expense not found."}), 404
        return "", 204

    @app.errorhandler(404)
    def not_found(_e):
        return jsonify({"error": "Not found."}), 404

    return app
