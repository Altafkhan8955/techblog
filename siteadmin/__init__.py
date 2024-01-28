from flask import Blueprint

siteadmin = Blueprint('siteadmin',__name__,static_folder='static',template_folder="templates")


from siteadmin import route