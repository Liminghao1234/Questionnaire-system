import pymysql

db = pymysql.connect(host="localhost",user="root",password="123",database="questionnaire")
cursor = db.cursor()


def find_min_num(list):
    new_list = sorted(list)
    for i in range(0,len(new_list)):
        if i+1!=new_list[i]:
            return i+1
    return len(new_list)+1


def select_username(username):
    sql = 'select * from users where username="%s";'%username
    cursor.execute(sql)
    return len(cursor.fetchall())


def insert_users(username,password):
    sql = "select id from users"
    cursor.execute(sql)
    re = cursor.fetchall()
    # 获取插入id
    ids = []
    for r in re:
        ids.append(r[0])
    id = find_min_num(ids)
    insert_sql = 'insert into users values(%d,"%s","%s");'%(id,username,password)
    cursor.execute(insert_sql)
    db.commit()


def check_login(username,password):
    sql = 'select * from users where username="%s" and password="%s";'%(username,password)
    cursor.execute(sql)
    return len(cursor.fetchall())


def get_user_id(username):
    sql = 'select id from users where username="%s"'%username
    cursor.execute(sql)
    return cursor.fetchone()[0]


def create_questionnaire(username,questionnaire_name,description):
    sql = 'select questionnaire_id from questionnaire'
    cursor.execute(sql)
    re = cursor.fetchall()
    ids = []
    for r in re:
        ids.append(r[0])
    questionnaire_id = find_min_num(ids)
    user_id = get_user_id(username)
    insert_sql = 'insert into questionnaire values(%d,%d,"%s","%s",%d);'%(questionnaire_id,user_id,questionnaire_name,description,0)
    cursor.execute(insert_sql)
    db.commit()


def get_questionnaire_list(username):
    user_id = get_user_id(username)
    sql = "select * from questionnaire where user_id=%d"%user_id
    cursor.execute(sql)
    re = cursor.fetchall()
    return re


def get_question(questionnaire_id):
    # user_id = get_user_id(username)
    questionnaire_sql = 'select questionnaire_name,questionnaire_description,state,questionnaire_id from ' \
                        'questionnaire where questionnaire_id=%s;'%questionnaire_id
    cursor.execute(questionnaire_sql)
    questionnaire_inf = cursor.fetchone()
    question_inf = []
    question_sql = 'select question_id,question_type,question from question where questionnaire_id=%s'%questionnaire_id
    cursor.execute(question_sql)
    questions = cursor.fetchall()
    for question in questions:
        question_id = question[0]
        option_sql = "select option_id,question_option from question_option where question_id=%s"%question_id
        cursor.execute(option_sql)
        option_inf = cursor.fetchall()
        question_list = [question, option_inf]
        question_inf.append(question_list)
    return questionnaire_inf,question_inf

    # sql = 'select question_id,question,question_type,questionnaire_description,questionnaire_name ' \
    #       ' from question,questionnaire' \
    #       ' where questionnaire.questionnaire_id=question.questionnaire_id' \
    #       ' and questionnaire.user_id = %s' \
    #       ' and question.questionnaire_id = %s' \
    #       ' order by question_id;'%(user_id,questionnaire_id)
    # cursor.execute(sql)
    # re = cursor.fetchall()
    # option = []
    # for r in re:
    #     option_sql = "select option_id,question_option from question_option where question_id=%s"%r[0]
    #     cursor.execute(option_sql)
    #     option_re = cursor.fetchall()
    #     option_list = []
    #     for i in option_re:
    #         option_list.append(i)
    #     option.append(option_list)
    # length = min(len(re), len(option))
    # return re,option,length


def get_defalut_questionnaire(username):
    user_id = get_user_id(username)
    sql = 'select questionnaire_id from questionnaire where user_id=%s order by questionnaire_id;'%user_id
    cursor.execute(sql)
    re = cursor.fetchone()
    return re[0]


def insert_question(questionnaire_id,question_type,question,option):
    # 获取待插入的question_id，为最大的id值后面一位
    select_question_id_sql = 'select question_id from question order by question_id;'
    cursor.execute(select_question_id_sql)
    select_question_id = cursor.fetchall()
    length = len(select_question_id)
    question_id = select_question_id[length-1][0]+1
    # 插入question
    insert_question_sql='insert into question values(%s,%s,"%s","%s")'%(question_id,questionnaire_id,question_type,question)
    # print(insert_question_sql)
    cursor.execute(insert_question_sql)
    # db.commit()
    # 插入选项
    alp = 'A'
    for i in option:
        insert_option_sql = 'insert into question_option values("%s",%s,"%s");'%(alp,question_id,i)
        cursor.execute(insert_option_sql)
        # db.commit()
        alp = chr(ord(alp)+1)
    db.commit()


def delete_questionnaire(questionnaire_id):
    delete_questionnaire_sql = 'delete from questionnaire where questionnaire_id=%s;'%questionnaire_id
    delete_question_sql = 'delete from question where questionnaire_id=%s'%questionnaire_id
    select_question_id = 'select question_id from question where questionnaire_id=%s;'%questionnaire_id
    cursor.execute(select_question_id)
    # print(delete_question_sql)
    # print(delete_questionnaire_sql)
    re = cursor.fetchall()
    for question_id in re:
        delete_option_sql = 'delete from question_option where question_id=%s'%question_id[0]
        delete_choice_answer = 'delete from choice_answer where question_id=%s'%question_id[0]
        delete_completion_answer = 'delete from completion_answer where question_id=%s'%question_id[0]
        cursor.execute(delete_option_sql)
        cursor.execute(delete_choice_answer)
        cursor.execute(delete_completion_answer)
    cursor.execute(delete_question_sql)
    cursor.execute(delete_questionnaire_sql)
    db.commit()


def insert_completion(questionnaire_id,question_title):
    # 获取待插入的question_id，为最大的id值后面一位
    select_question_id_sql = 'select question_id from question order by question_id;'
    cursor.execute(select_question_id_sql)
    select_question_id = cursor.fetchall()
    length = len(select_question_id)
    question_id = select_question_id[length - 1][0] + 1
    # 插入选择题
    sql = 'insert into question values(%s,%s,"completion","%s");'%(question_id,questionnaire_id,question_title)
    cursor.execute(sql)
    db.commit()


def delete_question(question_id):
    delete_question_sql = 'delete from question where question_id=%s'%question_id
    delete_option_sql = 'delete from question_option where question_id=%s'%question_id
    cursor.execute(delete_question_sql)
    cursor.execute(delete_option_sql)
    db.commit()


def get_insert_num():
    sql = 'select num from completion_answer order by num desc'
    cursor.execute(sql)
    re = cursor.fetchone()
    if re:
        num = re[0]+1
    else:
        num = 1
    sql = 'select num from choice_answer order by num desc'
    cursor.execute(sql)
    re = cursor.fetchone()
    if re:
        num = max(num,re[0]+1)
    return num


def insert_choice(num,question_id,answer):
    sql = 'insert into choice_answer values(%s,%s,"%s")'%(num,question_id,answer)
    cursor.execute(sql)
    db.commit()


def insert_completion(num,question_id,answer):
    sql = 'insert into completion_answer values(%s,%s,"%s")'%(num,question_id,answer)
    cursor.execute(sql)
    db.commit()


def generate(questionnaire_id):
    sql = 'update questionnaire set state=1 where questionnaire_id=%s'%questionnaire_id
    cursor.execute(sql)
    db.commit()