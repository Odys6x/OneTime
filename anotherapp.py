from Problem import *
from adform import *
from myform import *
from Create import *
from flask import *
from user import *
from forms import *
from wtforms import Form, StringField, BooleanField, TextAreaField, RadioField, SelectField, validators, PasswordField, \
    DateField, SubmitField, \
    IntegerField, FileField, SelectMultipleField, widgets, DateTimeField

from wtforms.validators import DataRequired
from datetime import datetime

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='dev'
)




@app.route('/')
def home():
    return render_template('Noaccount.html')


@app.route('/report', methods=('GET', 'POST'))
def report():
    form = RForm(request.form)
    if request.method == 'POST':
        problem = form.problem.data
        description = form.description.data
        location = form.location.data
        date     = form.date.data
        error = ""


        if problem == "":
            error = 'problem is required.'
        if description == "":
            error = 'Description is required.'
        if location == "":
            error = 'Location is required'
        if date == "":
            error = 'Date is required'

        if error == "":

            problems.create_request(problem, description, location ,date)



            return redirect(url_for('homepage'))
        flash(error)
    return render_template('Userpage.html', form=form)




@app.route('/admin')
def viewproblems():


    y = get_problems()



    return render_template('Adminpage.html', problems=y)









@app.route('/viewcomment')
def results():


    o = get_myuser()



    return render_template('Viewcomment.html',comments = o)








@app.route('/comments' ,methods=('GET', 'POST'))
def comment():
        form = RForm(request.form)
        if request.method == 'POST':
            comments = form.comments.data
            name = form.name.data
            error = ""

            if comments == "":
                error = 'comment is required'

            if name == "":
                error = 'user is required'

            if error == "":
                addcomments(name,comments)
                return redirect(url_for('viewproblems'))


        return render_template('comments.html',form=form)








@app.route('/<string:id>', methods=['POST'])
def delete(id):
    if request.method == "POST":

        delete_problems(id)
        posts = get_problems()

    return render_template('Adminpage.html', problems=posts)



@app.route('/<string:id>/delete', methods=['POST'])
def deletenews(id):
    if request.method == "POST":

        delete_news(id)
        posts = get_news()

    return render_template('viewnews.html', news=posts)




#========================================================================================================================#

@app.route('/login',  methods=('GET', 'POST'))
def login():
    login_form = LoginForm(request.form)
    error = None
    if request.method == 'POST':
        user = get_user(login_form.id.data, login_form.password.data)
        if user is False:
            ban = blackinfo(login_form.id.data)
            error = ban
        elif user is None:
            error = 'Wrong username and password'
        else:
            session['username'] = user.username
            return redirect(url_for('homepage'))
        flash(error)
    return render_template('login.html', form=login_form)

@app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        username = form.id.data
        password = form.password.data
        answer = form.answer.data
        email = form.email.data
        user = checkname(username)
        if len(password) > 7 and password.isalnum():
            pass
        else:
            user = False

        error = None
        if user is True:
            error = 'Username already in use'
        elif user is False:
            error = 'Password has to be alphanumeric and at least 8 characters'
        elif not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not answer:
            error = 'Answer is required'
        elif not email:
            error = 'Email is required'
        else:
            create_user(username, password, answer, email)
            return redirect(url_for('login'))
        flash(error)
    return render_template('register.html', form=form)

@app.route('/changepassword', methods=('GET', 'POST'))
def password():
    pform = PasswordForm(request.form)
    if request.method == 'POST':
        username = pform.id.data
        password = pform.password.data
        answer = pform.answer.data
        user = cpassword(username, password, answer)
        if len(password) > 7 and password.isalnum():
            pass
        else:
            user = False
        error = None
        if user is None:
            error = 'Wrong Details'
        elif user is False:
            error = 'Password has to be alphanumeric and at least 8 characters'
        else:
            return redirect(url_for('login', form=pform))
        flash(error)
    return render_template('password.html', form=pform)







@app.route('/blacklist', methods=('GET', 'POST'))
def blacklist():
    bform = BlacklistForm(request.form)
    if request.method == 'POST':
        username = bform.id.data
        reason = bform.reason.data
        user = checkname(username)
        error = None
        if user is None:
            error = 'Invalid username'
        else:
            blacklistuser(username, reason)
            error = 'Blacklisted'
        flash(error)
    return render_template('blacklist.html', form=bform)

@app.route('/whitelist', methods=('GET', 'POST'))
def whitelist():
    bform = BlacklistForm(request.form)
    if request.method == 'POST':
        username = bform.id.data
        user = checkname2(username)
        error = None
        if user is None:
            error = 'Invalid username'
        else:
            whitelistuser(username)
            error = 'Whitelisted'
        flash(error)
    return render_template('whitelist.html', form=bform)

