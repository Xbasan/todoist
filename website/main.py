from flask import (
           Flask,
           render_template,
           request,
           jsonify
)

from db import (
           list_json,
           delete_list,
           select_list,
           inser_list
)

app = Flask(__name__)


def save_list(list_json={
           "title": "",
           "text": "",
           "_date":""
}):
           title = list_json["title"]
           text = list_json["text"]
           date = list_json["_date"]
           inser_list(title=title, text=text, date=date)

    
def readings_list():
           return list_json(select_list())


@app.route('/',
           methods=['GET'])
def index():
           return render_template('index.html', lists=readings_list())

@app.route('/', 
           methods=["POST"])
def index_post():
           if request.form.get("id") :
                      
                      id = request.form.get("id")

                      delete_list(id=id)

                      return render_template("index.html",lists=readings_list())
           else:
                      title = request.form.get("title")
                      text = request.form.get("text")
                      date = request.form.get("date")

                      save_list(list_json={
                                            "title": title,
                                            "text": text,
                                            "_date": date                      
                                }
                      )

           # return render_template('eror.html')
           return render_template("index.html",lists=readings_list()) 


@app.route('/api',
           methods=['GET', 'POST'])
def api():
           ret_list = request.args.get("list")
           insert = request.args.get("insert")
           delet = request.args.get("del")

           if ret_list is not None:
                      return jsonify(readings_list())
           
           if insert is not None:
                      content = request.json

                      title = content["title"]
                      text = content["text"]
                      date = content["_date"]
                      
                      save_list(list_json={
                                           "title": title,
                                           "text": text,
                                           "_date": date 
                                })

                      return jsonify({"status":"true"})
             
           if delet is not None:
                      content = request.json
                      try:
                                 id = content["id"]
                                 delete_list(id)

                                 return jsonify({"status":"true"})
                      except:
                                 return jsonify({"status":"false"})
           

if __name__ == '__main__':
           app.run(debug=True,
                   host='0.0.0.0') # 2000
