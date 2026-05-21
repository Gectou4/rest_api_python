import re

from flask import Flask, jsonify, request

from src.controllers.task import TaskController
from src.controllers.user import UserController

app = Flask(__name__)

ROUTES = [
    ("GET", r"^user/(\d+)$", "get_index", UserController),
    ("GET", r"^user/(\d+)/task$", "get_user_task", UserController),
    ("POST", r"^task$", "post_add_task", TaskController),
    ("PUT", r"^task$", "put_add_task", TaskController),
    ("POST", r"^task/(\d+)$", "post_edit_task", TaskController),
    ("PUT", r"^task/(\d+)$", "put_edit_task", TaskController),
    ("DELETE", r"^task/(\d+)$", "delete_task", TaskController),
    ("POST", r"^user/(\d+)/task/(\d+)$", "post_add_task_to_user", TaskController),
    ("PUT", r"^user/(\d+)/task/(\d+)$", "put_add_task_to_user", TaskController),
    ("DELETE", r"^user/(\d+)/task/(\d+)$", "delete_user_task", TaskController),
]


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Accept, X-HTTP-Method-Override"
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def handle_request(path):
    if request.method == "OPTIONS":
        return "", 204

    method = request.headers.get("X-HTTP-Method-Override", request.method).upper()
    if method == "HEAD":
        method = "GET"

    accept_markdown = "text/markdown" in request.headers.get("Accept", "")

    for route_method, pattern, action_name, controller_class in ROUTES:
        if route_method != method:
            continue
        match = re.match(pattern, path)
        if match:
            controller = controller_class()
            action = getattr(controller, action_name, None)
            if action:
                args = [int(g) for g in match.groups()]
                response = action(*args)

                if accept_markdown and hasattr(controller, "markdown_response"):
                    data = response.get_json(silent=True)
                    if data is not None:
                        return controller.markdown_response(data, response.status_code)
                return response

    return jsonify("Route not found"), 404


@app.errorhandler(Exception)
def handle_error(error):
    return jsonify({"error": str(error)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