@app.route('/adlogin',  methods=('GET', 'POST'))
def adlogin():
    adlogin_form = adLoginForm(request.form)
    error = None
    if request.method == 'POST':
        admin = get_admin(adlogin_form.id.data, adlogin_form.password.data)
        if admin is None:
            error = 'Wrong username and password'
        else:
            session['adminname'] = admin.username
            return redirect(url_for('Adminhomepage'))
        flash(error)
    return render_template('adlogin.html', form=adlogin_form)

@app.route('/adregister', methods=('GET', 'POST'))
def adregister():
    form = adRegisterForm(request.form)
    if request.method == 'POST':
        username = form.id.data
        password = form.password.data
        email = form.email.data
        user = checkadname(username)
        error = None
        if len(password) > 7 and password.isalnum():
            pass
        else:
            user = False
        if user is True:
            error = 'Username already in use'
        elif not username:
            error = 'Username is required.'
        elif user is False:
            error = 'Password has to be alphanumeric and at least 8 characters'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = 'Email is required'
        else:
            create_admin(username, password, email)
            return redirect(url_for('adlogin'))
        flash(error)
    return render_template('adregister.html', form=form)

@app.route('/logout', methods=('GET', 'POST'))
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/Alogout', methods=('GET', 'POST'))
def Alogout():
    session.clear()
    return redirect(url_for('adlogin'))

@app.route('/homepage')
def homepage():
    return render_template('Home Page.html')



@app.route('/Adminhomepage')
def Adminhomepage():
    return render_template('AdminHome.html')


#=======================================================================================================================#




class IncidentForm(Form):
    category = SelectField("Category", [validators.DataRequired()], choices=[("North", "North"),
                                                                             (
                                                                                 "South",

                                                                                 "South"),
                                                                             ("East",
                                                                              "East"), (
                                                                                 "West",
                                                                                 "West")],
                           default="Choose your option")
    date = DateField('Date of incident  ', default=datetime.today().date(),
                                 validators=[DataRequired()])
    time = StringField( "Time of Incident",[validators.DataRequired()])

    location = StringField('Location',[validators.DataRequired()])

    description = TextAreaField('Enter Description of incident',[validators.DataRequired()])

    submit = SubmitField("submit")

class Incident:
    def __init__(self,category,date,time,location,description ):
        self.__category = category
        self.__date = date
        self.__time = time
        self.__location = location
        self.__description = description
        self.__id = ''
    def get_id(self):
        return self.__id
    def set_id(self,id):
        self.__id = id




    def get_category(self):
        return self.__category
    def set_category(self,category):
        self.__category = category

    def get_time(self):
        return self.__time
    def set_time(self,time):
        self.__time = time

    def get_date(self):
        return self.__date
    def set_date(self,date):
        self.__date = date

    def get_location(self):
        return self.__location
    def set_location(self,location):
        self.__location = location

    def get_description(self):
        return self.__description
    def set_description(self,description):
        self.__description = description






@app.route('/incident', methods=['GET', 'POST'])
def incident():
    form = IncidentForm(request.form)

    db_read = shelve.open("incident.db")

    try:
        incidentList = db_read["incident"]
    except:
        incidentList = {}

    if request.method == 'POST' and form.validate():
            date = form.date.data
            time = form.time.data
            location = form.location.data
            description = form.description.data
            category = form.category.data

            incident = Incident(category,date,time,location,description)

            id = len(incidentList) + 1

            incident.set_id(id)

            incidentList[id] = incident

            db_read["incident"] = incidentList

            db_read.close()
            return redirect('/incident')
    return render_template('incident.html', form=form)


@app.route('/incidentsummary')
def summary():
    db_read = shelve.open("incident.db", "r")
    incident = db_read['incident']
    print(incident)
    list = []
    for id in incident:
        list.append(incident.get(id))
    db_read.close()
    return render_template('incidentsummary.html',incident= list )



@app.route('/excuseslip')
def excuse():
    db_read = shelve.open("incident.db", "r")
    incident = db_read['incident']
    print(incident)
    list = []
    for id in incident:
        list.append(incident.get(id))
    db_read.close()
    return render_template('excuseresult.html',incident= list )


#===================================================================================================#














@app.route('/addnews', methods=('GET', 'POST'))
def gothere():
    form = FillUp(request.form)
    if request.method == 'POST':
        news = form.news.data
        title = form.title.data
        desc = form.desc.data
        severity = form.severity.data
        error = ""

        if news == "":
            error = 'problem is required.'
        if title == "":
            error = 'Title is required.'
        if desc == "":
            error = 'Description is required'
        if severity == "":
            error = 'Please select a button'


        if error == "":
            adminForm.create_news(news, title, desc, severity)
            flash("Uploaded Successfully")


    return render_template('Urgent News.html',form=form)



@app.route('/viewnews')
def viewnews():


    x = get_news()



    return render_template('viewnews.html', news=x)


if __name__ == '__main__':
    app.run(port = '80')

