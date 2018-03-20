###############################
####### SETUP (OVERALL) #######
###############################

## Import statements
# Import statements
from __future__ import print_function #this has to be at the begining of file
import unittest
import itertools
import collections
import os
#import facebook_info # same deal as always...
import json
import urllib.request, urllib.parse, urllib.error
from urllib.request import Request, urlopen
import ssl
import requests
import pprint
import pickle
import re
from datetime import date, datetime, timedelta, time
import httplib2
import os
import oauth2client
from oauth2client import file, client, tools
import base64

from flask import Flask, render_template, session, redirect, url_for, request, flash
from flask_script import Shell, Manager
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand

from yelpapi import YelpAPI
#import argparse
from pprint import pprint
api_key='n1El1-a4TORQrAc5xBjfX-Sc6ZKDPisyjMU_JTcGFxX8Je5LO1U40U_OCTWbO1zdHNwWYnBlxUA_kLvQZvPH9nCCNlm3sWIxExHmZuBtXCkqlBbfw_XRL4FHMsCVWnYx'

#yelp_api = YelpAPI(args.api_key)

yelp_api = YelpAPI(api_key)

# Configure base directory of app
basedir = os.path.abspath(os.path.dirname(__file__))

## App setup code
app = Flask(__name__)
#app.debug = True
#app.use_reloader = True

## All app.config values

app.config['SECRET_KEY'] = 'hardtoguessstringfromsi364thisisnotsupersecurebutitsok'


app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/hcyenmidtermdb"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


## Statements for db setup (and manager setup if using Manager)

manager = Manager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand) # Add migrate command to manager

######################################
######## HELPER FXNS (If any) ########
######################################

##################
##### MODELS #####
##################

class Name(db.Model):
    __tablename__ = "names"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))

    def __repr__(self):
        return "{} (ID: {})".format(self.name, self.id)


class Industry(db.Model):
    __tablename__ = 'industries'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    companies = db.relationship('Company',backref='Industry')

    def __repr__(self):
        return "{} (ID: {})".format(self.name,self.id)

class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    industry_id = db.Column(db.Integer, db.ForeignKey('industries.id'))
    employees = db.relationship('Employee',backref='Company')

    def __repr__(self):
        return "{} (ID: {})".format(self.name,self.id)

class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    position = db.Column(db.String(64))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))

    def __repr__(self):
        return "{} by {} | {}".format(self.name, self.company_id)





##### Helper functions
### For database additions / get_or_create functions
def get_or_create_industry(db_session, industry_name):
    industry = db_session.query(Industry).filter_by(name=industry_name).first()
    if industry:
        return industry
    else:
        industry = Industry(name=industry_name)
        db_session.add(industry)
        db_session.commit()
        return industry
'''
def get_or_create_company(db_session,company_name):
    company = db_session.query(Company).filter_by(name=company_name).first()
    if company:
        return company
    else:
        company = Company(name=company_name)
        db_session.add(company)
        db_session.commit()
        return company
'''
def get_or_create_company(db_session, company_name, company_industry ):
    company = db_session.query(Company).filter_by(name=company_name).first()
    if company:
        return company
    else:
    

        industry = get_or_create_industry(db_session, company_industry)
        company = Company(name=company_name, industry_id=industry.id)
        db_session.add(company)
        db_session.commit()
        return company

# you cannot add the employee unless the company is in the database. If not, it will display the company form for you to add the company first.
# This function returns two values and the purpose is to allow you to add the company first if the company is not in the database.
def get_or_create_employee(db_session, employee_name, employee_company, employee_position):
    employee = db_session.query(Employee).filter_by(name=employee_name).first()
    if employee:
        #https://stackoverflow.com/questions/9752958/how-can-i-return-two-values-from-a-function-in-python
        return employee, True
    else:
        company = db_session.query(Company).filter_by(name=employee_company).first()
        if company:

        
            employee = Employee(name=employee_name, position=employee_position, company_id=company.id)
            db_session.add(employee)
            db_session.commit()
            return employee, True
        else:
            flash('***** Sorry! You need to add the company and industry first before you could add the employee')
            #return redirect('http://localhost:5000/company')
            return  redirect(url_for('company')), False
            

            #company = get_or_create_company(db_session, employee_company, company_industry)
