from fjell import views, http
from fjell.plugins.jinja2 import Jinja2ViewMixin
from fjell.plugins.sqla import SqlAlchemyMixin

from example.models import User


def index(request):
    return "hello world from index!\n"


class TemplateView(views.View, Jinja2ViewMixin):
    def render(self, request):
        return self.render_template("test.html", templating="jinja")


class JsonViewSet(views.ViewSet):
    def get(self, request):
        return http.JsonResponse(
            {"status": "ok", "message": "hello world from BarViewSet.get!",}
        )

    def post(self, request):
        return http.JsonResponse(
            {
                "status": "ok",
                "message": "hello %s from BarViewSet.post!" % request.form["name"],
            }
        )


class UsersViewSet(views.RestViewSet, SqlAlchemyMixin):
    def list(self, request):
        users = self.session.query(User).all()
        return http.JsonResponse({"users": [u.as_dict() for u in users]})

    def show(self, request, id):
        user = self.session.query(User).filter_by(id=id).first()
        if not user:
            return http.Response(status=404)
        return http.JsonResponse(user.as_dict())

    def create(self, request):
        user = User(name=request.form["name"], password=request.form["password"])
        self.session.add(user)
        self.session.commit()
        return http.JsonResponse(user.as_dict())

    def update(self, request, id):
        user = self.session.query(User).filter(User.id == id).first()
        user.name = request.form["name"]
        self.session.add(user)
        self.session.commit()
        return http.JsonResponse(user.as_dict())

    def delete(self, request, id):
        user = self.session.query(User).filter(User.id == id).first()
        self.session.delete(user)
        self.session.commit()
        return http.Response(status=202)
