from __init__ import app
from __init__ import db

app.app_context().push()
db.create_all()