'''
def get_or_create_employee(db_session, employee_name, employee_company, employee_position):
    employee = db_session.query(Employee).filter_by(name=employee_name).first()
    if employee:
        return employee
    else:
        company = get_or_create_company(db_session, employee_company, company_industry)
        employee = Employee(name=employee_name, position=employee_position, company_id=company.id)
        db_session.add(employee)
        db_session.commit()
        return employee
'''
##### Set up Models #####

'''

class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    companyname = db.Column(db.String(124), index=True, unique=True)
    industry = db.Column(db.String(124))
    address1 = db.Column(db.String(124))
    address2 = db.Column(db.String(124))
    city = db.Column(db.String(30))
    state = db.Column(db.String(2))
    zipcode = db.Column(db.Integer)
    employees = db.relationship('Employee', backref='Company', lazy='dynamic')

    def __repr__(self):
        return "{companyname} | ID: {id}".format(self.companyname, self.id)
        #return '<User %r>' % (self.username)

class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(120))
    lastname = db.Column(db.String(120))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))

    def __repr__(self):
        #return "{Tweet text %r} % (ID: {tweet id})".format(self.text, self.id)
        return "Employee Name:{firstname} " " {lastname} | (ID:{id})".format(self.firstname, self.lastname, self.id)

'''

#from HW3
def validate_category(form, field):
    if (field.data).startswith("@"):
        raise ValidationError("category entry could not start with @")
#from HW3
def validate_employee_name(form, field):
    if not " " in (field.data):
        raise ValidationError("Employee name MUST be at least 2 words")

def validate_state(form, field):
    if len(field.data) != 2:
        print(field.data)
        raise ValidationError("state abbreviation must be two characters")

###################
###### FORMS ######
###################

class NameForm(FlaskForm):
    name = StringField("Please enter your name.",validators=[Required()])
    submit = SubmitField()

class YelpSearchForm(FlaskForm):
    category = StringField("What is the category of the business you are searching for? (ice cream, restaurant, etc)", validators=[Required(), validate_category])
    city = StringField("Please enter the City",validators=[Required()])
    #state = StringField("Please enter the two letters of state abbreviation. (MI, NY, etc)", [Required(), validate_state])
    state = StringField("Please enter the two letters of state abbreviation. (MI, NY, etc)", validators=[Required(), validate_state])

    submit = SubmitField('Submit')

class EmployeeForm(FlaskForm):
    employee = StringField("What is the name of the employee?", validators=[Required(), validate_employee_name])
    company = StringField("What is the name of the company where the employee works?",validators=[Required()])
    #industry = StringField("What industry the company falls into?",validators=[Required()])
    position = StringField("What is the employee's position in the company?", validators=[Required()])
    submit = SubmitField('Submit')

class CompanyForm(FlaskForm):
   
    company = StringField("What is the name of the company where the employee works?",validators=[Required()])
    industry = StringField("What industry the company falls into?",validators=[Required()])
    
    submit = SubmitField('Submit')


#class EmployeeCompanyForm(FlaskForm):
#    employee_name = StringField('Enter employee name:', validators=[Required(), validate_employee_name])
#    company_name = StringField('Enter company name:', validators=[Required()])
#    submit = SubmitField('Submit')
#http://wtforms.simplecodes.com/docs/1.0.1/validators.html
#https://stackoverflow.com/questions/17730455/flask-wtf-form-validation-not-working
#validation only works for post not get



#######################
###### VIEW FXNS ######
#######################
## Error handling routes - PROVIDED
## The following two functions, plus the 404 and 500 .html files in the templates folder are from instructor's notes (discussion/lecture)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

