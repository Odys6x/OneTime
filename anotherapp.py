from flask import *
from Problem import *
from Create import *

app = Flask(__name__)
app.secret_key = 'secret_123'




@app.route('/report', methods=('GET', 'POST'))
def register():
    form = RequestForm(request.form)
    if request.method == 'POST':

        problem = form.problem.data
        description = form.description.data
        location = form.location.data
        date     = form.date.data
        error = ""
        if problem == "":
            error = 'Username is required.'
        if description == "":
            error = 'Description is required.'
        if location == "":
            error = 'Location is required'
        if date == "":
            error = 'Date is required'

        if error == "":

            User.create_request(problem, description, location,date)
            return redirect(url_for('viewproblems'))
        flash(error)
    return render_template('Userpage.html', form=form)




@app.route('/admin')
def viewproblems():

    db_read = shelve.open("storage", "r")
    klist = list(db_read.keys())
    x = []
    for i in klist:
        x.append(db_read[i])

    print(klist)

    return render_template('Adminpage.html', problems=x)


if __name__ == '__main__':
    app.run(port = '80')

