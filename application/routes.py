from application import app, db
from flask import request, jsonify, render_template, redirect
from application.models import FriendsCharacter
from application.forms import AddCharacterForm

def format_character(character):
    return {
        "name": character.name,
        "age": character.age,
        "catch_phrase": character.catch_phrase
    }

# @app.route("/characters", methods=["POST"])
# def create_character():
#     # Retrieved data from client
#     data = request.json
#     # Created a new character using the data
#     character = FriendsCharacter(data['name'], data['age'], data['catch_phrase'])
#     # Send character to datbase
#     db.session.add(character)
#     db.session.commit()
#     # Return JSON response back to the user/client
#     return jsonify(id=character.id, name=character.name, age=character.age, catch_phrase=character.catch_phrase)

# @app.route("/characters", methods=['GET'])
# def get_characters():
#     characters = FriendsCharacter.query.all()
#     character_list = []
#     for character in characters:
#         character_list.append(format_character(character))
#     return character_list
@app.route("/characters", methods=["POST", "GET"])
def characters():
    form = AddCharacterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            character = FriendsCharacter(form.name.data, form.age.data, form.catch_phrase.data)
            db.session.add(character)
            db.session.commit()
            return redirect('/')
        # else:
            #error handling
        # # Retrieved data from client
        # data = request.json
        # # Created a new character using the data
        # character = FriendsCharacter(data['name'], data['age'], data['catch_phrase'])
        # # Send character to the database
        # db.session.add(character)
        # db.session.commit()
        # # Return JSON response back to the user/client
        # return jsonify(id=character.id, name=character.name, age=character.age, catch_phrase=character.catch_phrase)
    else:
        characters = FriendsCharacter.query.all()
        character_list = []
        for character in characters:
            character_list.append(format_character(character))
        return render_template('characters.html', characters= character_list, form=form)

#Get /:id
@app.route('/characters/<id>')
def get_character(id):
    #filter_by
    character = FriendsCharacter.query.filter_by(id=id).first()
    return render_template("character.html", character=character)

# DELETE /:id
@app.route("/characters/<id>", methods=['DELETE'])
def delete_character(id):
    character = FriendsCharacter.query.filter_by(id=id).first()
    db.session.delete(character)
    db.session.commit()
    return f"Character deleted {id}"

# PATCH /:id
@app.route("/characters/<id>", methods=["PATCH"])
def update_character(id):
    character = FriendsCharacter.query.filter_by(id=id)
    data = request.json
    character.update(dict(name=data["name"], age=data["age"], catch_phrase=data["catch_phrase"]))
    #commit change to database
    db.session.commit()
    #retrieve specific character from the filtering
    updatedCharacter= character.first()
    #return Json response to clinet
    return jsonify(id=updatedCharacter.id, name=updatedCharacter.name, age=updatedCharacter.age, catch_phrase=updatedCharacter.catch_phrase)




