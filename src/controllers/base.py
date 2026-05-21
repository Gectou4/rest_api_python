from flask import jsonify, make_response


class BaseController:
    status_code: int = 200

    def json_response(self, data, status_code: int = 200):
        self.status_code = status_code
        response = make_response(jsonify(data), status_code)
        response.headers["Content-Type"] = "application/json"
        return response

    def markdown_response(self, data, status_code: int = 200):
        self.status_code = status_code
        md = self._dict_to_markdown(data)
        response = make_response(md, status_code)
        response.headers["Content-Type"] = "text/markdown"
        return response

    def _dict_to_markdown(self, data, indent: int = 0) -> str:
        lines = []
        prefix = "  " * indent
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    lines.append(f"{prefix}**{key}**:")
                    lines.append(self._dict_to_markdown(value, indent + 1))
                else:
                    lines.append(f"{prefix}**{key}**: {value}")
        elif isinstance(data, list):
            for item in data:
                lines.append(f"{prefix}- {self._dict_to_markdown(item, indent + 1)}")
        else:
            lines.append(f"{prefix}{data}")
        return "\n".join(lines)
