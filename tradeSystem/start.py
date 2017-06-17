#encoding=utf8
from flask import Flask,render_template,request#,jsonify
from database import *
import json
import hashlib
from flask_cors import *
app = Flask(__name__)
CORS(app,supports_credentials=True)
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
                ret=loginStockUserManager(request.args.get("username"),request.args.get("password"))
                if ret["status"]:
                    return "1;%s"%ret["error"]
                    #return render_template("index.html")
                else:
                    return "0;%s"%ret["error"]
                    #return render_template("staff_login.html")
            elif user_type==u"交易系统管理员":
                ret = loginStockQueryManager(request.args.get("username"), request.args.get("password"))
                if ret["status"]:
                    return "1;%s"%ret["error"]
                    # return render_template("index.html")
                else:
                    return "0;%s"%ret["error"]
            #校验

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

def test():
    # if ret1["status"] and ret2["status"] and ret3["status"] and ret4["status"]:
    #     return "1;success"
    # else:
    #     return "0;error"
    return render_template("test.html")
        #ret1=delStockUser('1234567890')
    #ret2=delStockUser('0123456789')

def get_type():
    if request.method=="GET":
        ret=getStockQueryManager(request.args.get("id"))
        if ret["status"]:
            ret["result"].pop("id")
        return json.dumps(ret)

def want_sell():
    if request.method=="GET":
        ret=frozeStock(request.args.get("id"),request.args.get("stock_id"),request.args.get("amount"))
        if ret["status"]:
            return "1;%s"%ret["error"]
        else:
            return "0;%s"%ret["error"]

def transaction():
    if request.method=="GET":
        ret=mvStock(request.args.get("id_1"),request.args.get("id_2"),request.args.get("stock_id"),request.args.get("amount"))
        if ret["status"]:
            return "1;%s"%ret["error"]
        else:
            return "0;%s"%ret["error"]

def check():
    if request.method=="GET":
        if request.args.get("id") and request.args.get("password"):
            ret=loginStockUser(request.args.get("id"),request.args.get("password"))
            return json.dumps(ret)

def information():
    if request.method=="GET":
        if request.args.get("id"):
            ret1=getStockUser(request.args.get("id"))
            ret2=getFundAccount(request.args.get("id"))
            ret3=getStocks(request.args.get("id"))
            if ret1["status"]:
                if ret2["status"]:
                    if ret3["status"]:
                        fund_list=[x["fund_id"] for x in ret2["result"]]
                        stock_list=[x  for x in ret3["result"] if x.pop("id")]
                        ret1["result"].pop("fund")
                        ret1["result"]["fund_list"]=fund_list
                        ret1["result"]["stock_list"]=stock_list
                        return json.dumps(ret1)
                    else:
                        ret3["result"]=None
                        return json.dumps(ret3)
                else:
                    ret2["result"]=None
                    return json.dumps(ret2)
            else:
                ret1["result"]=None
                return json.dumps(ret1)

def change_password():
    global state
    global user_mapping
    ip = request.remote_addr
    if ip in state:
        if request.method == "GET":
            if request.args.get("password"):
                id = user_mapping[ip]
                ret=getStockUser(id)
                if ret['status']:
                    if ret["result"]["password"]==request.args.get("password"):
                        return "0;Same password"
                    else:
                        ret_ret = updStockUser(id,{"password": request.args.get("password")})
                        if ret_ret["status"]:
                            return "1;%s" % ret_ret["error"]
                        else:
                            return "0;%s" % ret_ret["error"]
                else:
                    return "0;%s" % ret["error"]
            else:
                return render_template("change_password.html")
    else:
        return render_template("no_login.html")

def change_information():
    global state
    global user_mapping
    ip = request.remote_addr
    if ip in state:
        id = user_mapping[ip]
        ret = getStockUser(id)
        info=ret["result"]
        info.pop("available")
        info.pop("fund")
        info.pop("create_time")
        info.pop("id")
        info.pop("password")
        # for x in info:
        #     if info[x]==None:
        #         info[x]=""
        #info={"name":"受到激发了"}
        if request.method == "GET":
            if ret["status"]:
                return render_template("change_information.html",form=json.dumps(info))
        elif request.method=="POST":
            form=request.form.to_dict()
            if form:
                form["sex"]=int(form["sex"])
                form["degree"]=int(form["degree"])
                print form
                print info
                if form!=info:
                    ret_ret=updStockUser(id,form)
                    if ret_ret["status"]:
                        return "1;%s"%ret_ret["error"]
                    else:
                        return "0;%s"%ret_ret["error"]
                else:
                    return "0;Same information"
            else:
                return render_template("change_information.html", form=json.dumps(info))
    else:
        return render_template("no_login.html")

