import elasticsearch
import json
from flask import Flask, request, redirect
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, DateField
from wtforms.validators import DataRequired
import datetime


app = Flask(__name__)
es_client = elasticsearch.Elasticsearch('localhost:9200')

app.secret_key = 'icis secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECURITY_PASSWORD_SALT'] = 'ICIS'
app.config['SECURITY_PASSWORD_HASH'] = 'sha512_crypt'
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
app.config['WTF_CSRF_SECRET_KEY'] = 'icissecrete'


db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    seq = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    babyName = db.Column(db.String(255), nullable=False)
    birthDate = db.Column(db.Date, nullable=False)


class Role(db.Model, RoleMixin):
    seq = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(100), unique=True, nullable=False)
    milkpowder = db.Column(db.String(100))
    diaper = db.Column(db.String(100))
    toy = db.Column(db.String(100))
    snack = db.Column(db.String(100))


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


class UserForm(FlaskForm):
    id = StringField('id', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    babyName = StringField('babyName', validators=[DataRequired()])
    birthDate = DateField('birthDate', format="%m/%d/%Y", validators=[DataRequired()])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/shop-grid')
def shop_grid():
    return render_template('shop-grid.html')


@app.route('/search', methods=['POST'])
def search():
    titles = []
    imgs = []
    prices = []

    search_term = request.form['search']
    doc = es_client.search(index='_all', body={
        "query": {
            "match_phrase": {
                "title": search_term
            }
        }
    }, size=999)

    resultCount = len(doc['hits']['hits'])

    # for i in range(resultCount):
    #     print(json.dumps(doc['hits']['hits'][i]['_source'], ensure_ascii=False, indent=2))

    for i in range(resultCount):
        titles.append(doc['hits']['hits'][i]['_source']['title'])

    for i in range(resultCount):
        imgs.append(doc['hits']['hits'][i]['_source']['img'])

    for i in range(resultCount):
        prices.append(str(doc['hits']['hits'][i]['_source']['price']) + '원')

    return render_template('shop-grid.html', titles=titles, imgs=imgs, prices=prices)


@app.route('/register', methods=['POST','GET'])
def register():
    userform = UserForm()

    if request.method == 'POST':

        # User DB에 넣기
        user = User()
        user.id = userform.id._value()
        user.password = userform.password._value()
        user.babyName = userform.babyName._value()
        birthDate = userform.birthDate._value().split('/')

        user.birthDate = datetime.date(int(birthDate[2]), int(birthDate[0]), int(birthDate[1]))

        db.session.add(user)
        db.session.commit()
        return render_template('preference.html', user = user.id)

    return render_template('register.html', form=userform)


@app.route('/prefer', methods=['POST','GET'])
def prefer():

    if request.method == 'POST':
        user_id = request.form['user_id']
        milkpowder = request.form['milkpowder']
        diaper = request.form['diaper']
        toy = request.form['toy']
        snack = request.form['snack']

        print(user_id, milkpowder, diaper, toy, snack)

        role = Role()
        role.user_id = user_id
        role.milkpowder = milkpowder
        role.diaper = diaper
        role.toy = toy
        role.snack = snack

        db.session.add(role)
        db.session.commit()

        return redirect('/')

    return render_template('preference.html')


if __name__ == '__main__':
    app.run()

