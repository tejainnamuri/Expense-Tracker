"""In-memory expense storage with optional JSON file persistence."""
import json
import os
import uuid


class ExpenseStore:
    """Holds expenses in memory and optionally mirrors them to a JSON file.

    Expenses are kept in a dict keyed by id for O(1) lookup/delete, plus an
    ordered list of ids so listing preserves insertion order.
    """

    def __init__(self, persist_path=None):
        self.persist_path = persist_path
        self._expenses = {}
        self._order = []
        if self.persist_path and os.path.exists(self.persist_path):
            self._load()

    def _load(self):
        try:
            with open(self.persist_path, "r") as f:
                data = json.load(f)
            for expense in data:
                self._expenses[expense["id"]] = expense
                self._order.append(expense["id"])
        except (json.JSONDecodeError, OSError):
            # Start fresh instead of crashing on boot if the file is missing/corrupt
            self._expenses = {}
            self._order = []

    def _save(self):
        if not self.persist_path:
            return
        with open(self.persist_path, "w") as f:
            json.dump(self.list_all(), f, indent=2)

    def add(self, title, amount, category, date):
        expense_id = str(uuid.uuid4())
        expense = {
            "id": expense_id,
            "title": title,
            "amount": round(float(amount), 2),
            "category": category,
            "date": date,
        }
        self._expenses[expense_id] = expense
        self._order.append(expense_id)
        self._save()
        return expense

    def list_all(self):
        return [self._expenses[i] for i in self._order]

    def get(self, expense_id):
        return self._expenses.get(expense_id)

    def filter_by_category(self, category):
        return [e for e in self.list_all() if e["category"].lower() == category.lower()]

    def search(self, query):
        q = query.lower()
        return [
            e for e in self.list_all()
            if q in e["title"].lower() or q in e["category"].lower()
        ]

    def delete(self, expense_id):
        if expense_id not in self._expenses:
            return False
        del self._expenses[expense_id]
        self._order.remove(expense_id)
        self._save()
        return True

    def total(self, category=None):
        expenses = self.list_all() if category is None else self.filter_by_category(category)
        return round(sum(e["amount"] for e in expenses), 2)

    def total_by_category(self):
        totals = {}
        for e in self.list_all():
            totals[e["category"]] = round(totals.get(e["category"], 0) + e["amount"], 2)
        return totals
