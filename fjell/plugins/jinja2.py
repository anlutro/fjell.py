import diay
import jinja2
from fjell.app import Application
from fjell.http import Response


__plugin__ = "Jinja2Plugin"


class Jinja2Plugin(diay.Plugin):
    @diay.provider(singleton=True)
    def provide_jinja_loader(self, app: Application) -> jinja2.BaseLoader:
        # TODO: ability to change which loader to use
        return jinja2.PackageLoader(app.name, "templates")

    @diay.provider(singleton=True)
    def provide_jinja_env(
        self, loader: jinja2.BaseLoader
    ) -> jinja2.Environment:  # noqa
        return jinja2.Environment(loader=loader)


@diay.inject("jinja", jinja2.Environment)
class Jinja2ViewMixin:
    def render_template(self, template, **context):
        return Response(
            self.jinja.get_template(template).render(**context), mimetype="text/html"
        )
