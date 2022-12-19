from web import app
from flask import render_template


@app.route('/')
@app.route('/index')
def index():
    data = {
        'name': 'Timur',
        'age': 34,
        'title': 'Main page'
    }
    html = render_template('shop/index.html', **data)
    return html


@app.route('/login')
def login():
    return render_template('user/login.html', title='Login')

@app.route('/cart')
def cart():
    return render_template('cart/cart.html', title='Cart')

@app.route('/model_directory')
def model_directory():
    return render_template('model_directory/model_directory.html', title='Model_directory')

