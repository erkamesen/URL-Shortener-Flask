from flask_bootstrap import Bootstrap
from flask import Flask, redirect, url_for, render_template, flash, request
from flask_wtf.csrf import CSRFProtect

from controller import short_url, qr_code_url, get_original_url, click_counter, show_stats

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
        click_counter(target_url)
        return redirect(target_url)
    else:
        flash('Invalid URL')
        return redirect(url_for('index'))
    
    
@app.route("/clicks")
def clicks():
    url_list = show_stats()
    return render_template("clicks.html", url_list = url_list)



""" with app.app_context():
    db.drop_all()
    db.create_all() """



if __name__ == "__main__":
    app.run()


