from __init__ import *
from Model import *


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/index")
def home():
    return redirect("/")


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        if check_login(username, password):
            session["username"] = username
            return redirect("/question_list")
        else:
            erro = "Incorrect username or password!"
            return render_template("login.html", erro=erro)
    return render_template("login.html")


@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form["username"]
        if request.form["password1"] != request.form["password2"]:
            erro = "The two passwords do not match"
            return render_template("signup.html", erro=erro)
        else:
            password = request.form["password1"]
            if select_username(username):
                erro = "Username already exists"
                return render_template("signup.html", erro=erro)
            else:
                insert_users(username, password)
                return redirect("/login")

    return render_template("signup.html")


@app.route("/question_list", methods=['POST', 'GET'])
def question_list():
    username = session.get("username")
    questionnaire_list = get_questionnaire_list(username)
    questionnaire_id = get_defalut_questionnaire(username)
    # 获取问卷
    if request.args.get('questionnaire_id'):
        questionnaire_id = request.args.get('questionnaire_id')
    # questions, options, length = get_question(username, questionnaire_id)
    questionnaire_ifo,question_ifo = get_question(questionnaire_id)
    # 添加问卷
    if request.form.get("questionnaire_name") and request.form.get("description"):
        questionnaire_name = request.form.get("questionnaire_name")
        description = request.form.get("description")
        create_questionnaire(username, questionnaire_name, description)
        # print(questionnaire_name+"  "+description)
        return redirect("/question_list?questionnaire_id="+questionnaire_id)
    # 添加问题
    if request.form.get("question_type") and request.form.get("question_title"):
        question_type = request.form.get("question_type")
        question_title = request.form.get("question_title")
        insert_options = []
        i = 1
        # 如果为单选
        if question_type == "single choice":
            while request.form.get("single" + str(i)):
                value = request.form.get("single" + str(i))
                insert_options.append(value)
                i += 1
            insert_question(questionnaire_id,"single choice",question_title,insert_options)
            return redirect("/question_list?questionnaire_id="+questionnaire_id)
        # 如果为多选
        elif question_type == "multiple choice":
            while request.form.get("multiple" + str(i)):
                value = request.form.get("multiple" + str(i))
                insert_options.append(value)
                i += 1
            insert_question(questionnaire_id, "multiple choice", question_title, insert_options)
            return redirect("/question_list?questionnaire_id=" + questionnaire_id)
        # 如果为填空
        elif question_type == "completion":
            insert_completion(questionnaire_id,question_title)
            return redirect("/question_list?questionnaire_id=" + questionnaire_id)

    return render_template("question_list.html", username=username, questionnaire_list=questionnaire_list,
                           questionnaire_ifo=questionnaire_ifo,question_ifo=question_ifo)


@app.route("/visual_tool", methods=['POST', 'GET'])
def visual_tool():
    return render_template("visual_tool.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# 删除问卷
@app.route("/delete_questionnaire", methods=['POST', 'GET'])
def delete_questionnaire_route():
    questionnaire_id = request.args.get("questionnaire_id")
    # print(questionnaire_id)
    delete_questionnaire(questionnaire_id)
    return redirect("/question_list")


# 删除问题
@app.route("/delete_question", methods=['POST', 'GET'])
def delete_question_route():
    question_id = request.args.get("question_id")
    questionnaire_id = request.args.get("questionnaire_id")
    print(question_id+"   "+questionnaire_id)
    delete_question(question_id)
    return redirect("/question_list?questionnaire_id=" + questionnaire_id)


@app.route("/fill_in_questionnaire", methods=['POST', 'GET'])
def fill_in_questionnaire():
    questionnaire_id = request.args.get('questionnaire_id')
    questionnaire_ifo,question_ifo = get_question(questionnaire_id)
    num = get_insert_num()
    for question in question_ifo:
        name = "question"+str(question[0][0])
        if question[0][1] == "single choice":
            if request.form.get(name):
                answer = request.form.get(name)
                insert_choice(num,question[0][0],answer)
        elif question[0][1] == "multiple choice":
            if request.form.getlist(name):
                answer = request.form.getlist(name)
                for i in answer:
                    insert_choice(num, question[0][0],i)
        elif question[0][1] == "completion":
            if request.form.get(name):
                answer = request.form.get(name)
                insert_completion(num,question[0][0],answer)

    return render_template("fill_in_questionnaire.html",questionnaire_ifo=questionnaire_ifo,question_ifo=question_ifo)


@app.route("/generate_questionnaire", methods=['POST', 'GET'])
def generate_questionnaire():
    questionnaire_id = request.args.get('questionnaire_id')
    generate(questionnaire_id)
    return redirect("/question_list?questionnaire_id=" + questionnaire_id)


@app.route("/test", methods=['POST', 'GET'])
def test():
    if request.form.get("my_select"):
        select = request.form.get("my_select")
        print(select)
        i = 1
        while request.form.get("single" + str(i)):
            value = request.form.getlist("single" + str(i))
            print(value)
            i += 1
    return render_template("test.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
