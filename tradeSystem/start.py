#encoding=utf8
from flask import Flask,render_template,request,jsonify
import hashlib
app = Flask(__name__)
state=[]
user_mapping={}
@app.route('/',methods=['GET','POST'])
def staff_login():
    if request.method=="GET":
        if not request.args:
            return render_template("staff_login.html")
        else:
            user_type=request.args.get("RadioButtonList")
            if user_type==u"证券账户管理员":
            #校验
                if request.args.get("username")=="aaa" and request.args.get("password")==to_md5("aaa"):
                    return "1;msg:success"
                    #return render_template("index.html")
                else:
                    return "0;msg:error"
                    #return render_template("staff_login.html")
            elif user_type==u"交易系统管理员":
            #校验
                if request.args.get("username")=="bbb" and request.args.get("password")==to_md5("bbb"):
                    return "1;msg:success"
                    #return render_template("index_searchTrade.html")
                else:
                    return"0;msg:error"
                    #return render_template("staff_login.html")
           #render_template("staff_login.html")#前端保证
# elif request.method == "POST":
# # return request.form.items().__str__()
# #
# return jsonify(request.form)




@app.route('/<x>',methods=['GET','POST'])
def page(x):
    fuc = x.split(".html")[0]
    return eval(fuc)()

def change_password():
    global state
    global user_mapping
    ip = request.remote_addr
    if ip in state:
        if request.method == "GET":
            if request.args.get("password") and request.args.get("confirm"):
                if request.args.get("password") != to_md5("aaa") and request.args.get("confirm") != to_md5("aaa"):
                    return "1;msg:success"
                else:
                    return "0;msg:error"
            else:
                return render_template("change_password.html")
    else:
        return render_template("no_login.html")

def change_information():
    global state
    global user_mapping
    ip = request.remote_addr
    information={"name":"name"}
    if ip in state:
        if request.method == "GET":
            if request.form.get("form"):
                if request.form.get("form")!=information:
                    return "1;msg:success"
                else:
                    return "0;msg:error"
            else:
                return render_template("change_information.html",form=information)
    else:
        return render_template("no_login.html")

def change_capital_account():
    global state
    global user_mapping
    ip = request.remote_addr
    capital_account={}
    if ip in state:
        if request.method == "GET":
            if request.form.get("form"):
                if request.form.get("form") != capital_account:
                    return "1;msg:success"
                else:
                    return "0;msg:error"
            else:
                return render_template("change_capital_account.html", form=capital_account)
    else:
        return render_template("no_login.html")

##暂时不需要预先传入参数


def drop_account():
    global state
    global user_mapping
    ip = request.remote_addr
    if ip in state:
        if request.method == "GET":
            if request.args.get("password") and request.args.get("confirm"):
                if request.args.get("password") != to_md5("aaa") and request.args.get("confirm") != to_md5("aaa"):
                    return "1;msg:success"
                else:
                    return "0;msg:error"
            else:
                return render_template("drop_account.html")
    else:
        return render_template("no_login.html")

def user_login():
    global state
    global user_mapping
    ip = request.remote_addr
    if request.method=="GET":
        if request.args.get("username") == "aaa" and request.args.get("password") == to_md5("aaa"):
            if ip not in state:  # 单ip处理单用户
                state.append(ip)
            user_mapping[ip] = request.args.get("username")
            return "1;msg:success"
        elif request.args.get("username") and request.args.get("password"):
            return "0;msg:error"
        else:
            return render_template("user_login.html")

def signout():
    global state
    global user_mapping
    ip = request.remote_addr
    if ip in state:
        state.remove(ip)
        user_mapping.pop(ip)
    return render_template("user_login.html")

def index():
    global state
    global user_mapping
    ip = request.remote_addr
    if request.args.get("close"):
        if ip in state:
            state.remove(ip)
            user_mapping.pop(ip)
        return "leave?"
    else:
        return render_template("index.html")

def loss_account():
    global state
    global user_mapping
    ip = request.remote_addr
    if ip in state:
        if request.method == "GET":
            if request.args.get("password") and request.args.get("confirm"):
                if request.args.get("password") != to_md5("aaa") and request.args.get("confirm") != to_md5("aaa"):
                    return "1;msg:success"
                else:
                    return "0;msg:error"
            else:
                return render_template("loss_account.html")
    else:
        return render_template("no_login.html")

def new_account():
    if request.method == "GET":
        if request.args.get("password") and request.args.get("confirm"):#todo 验证
            if request.args.get("password") != to_md5("aaa") and request.args.get("confirm") != to_md5("aaa"):
                return "1;msg:success"
            else:
                return "0;msg:error"
        else:
            return render_template("new_account.html")


def renew_account():
    global state
    global user_mapping
    ip = request.remote_addr
    if ip in state:
        if request.method == "GET":
            if request.args.get("password") and request.args.get("confirm"):
                if request.args.get("password") != to_md5("aaa") and request.args.get("confirm") != to_md5("aaa"):
                    return "1;msg:success"
                else:
                    return "0;msg:error"
            else:
                return render_template("renew_account.html")
    else:
        return render_template("no_login.html")

def index_searchTrade():
    return render_template("index_searchTrade.html")

def index_v1():
    return render_template("index_v1.html")

def projects():
    return render_template("projects.html")

def to_md5(name):
    id = hashlib.md5()
    id.update(name.encode("utf-8"))
    id = id.hexdigest()
    return id

if __name__ == '__main__':
    app.run(debug=True,threaded=True)