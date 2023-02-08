import urllib.request
import certifi
from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify
SECRET_KEY = 'book'

app = Flask(__name__)

# mongoDB연결코드
ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.ynnqkbk.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.book_recommend


@app.route('/')
def home():
    return render_template('index.html')


# 회원가입페이지
@app.route("/api/signup", methods=["POST"])
def api_register():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    pw2_receive = request.form['pw2_give']
    nick_receive = request.form['nick_give']
    mail_receive = request.form['mail_give']
    address_receive = request.form['address_give']
    juso_receive = request.form['juso_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    pw2_hash = hashlib.sha256(pw2_receive.encode('utf-8')).hexdigest()

    result = db.join.find_one({'id': id_receive})
    if result is not None:
        return jsonify({'result': 'fail', 'msg': '이미 존재하는 ID입니다!'})

    else:
        db.join.insert_one({
            'id': id_receive,
            'pw': pw_hash,
            'pw2': pw2_hash,
            'nick': nick_receive,
            'mail': mail_receive,
            'address': address_receive,
            'juso': juso_receive
        })
        return jsonify({'result': 'success'})



#로그인
@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    result = db.join.find_one({'id': id_receive, 'pw': pw_hash})

    if result is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/api/isAuth', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        userinfo = db.join.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'nickname': userinfo['nick']})
    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})


        

@app.route('/writepage')
def writepage():
    return render_template('write.html')


# 상세페이지 이동
@app.route('/detail/<int:num>', methods=["GET"])
def detail(num):
    title = db.write.find_one({'num':num})['title']
    image = db.write.find_one({'num':num})['image']
    comment = db.write.find_one({'num':num})['comment']
    author = db.write.find_one({'num':num})['author']
    nicname = db.write.find_one({'num':num})['nicname']
    num = db.write.find_one({'num':num})['num']

    return render_template('detailpage.html',num=num, title=title, image=image, comment=comment, author=author, nicname=nicname)






# 글작성 페이지
@app.route("/write", methods=["POST"])
def write():
    nicname = request.form['nicname']
    comment = request.form['comment']
    image = request.form['image']
    title = request.form['title']
    author = request.form['author']
    book_list = list(db.write.find({},{'_id':False}))
    num = len(book_list) + 1
    if nicname == '' or comment == '':
        return jsonify({'msgnot': '내용을 입력해주세요'})
    else:
        doc = {
            'num':num,
            'image': image,
            'comment': comment,
            'nicname': nicname,
            'title': title,
            'author': author
        }
        db.write.insert_one(doc)
    return jsonify({'msg': '작성완료'})


# 상세페이지


@app.route("/detailpage", methods=["GET"])
def detail_comments():
    comment_list = list(db.bookrec.find({}, {'_id': False}))
    return jsonify({'comments': comment_list})


@app.route("/detailpage", methods=["POST"])
def detail_post():
    nickname_receive = request.form['nickname_give']
    comment_receive = request.form['comment_give']

    doc = {
        'nickname': nickname_receive,
        'comment': comment_receive
    }

    db.bookrec.insert_one(doc)
    return jsonify({'msg': '댓글작성 완료!'})


@app.route("/detailpage", methods=["DELETE"])
def detail_delete():
    num = request.form['num']
    db.write.delete_one({'num':int(num)})
    return jsonify({'msg': '삭제 완료!'})


# 수정페이지로 이동
@app.route('/updatepage/<int:num>')
def updatepage(num):
    title = db.write.find_one({'num':num})['title']
    image = db.write.find_one({'num':num})['image']
    comment = db.write.find_one({'num':num})['comment']
    author = db.write.find_one({'num':num})['author']
    nicname = db.write.find_one({'num':num})['nicname']
    num = db.write.find_one({'num':num})['num']

    return render_template('update.html',num=num, title=title, image=image, comment=comment, author=author, nicname=nicname)

# 수정기능
@app.route("/updatepage", methods=["PUT"])
def detail_edit():
    num = request.form['num']
    title = request.form['title']
    nicname = request.form['nicname']
    comment = request.form['comment']
    image = request.form['image']
    author = request.form['author']

    db.write.update_one({'num':int(num)},{'$set':{'title':title}})
    db.write.update_one({'num':int(num)},{'$set':{'nicname':nicname}})
    db.write.update_one({'num':int(num)},{'$set':{'comment':comment}})
    db.write.update_one({'num':int(num)},{'$set':{'image':image}})
    db.write.update_one({'num':int(num)},{'$set':{'author':author}})

    return jsonify({'msg': '수정 완료!'})


# 메인페이지
@app.route("/mainpage/login", methods=["POST"])
def mainpage_login():
    sample_receive = request.form['sample_give']
    return jsonify({'msg': 'POST(기록) 연결 완료!'})


@app.route("/showbook", methods=["GET"])
def book_card_get():
    book_card = list(db.write.find({}, {'_id': False}))
    return jsonify({'book': book_card})


@app.route("/mainpage/detail", methods=["POST"])
def mainpage_detail():
    user = db.users.find_one({'name': 'bobby'})
    return jsonify({'msg': 'POST(기록) 연결 완료!'})


# 회원가입페이지
@app.route("/join", methods=["POST"])
def join():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    pw_pw_receive = request.form['pw_pw_give']
    nick_receive = request.form['nick_give']
    mail_receive = request.form['mail_give']
    address_receive = request.form['address_give']
    juso_receive = request.form['juso_give']

    doc = {
        'id': id_receive,
        'pw': pw_receive,
        'pw_pw': pw_pw_receive,
        'nick': nick_receive,
        'mail': mail_receive,
        'address': address_receive,
        'juso': juso_receive
    }

    db.join.insert_one(doc)

    return jsonify({'msg': 'POST(기록) 연결 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5002, debug=True)
