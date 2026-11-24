from functools import wraps

from flask import flash, jsonify, redirect, request, session, url_for


def _eh_api():
    return request.path.startswith("/api/")


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "usuario" not in session:
            if _eh_api():
                return jsonify({"erro": "Faça login para continuar."}), 401
            flash("Faça login primeiro")
            return redirect(url_for("paginas.login"))
        return f(*args, **kwargs)
    return wrapper


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if "usuario" not in session:
                if _eh_api():
                    return jsonify({"erro": "Faça login para continuar."}), 401
                return redirect(url_for("paginas.login"))

            if session.get("tipo") not in roles:
                if _eh_api():
                    return jsonify({"erro": "Você não tem permissão para esta ação."}), 403
                flash("Acesso negado")
                return redirect(url_for("paginas.home"))

            return f(*args, **kwargs)
        return wrapper
    return decorator
