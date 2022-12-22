from flask_bootstrap import Bootstrap
from flask import Flask, redirect, url_for, render_template, flash, request
from flask_wtf.csrf import CSRFProtect

from controller import short_url, qr_code_url, get_original_url

from models import db


app = Flask(__name__)
app.config.from_pyfile("config.py")
csrf = CSRFProtect(app)
bootstrap = Bootstrap(app)
db.init_app(app)



@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        url = request.form['url']
        if url:
            context={
                "shorted_url":short_url(url),
                "qr_code":qr_code_url(url)
            }
            return render_template("index.html", **context)
            
        else:
            flash('The URL is required!')
            return render_template("index.html")
    else:
        return render_template("index.html")



@app.route('/<id>')
def target_url(id):
    
    if get_original_url(hashid=id):
        target_url = get_original_url(hashid=id)
        return redirect(target_url)
    else:
        flash('Invalid URL')
        return redirect(url_for('index'))


""" with app.app_context():
    db.create_all() """



if __name__ == "__main__":
    app.run()


