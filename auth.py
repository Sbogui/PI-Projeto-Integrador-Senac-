from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "usuario" not in session:
            flash("Faça login primeiro")
            return redirect(url_for("paginas.login"))
        return f(*args, **kwargs)
    return wrapper


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if "usuario" not in session:
                return redirect(url_for("paginas.login"))

            if session.get("tipo") not in roles:
                flash("Acesso negado")
                return redirect(url_for("paginas.home"))

            return f(*args, **kwargs)
        return wrapper
    return decorator