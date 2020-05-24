from fjell.app import Application

app = Application(__name__, debug=True)
app.config.update(
    {"db": "sqlite:////tmp/db.sqlite3",}
)

app.add_plugin("fjell.plugins.sqla")
app.add_plugin("fjell.plugins.jinja2")

app.add_routes(
    [
        ("GET", "/", "example.views.index"),
        ("GET", "/template", "example.views.TemplateView"),
        (("GET", "POST"), "/hello", "example.views.JsonViewSet"),
    ]
)

app.add_route_set("/users", "example.views.UsersViewSet")
