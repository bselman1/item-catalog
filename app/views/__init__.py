from flask import Flask
from .item_view import add_routes as add_item_routes
from .category_view import add_routes as add_category_routes
from .google_auth import add_routes as add_login_routes, GoogleAuthConfig
from .logout_view import add_routes as add_logout_route
from .default_view import add_routes as add_default_route
from app.services import CatalogService


def init_app(
    app: Flask,
    catalog_service: CatalogService,
    google_auth_config: GoogleAuthConfig
):
    add_item_routes(app, catalog_service)
    add_category_routes(app, catalog_service)
    add_login_routes(app, google_auth_config)
    add_logout_route(app)
    add_default_route(app)
