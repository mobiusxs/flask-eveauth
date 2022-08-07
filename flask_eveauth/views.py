from flask import Blueprint, redirect, url_for

routes = Blueprint('auth', __name__, url_prefix='/auth')


def authorize():
    return redirect('')


def callback():
    return redirect(url_for(''))


def logout():
    return redirect(url_for(''))


routes.add_url_rule(rule='/authorize', view_func=authorize, endpoint='authorize', methods=['GET'])
routes.add_url_rule(rule='/callback', view_func=callback, endpoint='callback', methods=['GET'])
routes.add_url_rule(rule='/logout', view_func=logout, endpoint='logout', methods=['GET'])
