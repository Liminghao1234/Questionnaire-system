from flask import *
from datetime import timedelta

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
app.config['SECRET_KEY'] = 'esTiw&1561#'
# 设置session的有效时间
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=3)

# login_manager.session_protection = 'strong'
# login_manager = LoginManager()
# login_manager.init_app(app)
