from flask import current_app as app

class Category:
    def __init__(self, category_name):
        self.category_name = category_name

    @staticmethod
    def get_categories():
        rows = app.db.execute('''
        SELECT *
        FROM Category
        ''')
        return [Category(*(rows[0])) if rows is not None else None]