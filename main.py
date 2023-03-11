import sqlite3
import random
from flask import Flask, redirect, request, render_template, jsonify, url_for, session

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

remark_cont = 0  # 一言调用次数
pic_cont = 0  # 壁纸调用次数


@app.route('/')
def index():
    return render_template("index.html", remark_cont=remark_cont, pic_cont=pic_cont)


@app.route('/yan/')
def yan():
    host_name = request.host_url
    return render_template("yan.html", host_name=host_name)


@app.route('/api/yan/')
def yan_api():
    global remark_cont
    remark_cont += 1
    ty = request.args.get('type')
    if ty == "f":
        data = get_yan(r'data/yan.db', "yan_f")
    elif ty == "y":
        data = get_yan(r'data/yan.db', "yan_y")
    elif ty == 'i':
        data = get_yan(r'data/yan.db', "yan_i")
    else:
        data = get_yan(r'data/yan.db', random.choice(["yan_f", "yan_y", "yan_i"]))
    data = random.choice(data)
    en = request.args.get('encode')
    if en == 'js':
        return 'function yan(){document.write("%s");}' % data[1].strip()
    yan_dic = {"id": data[0], "yan": data[1].strip(), "from_who": data[2], "come_from": data[3], "length": data[4],
               "type": data[5]}
    return jsonify(yan_dic)


@app.route('/pic/')
def pic():
    host_name = request.host_url
    return render_template("pic.html", host_name=host_name)


@app.route('/api/pic/')
def pic_api():
    global pic_cont
    pic_cont += 1
    data = get_yan(r'data/pic.db', 'pic_data')
    pic_data = random.choice(data)[2]
    en = request.args.get('encode')
    if en == 'js':
        return 'function pic(){var obj=document.getElementById("pic");obj.innerHTML="<img src="%s"/> ";}' % pic_data
    return redirect(pic_data)


# 连接数据库获取数据
def get_yan(db, db_name):
    try:
        conn = sqlite3.connect(db)
        cour = conn.cursor()
        sql = f'select * from {db_name}'
        cour.execute(sql)
        data = cour.fetchall()
        cour.close()
        conn.close()
        return data
    except EOFError as e:
        print('数据库连接失败')


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
