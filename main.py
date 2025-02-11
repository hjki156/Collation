from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import manager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/Collation'
db = SQLAlchemy(app)
Exam = manager.Exam_Factory(db.Model)

@app.before_request
def create_tables():
    if not hasattr(app.config, 'initialized'):
        app.config.initialized = True
        with app.app_context():
            db.create_all()

@app.route('/')
def index():
    return 'running'

@app.route('/count')
def count():
    length = Exam.query.count()
    return jsonify({'code': 200, 'length': length})

@app.route('/add')
def add():
    content = request.json.get('content')
    author = request.json.get('author')
    try:
        new_question = Exam(content=content, author=author)
        db.session.add(new_question)
        db.session.commit()
        return jsonify({'code': 200})
    except Exception as e:
        print(e)
        return jsonify({'code': 400})

def main():
    return

if __name__ == '__main__':
    app.run(port=2013, debug=True)
