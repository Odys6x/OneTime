from flask import *
from user import *
import shelve

class problems:
    def __init__(self,problem,description,location,date):
        self.__problem = problem
        self.__description = description
        self.__location = location
        self.__date = date
        self.__status = 'pending'
        self.__name = ' '
        self.__comment = ' '

    def get_name(self):
        return self.__name


    def set_name(self,name):
        self.__name = name


    def get_comment(self):
        return self.__comment


    def set_comment(self,comment):
        self.__comment = comment


    def get_problem(self):
        return self.__problem

    def get_description(self):
        return self.__description

    def get_location(self):
        return self.__location

    def get_date(self):
        return self.__date

    def get_status(self):
        return self.__status

    def create_request(problem, description, location, date):
        new = shelve.open('problems')
        p = problems(problem,description,location,date)
        p.set_name(session['username'])
        p.self__problem = problem
        p.self__description = description
        p.self__location = location
        p.self__date = date
        new[description] = p


class myUser:
    def __init__(self,name,comments):
        self.__name = name
        self.__comments = comments



    def get_name(self):
        return self.__name

    def get_comments(self):
        return self.__comments


def delete_problems(id):
    storage = shelve.open('problems')
    if id in storage:
        del storage[id]



def get_problems():
    storage = shelve.open('problems')
    klist = list(storage.keys())
    x = []
    for i in klist:
        x.append(storage[i])
    return x




def get_user(username):
    blacklist = shelve.open('blacklist')
    if username in blacklist:
        return False

    return None


def blacklistuser(username):
    blacklist = shelve.open('blacklist')
    b = Blacklist()
    b.username = username
    blacklist[username] = b



def addcomments(name,comments):
    comment = shelve.open('comments')
    p = myUser(name,comments)
    p.self__name =name
    p.self__comments = comments
    comment[name] = p


def get_myuser():
    storage = shelve.open('comments')
    klist = list(storage.keys())
    x = []
    for i in klist:
        x.append(storage[i])
    return x







def get_excuse():
    storage = shelve.open('incident.db')
    klist = list(storage.keys())
    x = []
    for i in klist:
        x.append(storage[i])
    return x





