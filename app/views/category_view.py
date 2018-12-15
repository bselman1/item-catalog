from flask import render_template, jsonify, abort,url_for, Flask
from flask.views import View, MethodView
from app.services import CatalogService

def add_routes(app: Flask, catalog_service: CatalogService):
    app.add_url_rule('/categories', 
        view_func = CategoriesView.as_view('categories_view', catalog_service=catalog_service))

    app.add_url_rule('/api/categories', 
        view_func = CategoriesViewJson.as_view('categories_json_view', catalog_service=catalog_service))

    app.add_url_rule('/category/<string:category_name>', 
        view_func = CategoryView.as_view('category_view', catalog_service=catalog_service))

    app.add_url_rule('/api/category/<string:category_name>', 
        view_func = CategoryViewJson.as_view('category_json_view', catalog_service=catalog_service))

    app.add_url_rule('/api/catalog',
        view_func = CatalogViewJson.as_view('catalog_json_view', catalog_service=catalog_service))

    
class CategoriesView(View):
    def __init__(self, catalog_service: CatalogService):
        self.catalog_service = catalog_service

    def dispatch_request(self):
        categories = self.catalog_service.get_categories()
        return render_template('categories.html', categories = categories)

class CategoriesViewJson(MethodView):
    def __init__(self, catalog_service: CatalogService):
        self.catalog_service = catalog_service

    def get(self):
        categories = self.catalog_service.get_categories()
        category_dicts = { 'categories': [category.to_dict() for category in categories] }
        return jsonify(category_dicts)

class CategoryView(View):
    def __init__(self, catalog_service: CatalogService):
        self.catalog_service = catalog_service

    def dispatch_request(self, category_name: str):
        category = self.catalog_service.get_category(category_name)
        categories = self.catalog_service.get_catalog()
        return render_template('selected_category.html', category=category, categories=categories)

class CategoryViewJson(MethodView):
    def __init__(self, catalog_service: CatalogService):
        self.catalog_service = catalog_service

    def get(self, category_name: str):
        category = self.catalog_service.get_category(category_name)
        if category is None:
            abort(404)
        return jsonify(category.to_dict())

class CatalogViewJson(MethodView):
    def __init__(self, catalog_service: CatalogService):
        self.catalog_service = catalog_service
    
    def get(self):
        catalog = self.catalog_service.get_catalog()
        category_dicts = { 'categories': [category.to_dict() for category in catalog] }
        return jsonify(category_dicts)