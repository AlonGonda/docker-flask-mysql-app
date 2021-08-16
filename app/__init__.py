from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from wtforms import *
from passlib.hash import *
import requests
from models import Employee

from config import app_config

db = SQLAlchemy()
login_manager = LoginManager()



def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    #app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)

    def Request(url):
        base_url = 'http://tinyurl.com/api-create.php?url='
        url = base_url + url
        r = requests.get(url)
        return r.text

    # temporary route
    @app.route('/', methods=['GET', 'POST'])
    def hello_world():
        #get data from user
        form = EnterUrl(request.form)
        if request.method == 'POST':
            get_url = form.original.data
            #check if url exists
            indb = Employee.query.filter_by(url = get_url).first()
            if indb > 0:
                #get the url+tinyurl row from the db
                tinyurl = indb.tiny_url
                #show the tinyurl
                flash(Markup('<a href="%s" class="alert-link">%s</a>' %(tiny_url, tiny_url)), 'success')
            else:
                #insert the new data into the db
                tinyurl = Request(url)
                if (tinyurl != 'Error'):
                    to_add = Employee(url=get_url, tiny_url = tinyurl)
                    db.session.add(to_add)
                    #commit to DB
                    dn.session.commit()
                    #show the tinyurl
                    flash(Markup('<a href="%s" class="alert-link">%s</a>' %(tiny_url, tiny_url)), 'success')
                else:
                    flash(Markup('Bad URL. Try Again!'), 'success')
            redirect(url_for('index'))

        return render_template('home.html', form=url)

    class EnterUrl(Form):
        original = StringField('Enter Actual URL')

    login_manager.init_app(app)
    login_manager.login_message = 'You must be logged in to access this page'
    login_manager.login_view = 'auth.login'

    migrate = Migrate(app,db)

    from app import models

    return app
