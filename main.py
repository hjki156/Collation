from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
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
    return jsonify({'code': 200, 'length': Exam.query.count()})

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

@app.route('/delete/<int:id>')
def delete_by_id(id):
    question = Exam.query.get(id)
    if question:
        db.session.delete(question)
        db.session.commit()
        return jsonify({'code': 200})
    return jsonify({'code': 400, 'msg': 'Not found'})

@app.route('/get/')
@app.route('/get/<int:page>')
def get(page=1):
    size = 15
    if request.content_type == 'application/json':
        size = request.json.get('size', size)
    questions = Exam.query.order_by(Exam.id).paginate(page=page, per_page=size)
    data = [exam.to_dict() for exam in questions]
    return jsonify({'code': 200, 'data': data, 'length': Exam.query.count()})

@app.route('/search')
def search():
    query = request.args.get('q')
    if not query:
        return jsonify({'message': 'No query provided'}), 400
    results = Exam.query.filter(or_(Exam.content.contains(query), Exam.author.contains(query), Exam.tags.contains(query))).all()
    result_list = [exam.to_dict() for exam in results]
    return jsonify(result_list)

def main():
    return

if __name__ == '__main__':
    app.run(port=2013, debug=True)
