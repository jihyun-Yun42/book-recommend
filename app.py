from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

# mongoDB연결코드
from pymongo import MongoClient
import certifi
ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.ynnqkbk.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile = ca)
db = client.book_recommend

# 크롤링을 위한 코드
import requests
from bs4 import BeautifulSoup

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')


@app.route('/')
def home():
   return render_template('index.html')
 

# 글작성 페이지
@app.route("/write", methods=["POST"])
def write():
    url = request.form['url']
    nicname = request.form['nicname']
    comment = request.form['comment']

    doc = {
        'url':url,
        'comment':comment,
        'nicname':nicname
    }
    db.write.insert_one(doc)
    return jsonify({'msg': '작성완료'})



# 상세페이지
@app.route("/detailpage/like", methods=["POST"])
def detailpage_like():
    sample_receive = request.form['sample_give']
    return jsonify({'msg': 'POST(기록) 연결 완료!'})


@app.route("/detailpage", methods=["GET"])
def detailpage_get():
    return jsonify({'msg': 'POST(기록) 연결 완료!'})


@app.route("/detailpage/delete", methods=["POST"])
def detailpage_delete():
    sample_receive = request.form['sample_give']
    return jsonify({'msg': 'POST(기록) 연결 완료!'})



# 메인페이지
@app.route("/mainpage/login", methods=["POST"])
def mainpage_login():
    sample_receive = request.form['sample_give']
    return jsonify({'msg': 'POST(기록) 연결 완료!'})


@app.route("/mainpage", methods=["GET"])
def mainpage_get():
    return jsonify({'msg': 'POST(기록) 연결 완료!'})


# 회원가입페이지
@app.route("/join", methods=["POST"])
def join():
    sample_receive = request.form['sample_give']
    return jsonify({'msg': 'POST(기록) 연결 완료!'})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5001, debug=True)