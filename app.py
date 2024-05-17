from flask import Flask, render_template, request, redirect, url_for, session
import json
from form import FormActu


app = Flask(__name__)
#Session secret key
app.secret_key = '5%4KFFR57ùsDV$grvF£Sµ/'

@app.route("/")
def start():
    """ Page d'accueil redirigée vers les actualités """
    return redirect(url_for('actualite'))

@app.route("/supprimeractu", methods=['GET', 'POST'])
def supprimeractu():
    """ Liste les actualités et permet de les supprimer """
    if request.method == 'POST':
        actu_data = read_json("actualites")
        print("Request.form id : ", request.form['id'])
        for i in range(0,len(actu_data)):
            if actu_data[i]['id'] == int(request.form['id']):
                del actu_data[i]
        print(actu_data)
        f = open('actualites.json', "w")
        f.write(json.dumps(actu_data))
        f.close()
        return redirect(url_for('actualite'))

    dataActualites=read_json("actualites")
    return render_template("actu_bref.html", data=dataActualites, name="all")


@app.route("/ajouteractu", methods=['GET', 'POST'])
def ajouteractu():
    """ Permet d'ajouter une actualité """

    """ Ajoute l'actualité dans le fichier JSON si un POST a été effectué """
    if request.method == 'POST':
        write_json("actualites", {'id': int(request.form['id']), 'title': request.form['title'], 'dateActu': request.form['dateActu'], 'type' : request.form['type']})
        return redirect(url_for('actualite'))

    """ Détermine l'id de l'actualité à ajouter (max déjà existant + 1) """
    data=read_json("actualites")
    max=0
    index=0
    for i in range(0,len(data)):
        if data[i]['id'] > max:
            max=data[i]['id']
            index=data[i]['id']+1
    
    """ Afficher le formulaire d'ajout d'actualité """
    return '''
    <a href="/actualites"><button>Retour à la liste des actualités</button></a>
    <form method="post">
    <input type="hidden" name="id" value='''+str(index)+'''>
    <p><input disabled value='''+str(index)+''' type=text name=id>
    <p><input requiered placeholder=title type=text name=title>
    <p><label for=dateActu>Date de l'actualité</label>
    <p><input requiered placeholder=dateActu type=date name=dateActu>
    <p><input requiered placeholder='rock, jazz, ...' type=text name=type>
    <p><input type=submit value=Envoyer>
    </form>

    '''
   ################################################" CONCERTS "##########################################################
@app.route("/supprimerconcert", methods=['GET', 'POST'])
def supprimerconcert():
    """ Liste les concerts et permet de les supprimer """
    if request.method == 'POST':
        data = read_json("concert")
        print("Request.form id : ", request.form['id'])
        for i in range(0,len(data)):
            if data[i]['id'] == int(request.form['id']):
                del data[i]
        f = open('concert.json', "w")
        f.write(json.dumps(data))
        f.close()
        return redirect(url_for('concert'))

    dataConcert=read_json("concert")
    return render_template("concert_bref.html", data=dataConcert, name="all")


@app.route("/ajouterconcert", methods=['GET', 'POST'])
def ajouterconcert():
    """ Permet d'ajouter un concert """
 #{"id": 1, "title": "Musilac 2024", "dateConcert" : "03/05/2024"}
    """ Ajoute l'actualité dans le fichier JSON si un POST a été effectué """
    if request.method == 'POST':
        write_json("concert", {'id': int(request.form['id']), 'title': request.form['title'], 'dateConcert': request.form['dateConcert']})
        return redirect(url_for('concert'))

    """ Détermine l'id de l'actualité à ajouter (max déjà existant + 1) """
    data=read_json("concert")
    max=0
    index=0
    for i in range(0,len(data)):
        if data[i]['id'] > max:
            max=data[i]['id']
            index=data[i]['id']+1
    
    """ Afficher le formulaire d'ajout de concert """
    return '''
    <a href="/concert"><button>Retour à la liste des concerts</button></a>
    <form method="post">
    <input type="hidden" name="id" value='''+str(index)+'''>
    <p><input disabled value='''+str(index)+''' type=text name=id>
    <p><input requiered placeholder=title type=text name=title>
    <p><label for=dateConcert>Date du concert</label>
    <p><input requiered placeholder=dateConcert type=date name=dateConcert>
    <p><input type=submit value=Envoyer>
    </form>

    '''


@app.route("/login", methods=['GET', 'POST'])
def login():
    """ Permet de se connecter """
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('actualite'))
    return '''
    <form method="post">
        <p><input requiered placeholder=username type=text name=username>
        <p><input requiered placeholder=password type=password name=password>
        <p><input type=submit value=Connexion>
    </form>

    '''
@app.route("/logout")
def logout():
    """ Permet de se déconnecter (enlève le nom d'utilisateur de la session)""" 
    session.pop('username', None)
    return redirect(url_for('actualite'))

@app.route("/actualites")
def actualite():
    """ Afficher les actualités """
    dataActualites=read_json("actualites")
    dataCommentaire=read_json("commentaire")
    return render_template("actualites.html", data=dataActualites, commentaire=dataCommentaire, name="all")

@app.route("/actualites/<name>")
def specific_actualite(name):
    """ Afficher les actualités par type """
    dataActualites=read_json("actualites")
    dataCommentaire=read_json("commentaire")
    return render_template("actualites.html", data=dataActualites, commentaire=dataCommentaire, name=name)

@app.route("/concert")
def concert():
    """ Afficher les concerts """
    dataActualites=read_json("concert")
    return render_template("concert.html", data=dataActualites)

@app.route("/commentaire", methods=["POST"])
def commentaire():
    """ Valider et écrire un commentaire """
    write_json("commentaire", {'actu': request.form['actu'], 'name': request.form['name'], 'commentaire': request.form['commentaire']})
    return redirect(url_for('actualite'))

def read_json(name):
    """ Lire dans un fichier Json """
    f = open(name + '.json')
    data = json.load(f)

    f.close()
    return data

def write_json(name, data):
    """ Ecrire dans un fichier Json existant """
    dataFromFile = read_json(name)
    f = open(name + '.json', "w")

    dataFromFile.append(data)

    f.write(json.dumps(dataFromFile))

    f.close()
    return data
