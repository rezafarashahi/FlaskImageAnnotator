from app import app
from app import db

app.app_context().push()
db.create_all()