#https://stackoverflow.com/questions/20689195/flask-error-method-not-allowed-the-method-is-not-allowed-for-the-requested-url
#so we add, methods=['GET', 'POST'] to the following two routes
# this allows duplicated data.
@app.route('/', methods=['GET', 'POST'])
def home():
    form = NameForm() # User should be able to enter name after name and each one will be saved, even if it's a duplicate! Sends data with GET
    if form.validate_on_submit():
        name = form.name.data
        print(name)
        #newname = Name(name)
        newname = Name(name=name) ## change to Name(name=name) https://stackoverflow.com/questions/30032078/typeerror-init-takes-1-positional-argument-but-3-were-given
        db.session.add(newname)
        db.session.commit()
        return redirect(url_for('all_names'))
    return render_template('base.html',form=form)
#File "SI364midterm.py", line 237, in home
#    newname = Name(name)
#TypeError: __init__() takes 1 positional argument but 2 were given
#127.0.0.1 - - [02/Mar/2018 18:47:53] "POST / HTTP/1.1" 500 -
#solution is https://stackoverflow.com/questions/30032078/typeerror-init-takes-1-positional-argument-but-3-were-given
# change from newname = Name(name) to newname = Name(name=name)

@app.route('/names', methods=['GET', 'POST'])
def all_names():
    names = Name.query.all()
    return render_template('name_example.html',names=names)


@app.route('/yelp_search', methods = ['POST', 'GET'])
def yelpsearch():
   form = YelpSearchForm()
   return render_template('yelp_search.html', form = form)
'''
@app.route('/search_result', methods = ['POST', 'GET'])
def searchresult():
    form = YelpSearchForm()
    if form.validate_on_submit():
        category = form.category.data
        city = form.city.data
        state = form.state.data
        return render_template('search_data.html', category=category, city=city, state=state)
        
    return "Sorry, no data available"
'''

# use the template "list.html" to display the results for the choices entered by the user in the form above.
# The data should be displayed on http://localhost:5000/yelp_result

@app.route('/yelp_result', methods = ['POST', 'GET'])
def resultyelp():
    form = YelpSearchForm()
    '''
    if form.validate_on_submit():

        category = form.category.data
        city = form.city.data
        state = form.state.data
        print(category)
        print(city)
        print(state)
        pprint("term=category, location=city + ',' + state, sort_by='rating', limit=5")
        params_diction = {}
        params_diction['term'] = form.category.data
        
        params_diction['Location'] = form.city.data + ', ' + form.state.data
        
        params_diction['sort_by'] = 'rating'
        params_diction['Limit'] = 5
        #resp = yelp_api.search_query(term=%category, location=%city + ',' + %state, sort_by='rating', limit=5)
        #resp = yelp_api.search_query(term={}, location={}, sort_by='rating', limit=5).format(%category, %city + ',' + %state)
        resp = yelp_api.search_query(term=params_diction['term'], location=params_diction['Location'], sort_by='rating', limit=5)
        #resp = yelp_api.search_query(term=$category, Location=$city ,$state, sort_by='rating', limit=5)

        pprint(resp)
        return render_template('list.html', businesses = resp['businesses'])
        #return render_template('search_data.html', category=category, city=city, state=state)
        
    return "Sorry, no data available"
    '''
    if request.method == 'GET':
        result = request.args
        baseurl = "https://api.yelp.com/v3/businesses/search"
        params_diction = {}
        params_diction['term'] = result.get('category')
        print(result.get('category'))
        params_diction['Location'] = result.get('city') + ', ' + result.get('state')
        print(result.get('city') + ', ' + result.get('state'))
        params_diction['sort_by'] = 'rating'
        params_diction['Limit'] = 5

        #resp = requests.get(baseurl,params=params_diction)
        #pprint(resp)
        #text = resp.text
        #pprint(text)
        #python_obj = json.loads(text)
        #businesses = python_obj["businesses"]
        
        #resp = yelp_api.search_query(params = params_diction)

        #resp returns a dictionary
        resp = yelp_api.search_query(term=params_diction['term'], location=params_diction['Location'], sort_by='rating', limit=5)
        pprint(resp)
        

    
        #response = yelp_api.search_query(term='Restaurant', location='Ann Arbor, MI', sort_by='rating', limit=5)
        return render_template('list.html', businesses = resp['businesses'])
    '''

        #data = json.loads(resp.text)
        #pprint(data)
        #return render_template('list.html', businesses = resp['businesses'])
        #return render_template('list.html', businesses = businesses)
        
        #data = json.loads(resp.text)
        #pprint(data)

        #got this error : jinja2.exceptions.TemplateSyntaxError: expected token ':', got '}'
        #https://stackoverflow.com/questions/27704913/templatesyntaxerror-expected-token-got
        #initially, the list.html, I have this {% if {{b['url'] }} %}. I changed it to {% if b['url'] %} to delete the {{}}
    
        Don't do more {{}} inside of other {{}} blocks.

        Here's my url_for() call:

        <a href="{{ url_for('viewBlog', userid=item.userid)}}"></a>
        I was getting that same error when it looked like this:

        <a href="{{ url_for('viewBlog', userid={{item.userid}}) }}"></a>
        Once I removed the inner {{}}, the problem went away.
    '''
        
