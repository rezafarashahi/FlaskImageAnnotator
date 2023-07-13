from __init__ import app
from __init__ import db
from __init__ import Users
from werkzeug.security import generate_password_hash





app.app_context().push()



u = Users(username="sara",
          password_hash=generate_password_hash("sara1", "sha256"))
db.session.add(u)
db.session.commit()

db.create_all()