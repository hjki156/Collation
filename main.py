from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import manager
import datetime
import jwt
import functools
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/Collation'
app.config['SECRET_KEY'] = 'l9doyPjww0wQ0XjBovSJKgglhM3Bl3jmdYnYKxPZS8vmnaZj72ttwwaquU5IN3U7ZSneGPZzQ5z2XZKp0R3Ywdei2rPh8rMdDUaMuO9LKgZExkm096qFuSU19yrlq7sP6ySWQjIyyMGex6gjR4biWtfwfo66kE5awDvAtOHFn0K9R8goGsj68lMlGbZgtxApkAm8pFx4V65BOYlyTwoieZoHL8Ti6IkRAGtnr4a3NI7I1s6PHAMxS60AcfYUyDgN'  # 用于JWT加密的密钥
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=1)  # Token有效期为1天
db = SQLAlchemy(app)
Exam = manager.Exam_Factory(db.Model)
User = manager.User_Factory(db.Model)

@app.before_request
def create_tables():
    if not hasattr(app.config, 'initialized'):
        app.config.initialized = True
        with app.app_context():
            db.create_all()

# 装饰器：验证Token
def token_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # 从请求头获取token
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(" ")[1]
        
        if not token:
            return jsonify({'code': 401, 'message': 'Token is missing or invalid'}), 401

        try:
            # 验证token
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['user_id']).first()
            if current_user is None:
                return jsonify({'code': 401, 'message': 'User not found'}), 401
            
        except jwt.ExpiredSignatureError:
            return jsonify({'code': 401, 'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'code': 401, 'message': 'Invalid token'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/')
def index():
    return 'running'

# 注册接口
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'code': 400, 'message': 'Username and password are required'}), 400
    
    # 检查是否已存在相同用户名
    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({'code': 400, 'message': 'Username already exists'}), 400
    
    # 创建新用户
    new_user = User(username=data['username'])
    new_user.set_password(data['password'])
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'code': 200, 'message': 'User registered successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e)}), 500

# 登录接口
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'code': 400, 'message': 'Username and password are required'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'code': 401, 'message': 'Invalid username or password'}), 401
    
    # 生成token
    token_expiration = datetime.datetime.utcnow() + app.config['JWT_EXPIRATION_DELTA']
    token = jwt.encode(
        {
            'user_id': user.id,
            'username': user.username,
            'exp': token_expiration
        },
        app.config['SECRET_KEY'],
        algorithm="HS256"
    )
    
    return jsonify({
        'code': 200,
        'token': token,
        'user': user.to_dict(),
        'expires': token_expiration.isoformat()
    })

# 获取当前用户信息
@app.route('/user/me', methods=['GET'])
@token_required
def get_user_info(current_user):
    return jsonify({'code': 200, 'user': current_user.to_dict()})

@app.route('/count')
def count():
    return jsonify({'code': 200, 'length': Exam.query.count()})

@app.route('/update', methods=['POST'])
@token_required
def update(current_user):
    try:
        id = request.json.get('id')
        question = Exam.query.get(id)
        if question:
            setAll = lambda attr: setattr(question, attr, request.json.get(attr, getattr(question, attr)))
            for e in question.to_dict():
                setAll(e)
            db.session.commit()
            return jsonify({'code': 200})
        else:
            return jsonify({'code': 400, 'msg': 'Item Not Found'})
    except Exception as e:
        print(e)
        return jsonify({'code': 400})

@app.route('/add', methods=['POST'])
@token_required
def add(current_user):
    content = request.json.get('content')
    author = request.json.get('author')
    try:
        new_question = Exam(content=content, author=author)
        setAll = lambda attr: setattr(new_question, attr, request.json.get(attr, getattr(new_question, attr)))
        for e in new_question.to_dict():
            setAll(e)
        db.session.add(new_question)
        db.session.commit()
        return jsonify({'code': 200})
    except Exception as e:
        print(e)
        return jsonify({'code': 400})

@app.route('/delete/<int:id>', methods=['DELETE'])
@token_required
def delete_by_id(current_user, id):
    question = Exam.query.get(id)
    if question:
        db.session.delete(question)
        db.session.commit()
        return jsonify({'code': 200})
    return jsonify({'code': 400, 'msg': 'Not found'})

@app.route('/get/', methods=['POST', 'GET'])
@app.route('/get/<int:page>', methods=['GET'])
def get(page=1):
    id = request.args.get('id', None)
    if id is not None:
        question = Exam.query.filter(Exam.id == id).first()
        if not question:
            return jsonify({'code': 404, 'msg': f'id {id} is not found', 'data': None})
        return jsonify({'code': 200, 'data': question.to_dict()})
    size = request.args.get('size', 15)
    page = request.args.get('page', page)
    if request.is_json:
        page = request.json.get('page', page)
        size = request.json.get('size', size)
    page = int(page)
    size = int(size)
    questions = Exam.query.order_by(Exam.id).paginate(page=page, per_page=size)
    data = [exam.to_dict() for exam in questions]
    return jsonify({'code': 200, 'data': data, 'length': len(data)})

@app.route('/search', methods=['GET'])
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