@app.route('/company', methods=['GET', 'POST'])
def company():
    companies = Company.query.all()
    num_companies = len(companies)
    form = CompanyForm()
    if form.validate_on_submit():
        if db.session.query(Company).filter_by(name=form.company.data).first(): # If there's already a company with that name
            flash("You've already saved an company with that name!")
        get_or_create_company(db.session, form.company.data, form.industry.data)
        return redirect(url_for('see_all_companies'))
    return render_template('company.html', form=form, num_companies=num_companies)
'''
@app.route('/employee', methods=['GET', 'POST'])
def employee():
    employees = Employee.query.all()
    num_employees = len(employees)
    form = EmployeeForm()
    if form.validate_on_submit():
        if db.session.query(Employee).filter_by(name=form.employee.data).first(): # If there's already an employee with that name
            flash("You've already saved an employee with that name!")
        get_or_create_employee(db.session, form.employee.data, form.company.data, form.position.data)
        return redirect(url_for('view_all_employees'))
    return render_template('employee.html', form=form, num_employees=num_employees)
'''
@app.route('/employee', methods=['GET', 'POST'])
def employee():
    employees = Employee.query.all()
    num_employees = len(employees)
    form = EmployeeForm()
    if form.validate_on_submit():
        if db.session.query(Employee).filter_by(name=form.employee.data).first(): # If there's already an employee with that name
            flash("You've already saved an employee with that name!")

        if get_or_create_employee(db.session, form.employee.data, form.company.data, form.position.data)[1]:  #if the 2nd returned value is True, tuple element #2
            
            return redirect(url_for('view_all_employees'))

        else: #if 2nd returned value is False, then the company is not in the database. Display the company form to add company first.

            return  redirect(url_for('company'))
            # return None   #ValueError: View function did not return a response
            #pass

    return render_template('employee.html', form=form, num_employees=num_employees)

# display all the employees in the database.
@app.route('/all_employees')
def view_all_employees():
    all_employees = [] # To be tuple list of name, position
    employees = Employee.query.all()
    for e in employees:
        company = Company.query.filter_by(id=e.company_id).first()
        all_employees.append((e.name, company.name, e.position))
    return render_template('all_employees.html',all_employees=all_employees)

# display all the companies in the database.
@app.route('/all_companies')
def see_all_companies():
    companies = Company.query.all()
    names = [(c.name, len(Employee.query.filter_by(company_id=c.id).all())) for c in companies]
    return render_template('all_companies.html', company_names=names) 

# display all the industries in the database.
@app.route('/all_industries')
def see_all_industries():
    industries = Industry.query.all()
    names = [(i.name, len(Company.query.filter_by(industry_id=i.id).all())) for i in industries]
    return render_template('all_industries.html', industry_names=names)    


## Code to run the application...

# Put the code to do so here!
# NOTE: Make sure you include the code you need to initialize the database structure when you run the application!
if __name__=='__main__':
    db.create_all()
    manager.run()
    app.run(use_reloader=True,debug=True)