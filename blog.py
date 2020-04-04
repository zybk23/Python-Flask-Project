from flask import Flask ,render_template,redirect,request,flash,logging,session,url_for

from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,validators,PasswordField,RadioField,SelectField
from passlib.hash import sha256_crypt
from functools import wraps


class RegisterForm(Form):
    name= StringField("",validators=[validators.Length(min=4 , max=25)])
    username=StringField("",validators=[validators.Length(min=4 , max=25)])
    email=StringField("",validators=[validators.Email(message="Lütfen geçerli bir email adresi giriniz ")])
    password=PasswordField("", validators=[validators.DataRequired(message="Lütfen bir parola belirleyiniz."),
    validators.EqualTo( fieldname="confirm",message="Parolanız Uyuşmuyor")
    
    ])
    confirm=PasswordField("")
    sex=StringField("")
    date=StringField("")
class LoginForm(Form):
    username=StringField("")
    password=PasswordField("")
    

app=Flask(__name__,static_url_path="/static")
app.secret_key="taha"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "ybblog"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql=MySQL(app)
@app.route("/")

def index():
    numbers=[1,2,3,4,5,6]

    return render_template("index.html",numbers=numbers)


@app.route("/about")
def about():

    return render_template("about.html")



@app.route("/article/<string:id>")

def detail(id):

    return "Artıcle Id:"+id

@app.route("/register" , methods=["GET","POST"])

def register():

    form=RegisterForm(request.form)

    if request.method=="POST" and form.validate():

        name=form.name.data
        username=form.name.data
        email=form.username.data
        sex=form.sex.data
        date=form.date.data
        password=sha256_crypt.encrypt(form.password.data)

        cursor=mysql.connection.cursor()

        sorgu=("insert into users(name,username,email,sex,date,password) VALUES(%s,%s,%s,%s,%s,%s)")

        cursor.execute(sorgu,(name,username,email,sex,date,password))

        mysql.connection.commit()

        cursor.close()
        flash("Başarıyla kayıt oldunuz","success")
        return redirect(url_for("login"))
    else:

        return render_template("register.html",form=form)

@app.route("/login",methods=["GET","POST"])

def login():

    form=LoginForm(request.form)

    if request.method=="POST":
        username=form.username.data
        password_entered=form.password.data

        cursor=mysql.connection.cursor()

        sorgu=("select * from users where username=%s")

        result=cursor.execute(sorgu,(username,))

        if result>0:
            data=cursor.fetchone()
            real_password=data["password"]
            if sha256_crypt.verify(password_entered,real_password):
                flash("Başarıyla Giriş yaptınız","success")
                return redirect(url_for("index"))
            else:
                flash("Parolanız yanlış lütfen tekrar giriniz..","danger")
                return redirect(url_for("login"))
        else:
            flash("Böyle bir kullanıcı bulunmuyor","danger")
            return redirect(url_for("login"))


    else:
        return render_template("login.html",form=form)


if __name__ == "__main__":
    app.run(debug=True)