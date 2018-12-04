from flask import Flask, render_template, url_for, request, session, redirect

app = Flask(__name__)

# set the secret key
app.secret_key = 'hello soodevv github'

@app.route('/')
def hello():
    return render_template('hello.html')


@app.route('/user/<username>')
def profile(username):
    return '{} profile!!'.format(username='soo')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user_id'] = request.form['user_id']
        return redirect(url_for('hello'))

    return render_template('login.html')


if __name__ == '__main__':
    app.run()
