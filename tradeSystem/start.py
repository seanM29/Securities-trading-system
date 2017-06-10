#encoding=utf8
from flask import Flask,render_template,request,jsonify
app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method=="GET":
        print request.args.get("RadioButtonList1")
        if not request.args:
            return render_template("staff_login.html")
        elif request.args.get("RadioButtonList1")==u"证券账户管理员":
            return render_template("index.html")
        else:
            return render_template("index_searchTrade.html")


@app.route('/<x>',methods=['GET','POST'])
def page(x):
    if request.method=="GET":
        if not request.args:
            return render_template(x)
        else:
            if request.args.get("info"):
                return "0;msg:error"
            return render_template(x)#back=jsonify(request.args))#jsonify(request.args)
    elif request.method == "POST":
        # return request.form.items().__str__()
        return jsonify(request.form)#render_template(x)#back=jsonify(request.form))

# @app.route('/index_v1.html',methods=['GET','POST'])
# def index_v1():



if __name__ == '__main__':
    app.run(debug=True,threaded=True)