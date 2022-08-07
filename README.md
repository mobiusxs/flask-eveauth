# Flask EveAuth

Eve Online SSO Authentication for Flask applications.  
Implements the [OAuth 2.0 for Web Based Applications](https://docs.esi.evetech.net/docs/sso/web_based_sso_flow.html) flow.

## Requires
1. Python >= 3.7
1. Flask
1. Flask-SQLAlchemy
1. Requests

## Install

```
pip install flask-eveauth
```

## Quickstart

app.py

```
from flask import Flask
from flask_eveauth import Auth()
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)
auth = Auth(app, db)
```

index.html

```
{% if not current_user.is_authenticated %}
   <a href="{{ url_for('auth.authorize') }}">Authorize</a>
{% else %}
   <a href="{{ url_for('auth.logout') }}">Logout</a>
{% endif %}
```

