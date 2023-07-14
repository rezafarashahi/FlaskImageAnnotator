from __init__ import app
from __init__ import db
from __init__ import Users
from werkzeug.security import generate_password_hash





app.app_context().push()



db.create_all()
