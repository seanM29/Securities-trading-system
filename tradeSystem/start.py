#encoding=utf8
from flask import Flask,render_template,request,jsonify
import hashlib
app = Flask(__name__)
state=[]
@app.route('/',methods=['GET','POST'])
def index():
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




@app.route('/<x>',methods=['GET','POST'])
def page(x):
    ip = request.remote_addr
    if x=="signout":
        if ip in state:
            state.remove(ip)
        return render_template("user_login.html")
    global state

    if request.method=="GET":
        if not request.args:
            if ip not in state:
                if x in ["index.html", "index_v1.html", "index_searchTrade.html","new_account.html","user_login.html"]:
                    return render_template(x)
                else:
                    return render_template("no_login.html")
            return render_template(x)
        else:
            # if request.args.get("info"):
            #     return msg_dict[x]
            #校验
            if request.args.get("username")=="aaa" and request.args.get("password")=="aaa":
                #msg_dict[x] = "1;msg:success"
                if ip not in state:
                    state.append(ip)
                return "1;msg:success"
            elif request.args.get("username") and request.args.get("password"):
                return "0;msg:error"
                #msg_dict[x] = "0;msg:error"
            return render_template(x)#back=jsonify(request.args))#jsonify(request.args)
    elif request.method == "POST":
        # return request.form.items().__str__()
        #
        return jsonify(request.form)#render_template(x)#back=jsonify(request.form))

# @app.route('/index_v1.html',methods=['GET','POST'])
# def index_v1():

def to_md5(name):
    id = hashlib.md5()
    id.update(name.encode("utf-8"))
    id = id.hexdigest()
    return id

if __name__ == '__main__':
    app.run(debug=True,threaded=True)