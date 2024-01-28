from blogwebsite import app
from blogwebsite.database import db
from siteadmin import siteadmin

app.register_blueprint(siteadmin,url_prefix='/admin')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=False)
