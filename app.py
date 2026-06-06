import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///island.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    available = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET'])
def index():
    date_str = "Wednesday, June 10, 2026"
    votes = Vote.query.order_by(Vote.created_at.desc()).all()
    yes = Vote.query.filter_by(available=True).count()
    no = Vote.query.filter_by(available=False).count()
    items = Item.query.order_by(Item.created_at).all()
    return render_template('index.html', date=date_str, votes=votes, yes=yes, no=no, items=items)


@app.route('/vote', methods=['POST'])
def vote():
    name = request.form.get('name', 'Anonymous').strip()
    available = request.form.get('available') == 'on'
    v = Vote(name=name if name else 'Anonymous', available=available)
    db.session.add(v)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/item', methods=['POST'])
def add_item():
    name = request.form.get('item', '').strip()
    if name:
        item = Item(name=name)
        db.session.add(item)
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/api/status')
def api_status():
    yes = Vote.query.filter_by(available=True).count()
    no = Vote.query.filter_by(available=False).count()
    items = [i.name for i in Item.query.order_by(Item.created_at).all()]
    return jsonify({'date': '2026-06-10', 'yes': yes, 'no': no, 'items': items})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
