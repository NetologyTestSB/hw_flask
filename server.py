import flask
from errors import HttpError, error_handler
from user_crud import UserView
from ads_crud import AdsView


app = flask.Flask("app")

user_view = UserView.as_view("users")
app.add_url_rule(
    "/user/<int:user_id>", view_func=user_view, methods=["GET", "PATCH", "DELETE"]
)
app.add_url_rule("/user/", view_func=user_view, methods=["POST"])
ads_view = AdsView.as_view("advertisings")
app.add_url_rule(
    "/advertising/<int:ads_id>", view_func=ads_view, methods=["GET", "PATCH", "DELETE"]
)
app.add_url_rule("/advertising/", view_func=ads_view, methods=["POST"])



app.errorhandler(HttpError)(error_handler)

if __name__ == "__main__":
    app.run()

