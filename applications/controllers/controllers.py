from main import decks, app, db
from applications.data.models import *
from flask import render_template, request, redirect, session, json, send_file
from werkzeug.exceptions import HTTPException
from random import sample, shuffle

@app.route('/', methods = ['GET', 'POST'])
def index():
    session.pop('user', None)
    session['login'] = False
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        if 'admin_pass' in request.form:
            if request.form['admin_pass'] == 'P@ssw0rd':
                session['user'] = 'admin'
                session['login'] = True
                return redirect('/admin/dashboard')
            else:
                return render_template('error.html', error = 'Password Incorrect !!!', info = 'Incorrect Administrator Password !!! Try Again ...')
        else:
            d = dict()
            for u in User.query.all():
                d[u.email] = u.password
            if 'new_pass' in  request.form:
                if request.form['new_email'] in d.keys():
                    return render_template('error.html', error = 'User Already Exists !!!', info = '[ Go Back & Login ] OR [ Register With Another E-Mail ]')
                else:
                    db.session.add(User(email = request.form['new_email'], password = request.form['new_pass']))
                    db.session.commit()
                    session['user'] = request.form['new_email']
                    session['login'] = True
                    return redirect(f"/{session['user']}/dashboard")
            elif 'user_pass' in request.form:
                if request.form['user_email'] in d.keys():
                    if d[request.form['user_email']] == request.form['user_pass']:
                        session['user'] = request.form['user_email']
                        session['login'] = True
                        return redirect(f"/{session['user']}/dashboard")
                    else:
                        return render_template('error.html', error = 'Password Incorrect !!!', info = 'Incorrect User Password !!! Try Again ...')
                else:
                    return render_template('error.html', error = 'Unrecognised User !!!', info = 'User Not Registered !!! Go Back & Register ...')

@app.route('/<user>/dashboard', methods = ['GET', 'POST'])
def dashboard(user):
    if session['login'] == False:
        return render_template('error.html', error = 'Unauthorised Access !!!', info = 'Currently Not Logged In !!! Go Back & Login ...')
    elif session['login'] == True:
        if session['user'] == user:
            users = list()
            for U in User.query.all():
                u = dict()
                u['email'] = U.email
                u['correct'] = U.correct
                u['incorrect'] = U.incorrect
                u['score'] = (int(U.correct) * 2) - (int(U.incorrect) * 1)
                u['accuracy'] = (int(U.correct) * 100) / (int(U.correct) + int(U.incorrect)) if (int(U.correct) + int(U.incorrect)) != 0 else int(0)
                users.append(u)
            cards = dict()
            if decks:
                for deck in decks:
                    cards[deck] = Card.query.filter_by(deck = deck).all()
            if user == 'admin':
                if request.method == 'GET':
                    return render_template('dashboard.html', user = 'Administrator', cards = cards, decks = decks, users = users)
                elif request.method == 'POST':
                    if 'create_deck_name' in request.form:
                        if request.form['create_deck_name'] not in decks:
                            decks.append(request.form['create_deck_name'])
                            return redirect('/admin/dashboard')
                        else:
                            return render_template('error.html', error = 'Deck Already Exists !!!', info = '[ Go To That Deck ] OR [ Enter Unique Name ]')
                    elif 'add_card_front' in request.form:
                        db.session.add(Card(question = request.form['add_card_front'], answer = request.form['add_card_back'], deck = request.form['add_card_deck']))
                        db.session.commit()
                        return redirect('/admin/dashboard')
            elif user != 'admin':
                if request.method == 'GET':
                    data = dict()
                    for u in users:
                        if u['email'] == user:
                            data = u
                    return render_template('dashboard.html', user = user, cards = cards, decks = decks, data = data)
                elif request.method == 'POST':
                    pass
        elif session['user'] != user:
            if session['user'] == 'admin':
                return render_template('error.html', error = 'Access Denied !!!', info = 'Administrator Can\'t Access Other User\'s Contents')
            elif session['user'] != 'admin':
                if user == 'admin':
                    return render_template('error.html', error = 'Access Denied !!!', info = 'Users Can\'t Access Administrator\'s Contents')
                elif user != 'admin':
                    return render_template('error.html', error = 'Access Denied !!!', info = 'Users Can\'t Access Other User\'s Contents')

@app.route('/m/<user>/<model>/<action>/<element>', methods = ['GET', 'POST'])
def management(user, model, action, element):
    if session['login'] == False:
        return render_template('error.html', error = 'Unauthorised Access !!!', info = 'Currently Not Logged In !!! Go Back & Login ...')
    elif session['login'] == True:
        if session['user'] == user:
            if user == 'admin':
                if model == 'deck':
                    if action == 'remove':
                        decks.remove(element)
                        for card in Card.query.filter_by(deck = element).all():
                            db.session.delete(card)
                            db.session.commit()
                        return redirect('/admin/dashboard')
                    elif action == 'export':
                        f = open(element + '.csv', 'w')
                        f.write('FRONT,BACK\n----------,----------\n')
                        for card in Card.query.filter_by(deck = element).all():
                            f.write(card.question + ',"' + card.answer + '"\n')
                        f.close()
                        return send_file(element + '.csv', as_attachment = True)
                elif model != 'deck':
                    for card in Card.query.filter_by(deck = model).all():
                        if card.question == element:
                            db.session.delete(card)
                            db.session.commit()
                    return redirect('/admin/dashboard')
            elif user != 'admin':
                if action == 'export':
                    u = User.query.filter_by(email = user).first()
                    f = open(user + '.csv', 'w')
                    f.write('E-MAIL,CORRECT,INCORRECT,SCORE,ACCURACY\n')
                    f.write('----------,----------,----------,----------,----------\n')
                    f.write(u.email + ',' + str(u.correct) + ',' + str(u.incorrect) + ',' + str((int(u.correct) * 2) - (int(u.incorrect) * 1)) + ',' + str((int(u.correct) * 100) / (int(u.correct) + int(u.incorrect)) if (int(u.correct) + int(u.incorrect)) != 0 else int(0)) + ' %\n')
                    f.close()
                    return send_file(user + '.csv', as_attachment = True)
                elif action == 'play':
                    if request.method == 'GET':
                        cards = Card.query.filter_by(deck = model).all()
                        card = sample(cards, 1)
                        cards = list(set(cards).difference(set(card)))
                        options = list()
                        options.append(card[0].answer)
                        for c in sample(cards, 3):
                            options.append(c.answer)
                        shuffle(options)
                        return render_template('play.html', user = user, deck = model, question = card[0].question, options = options)
                    elif request.method == 'POST':
                        u = User.query.filter_by(email = user).first()
                        for k, v in request.form.items():
                            if Card.query.filter_by(deck = model, question = k).first().answer == v:
                                u.correct += 1
                            else:
                                u.incorrect += 1
                        db.session.commit()
                        return redirect(f"/m/{user}/{model}/play/start")
        elif session['user'] != user:
            if session['user'] == 'admin':
                return render_template('error.html', error = 'Access Denied !!!', info = 'Administrator Can\'t Access Other User\'s Contents')
            elif session['user'] != 'admin':
                if user == 'admin':
                    return render_template('error.html', error = 'Access Denied !!!', info = 'Users Can\'t Access Administrator\'s Contents')
                elif user != 'admin':
                    return render_template('error.html', error = 'Access Denied !!!', info = 'Users Can\'t Access Other User\'s Contents')

@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return render_template('error.html', error = 'HTTP Exception !!!', info = response)

@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return e
    return render_template('error.html', error = 'Exception !!!', info = e), 500