def change_capital_account():
    global state
    global user_mapping
    ip = request.remote_addr

    if ip in state:
        id=user_mapping[ip]
        ret=getFundAccount(id)
        if ret["status"]:
            capital_account =[x["fund_id"] for x in ret["result"]]
            if request.method == "GET":
                account=[]
                if request.args.get("account1"):
                    account.append(request.args.get("account1"))
                    if request.args.get("account2"):
                        account.append(request.args.get("account2"))
                    if request.args.get("account3"):
                        account.append(request.args.get("account3"))
                    if account != capital_account:
                        add=[x for x in account if x not in capital_account]
                        de=[x for x in capital_account if x not in account]
                        print add,de
                        ret_add=[addFundAccount(id,x)["status"] for x in add]
                        ret_de=[delFundAccount(id,x)["status"] for x in de]
                        print ret_add,ret_de
                        if False not in  ret_de and False not in ret_add:
                            return "1;msg:success"
                        else:
                            return "0;msg:error"
                    else:
                        return "0;Same account"
                else:
                    return render_template("change_capital_account.html", form=json.dumps(capital_account))
    else:
        return render_template("no_login.html")

def drop_account():
    global state
    global user_mapping
    ip = request.remote_addr
    if ip in state:
        if request.method == "GET":
            if request.args.get("id_number"):
                id = user_mapping[ip]
                ret = getStockUser(id)
                if ret['status']:
                    if request.args.get("id_number") == ret["result"]["id_number"]:
                        ret_ret = delStockUser(id)
                        if ret_ret['status']:
                            state.remove(ip)
                            user_mapping.pop(ip)
                            return "1;%s" % ret_ret["error"]
                        else:
                            return "0;%s" % ret_ret["error"]
                    else:
                        return "0;Incorrect id_number"
                else:
                    return "0;%s" % ret["error"]
            else:
                return render_template("drop_account.html")
    else:
        return render_template("no_login.html")
def user_login():
    global state
    global user_mapping
    ip = request.remote_addr
    if request.method=="GET":
        if request.args.get("username") and request.args.get("password"):
            ret = loginStockUser(request.args.get("username"), request.args.get("password"))
            if ret["status"]:
                if ip not in state:  # 单ip处理单用户
                    state.append(ip)
                user_mapping[ip] = request.args.get("username")
                return "1;%s" % ret["error"]
                # return render_template("index.html")
            else:
                return "0;%s" % ret["error"]
        else:
            return render_template("user_login.html")

def signout():
    global state
    global user_mapping
    ip = request.remote_addr
    if request.method=="GET":
        if ip in state:
            state.remove(ip)
            user_mapping.pop(ip)
            return render_template("user_login.html")
        else:
            return render_template("no_login.html")

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
            if request.args.get("id_number"):
                id=user_mapping[ip]
                ret=getStockUser(id)
                if ret['status']:
                    if request.args.get("id_number")==ret["result"]["id_number"]:
                        ret_ret=frozeStockUser(id)
                        if ret_ret['status']:
                            return "1;%s"%ret_ret["error"]
                        else:
                            return "0;%s"%ret_ret["error"]
                    else:
                        return "0;Incorrect id_number"
                else:
                    return "0;%s"%ret["error"]
            else:
                return render_template("loss_account.html")
    else:
        return render_template("no_login.html")

def new_account():
    if request.method == "GET":
            return render_template("new_account.html")
    elif request.method=="POST":
        form=request.form.to_dict()
        if form:
            form["sex"] = int(form["sex"])
            form["degree"] = int(form["degree"])
            ret=addStockUser(form['id'],form)
            if ret["status"]:
                if form.get("account1"):
                    ret1=addFundAccount(form['id'],form.get("account1"))
                    if not ret1["status"]:
                        return "0;%s"%ret1["error"]
                if form.get("account2"):
                    ret1=addFundAccount(form['id'],form.get("account2"))
                    if not ret1["status"]:
                        return "0;%s"%ret1["error"]
                if form.get("account3"):
                    ret1=addFundAccount(form['id'],form.get("account3"))
                    if not ret1["status"]:
                        return "0;%s"%ret1["error"]
                return "1;%s" % ret["error"]
                # return render_template("index.html")
            else:
                return "0;%s" % ret["error"]


        else:
            return render_template("new_account.html")



def renew_account():
    global state
    global user_mapping
    ip = request.remote_addr
    if ip in state:
        if request.method == "GET":
            if request.args.get("id_number"):
                id = user_mapping[ip]
                ret = getStockUser(id)
                if ret['status']:
                    if request.args.get("id_number") == ret["result"]["id_number"]:
                        ret_ret = unfrozeStockUser(id)
                        if ret_ret['status']:
                            return "1;%s" % ret_ret["error"]
                        else:
                            return "0;%s" % ret_ret["error"]
                    else:
                        return "0;Incorrect id_number"
                else:
                    return "0;%s" % ret["error"]
            else:
                return render_template("renew_account.html")
    else:
        return render_template("no_login.html")

def index_searchTrade():
    return render_template("index_searchTrade.html")

def index_v1():
    return render_template("index_v1.html")

def on_login():
    return render_template("on_login.html")

def projects():
    return render_template("projects.html")

def to_md5(name):
    id = hashlib.md5()
    id.update(name.encode("utf-8"))
    id = id.hexdigest()
    return id

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,threaded=True)
