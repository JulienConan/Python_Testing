import json
from datetime import datetime
from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']]
    if club:
        return render_template('welcome.html',club=club[0],competitions=competitions)
    else :
        flash("Sorry, that email wasn't found.")
        return render_template('index.html')

@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if datetime.strptime(foundCompetition['date'], "%Y-%m-%d %H:%M:%S") < datetime.now():
        flash("You don't booking places in past competitions.")
        return render_template('welcome.html',club=foundClub,competitions=competitions)
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    points_for_places = 3
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    if placesRequired > 12:
        flash("You shouldn't be able to book more than 12 places per competition.")
    elif placesRequired*points_for_places > int(club['points']):
        flash("You shouldn't be able to redeem more points than available.")
    elif (int(competition['numberOfPlaces'])-placesRequired) < 0 :
        flash("Not enough places for this tournament.")
    else:
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
        club['points'] = int(club['points'])-(placesRequired*points_for_places)
        flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/tab', methods=['GET'])
def tab():
    return render_template('tab.html', clubs=clubs)

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

app.run()