from flask import (
    render_template, 
    jsonify, 
    abort,
    url_for, 
    Flask, 
    request,
    redirect
)
from flask_login import login_required
from flask.views import View, MethodView
from app.services import CatalogService
from app.forms import NewItemForm, EditItemForm

def add_routes(app: Flask, catalog_service: CatalogService):
    app.add_url_rule('/item/<int:item_id>', 
        view_func = CatalogItemView.as_view('catalog_item_view', catalog_service=catalog_service))
    app.add_url_rule('/api/item/<int:item_id>', 
        view_func = CatalogItemViewJson.as_view('catalog_item_json_view', catalog_service=catalog_service))

    ## Add views that will require login
    new_item_view = NewCatalogItemView.as_view('new_catalog_item_view', catalog_service=catalog_service)
    app.add_url_rule('/item/new', view_func = login_required(new_item_view))

    edit_item_view = EditCatalogItemView.as_view('edit_catalog_item_view', catalog_service=catalog_service)
    app.add_url_rule('/item/<int:item_id>/edit', view_func = login_required(edit_item_view))

    delete_item_view = DeleteCatalogItemView.as_view('delete_catalog_item_view', catalog_service=catalog_service)
    app.add_url_rule('/item/<int:item_id>/delete', view_func = login_required(delete_item_view))

class CatalogItemView(View):
    def __init__(self, catalog_service: CatalogService):
        self.catalog_service = catalog_service

    def dispatch_request(self, item_id: int):
        item = self.catalog_service.get_category_item(item_id)
        return render_template('item.html', item = item)

class CatalogItemViewJson(MethodView):
    def __init__(self, catalog_service: CatalogService):
        self.catalog_service = catalog_service

    def get(self, item_id: int):
        item = self.catalog_service.get_category_item(item_id)
        if item is None:
            abort(404)
        return jsonify(item.to_dict())

class NewCatalogItemView(MethodView):
    def __init__(self, catalog_service: CatalogService):
        self.catalog_service = catalog_service

    def get(self):
        categories = self.catalog_service.get_categories()
        form = NewItemForm()
        form.set_categories(categories)
        return render_template('add_item.html', form=form)
    
    def post(self):
        categories = self.catalog_service.get_categories()
        form = NewItemForm(request.form)
        form.set_categories(categories)
        category_lookup = dict(form.category.choices)

        if form.validate_on_submit():
            try:
                self.catalog_service.save_category_item(form)
                selected_category = category_lookup[form.category.data]
                return redirect(url_for('category_view', category_name=selected_category))
            except Exception as e:
                return render_template('500.html', error = str(e))

        #Invalid form so redirect to the new item page so the user can try again
        return redirect(url_for('new_catalog_item_view'))

class EditCatalogItemView(MethodView):
    def __init__(self, catalog_service: CatalogService):
        self.catalog_service = catalog_service

    def get(self, item_id: int):
        item = self.catalog_service.get_category_item(item_id)
        if item is None:
            abort(404)

        categories = self.catalog_service.get_categories()
        form = EditItemForm()
        form.set_item(item, categories)
        return render_template('update_item.html', form=form)
    
    def post(self, item_id: int):
        categories = self.catalog_service.get_categories()
        form = EditItemForm(request.form)
        form.set_categories(categories)    

        if form.validate_on_submit():
            try:
                self.catalog_service.update_category_item(form, item_id)
                return redirect(url_for('catalog_item_view', item_id=item_id))
            except Exception as e:
                return render_template('500.html', error = str(e))
            
        return redirect(url_for('edit_catalog_item_view', item_id=item_id))

class DeleteCatalogItemView(MethodView):
    def __init__(self, catalog_service: CatalogService):
        self.catalog_service = catalog_service

    def get(self, item_id: int):
        item = self.catalog_service.delete_category_item(item_id)
        return redirect(url_for('categories_view'))
    