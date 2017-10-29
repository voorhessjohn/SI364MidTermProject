from flask import Flask, request, render_template, redirect, url_for, flash, make_response
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Required

import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supercalifragilisticexpialidocious'

####################
# 2 WTF Forms
####################

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')
    
class DadForm(FlaskForm):
    attitude = SelectField(u"What kind of attitude?", choices=[('silly','silly'),('serious','serious')], validators=[Required()])
    dress = SelectField(u"How does he dress?", choices=[('business','business'),('casual','casual'),('a badge','a badge')], validators=[Required()])
    job = SelectField(u"What kind of job does he do?", choices=[('blue collar', 'blue collar'),('white collar', 'white collar')], validators=[Required()])
    submit = SubmitField('Submit')

#####################################################################################################################
# If I had to do this part again, I would have made a single dictionary with names as keys and attributes as values #
#####################################################################################################################

SILLY = ['Jay Pritchett','Stan Smith','Al Bundy', 'Carl Winslow', 'Danny Tanner', 'Michael Bluth', 'Mike Brady', 'Peter Griffin', 'Phil Dunphy', 'Tony Micelli']
SERIOUS = ['Michael Taylor','Seeley Booth','Andy Taylor', 'Archie Bunker', 'Earl Sinclair', 'Fred Sanford', 'Gomez Addams', 'Herman Munster', 'Leland Palmer', 'Philip Banks', 'Red Forman', 'Steven Keaton', 'Tony Soprano', 'Ward Cleaver']
BUSINESS = ['Seeley Booth','Stan Smith','Danny Tanner', 'Michael Bluth', 'Mike Brady', 'Phil Dunphy', 'Gomez Addams', 'Herman Munster', 'Leland Palmer', 'Philip Banks', 'Steven Keaton', 'Tony Soprano', 'Ward Cleaver']
CASUAL = ['Michael Taylor','Jay Pritchett','Al Bundy', 'Peter Griffin', 'Tony Micelli', 'Archie Bunker', 'Earl Sinclair', 'Fred Sanford', 'Red Forman']
BLUE = ['Al Bundy', 'Andy Taylor', 'Archie Bunker', 'Carl Winslow', 'Earl Sinclair', 'Fred Sanford', 'Peter Griffin', 'Red Forman', 'Tony Micelli', 'Tony Soprano', 'Phil Dunphy', 'Herman Munster']
WHITE = ['Michael Taylor','Jay Pritchett','Seeley Booth','Stan Smith','Danny Tanner', 'Gomez Addams', 'Herman Munster', 'Leland Palmer', 'Michael Bluth', 'Mike Brady', 'Philip Banks', 'Steven Keaton', 'Ward Cleaver']
BADGE = ['Seeley Booth','Stan Smith','Andy Taylor', 'Carl Winslow']

def getDadFile(name):
    dadFile=name.replace(" ", "")
    dadFile=dadFile + ".jpg"
    return dadFile

############################
# Two error handler routes #
############################

@app.errorhandler(404)
def four_oh_four(error):
    return render_template('thats_a_404.html'), 404

@app.errorhandler(403)
def four_oh_three(error):
    return render_template('thats_a_503.html'), 403

@app.route('/')
def index():
    nameForm = NameForm()
    return render_template('nameform.html', form=nameForm)

@app.route('/dadform', methods = ['GET', 'POST'])
def showDadForm():
    form=NameForm(request.form)
    if request.method == 'POST' and form.name.data != "":
        userName = form.name.data

    ####################
    # Setting a cookie #
    ####################

        response = make_response('<h1>This document carries a cookie!</h1>')
        response.set_cookie('Name', userName)
    
        dadForm = DadForm()
        return render_template('dadform.html', form=dadForm, username=userName)
    else:
        flash('All fields are required!')
        return redirect(url_for('index'))
    
@app.route('/dadresult', methods = ['GET', 'POST'])
def showDadResult():
    form = DadForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        attitude = form.attitude.data
        dress = form.dress.data
        job = form.job.data
        if attitude == 'silly':
            attList = SILLY
        else:
            attList = SERIOUS
        if dress == 'business':
            dressList = BUSINESS
        elif dress == 'casual':
            dressList = CASUAL
        else:
            dressList = BADGE
        if job == 'blue collar':
            jobList = BLUE
        else:
            jobList = WHITE

        #set intersection method found here: https://stackoverflow.com/questions/3852780/python-intersection-of-multiple-lists
        d=[attList, dressList, jobList]
        d=sorted(d)
        result = set(d[0]).intersection(*d)

        return render_template('dad_result.html', result=result)
        
    flash('All fields are required!')

    ########################
    # redirect and url_for #
    ########################
    return redirect(url_for('showDadForm'))

@app.route('/finaldad/<dadname>')
def showFinalDad(dadname):
    dadFile = getDadFile(dadname)
    return render_template('final_dad.html', dadName=dadname, dadFile=dadFile)

