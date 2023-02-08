import urllib.request
import certifi
from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

# mongoDB연결코드
ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.ynnqkbk.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.book_recommend


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/signin')
def signin():
    return render_template('sign-in.html')


@app.route('/detail/<int:num>', methods=["GET"])
def detail(num):
    title = db.write.find_one({'num':num})['title']
    image = db.write.find_one({'num':num})['image']
    comment = db.write.find_one({'num':num})['comment']
    author = db.write.find_one({'num':num})['author']
    nicname = db.write.find_one({'num':num})['nicname']
    num = db.write.find_one({'num':num})['num']

    return render_template('detailpage.html',num=num, title=title, image=image, comment=comment, author=author, nicname=nicname)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/writepage')
def writepage():
    return render_template('write.html')


@app.route('/updatepage/<int:num>')
def updatepage(num):
    num = db.write.find_one({'num':num})['num']
    return render_template('update.html')



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


@app.route("/detailpage/edit", methods=["PUT"])
def detailpage_edit():
    sample_receive = request.form['sample_give']
    return jsonify({'msg': 'POST(기록) 연결 완료!'})


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
