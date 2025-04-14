from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(250), nullable=False)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return jsonify({"Message": "Secure Notes API - This is a tester message to see if it works, fingers crossed! "})

@app.route('/notes', methods=['GET'])
def get_notes():
    notes = Note.query.all()
    return jsonify([{'id': n.id, 'title': n.title, 'content': n.content} for n in notes])


@app.route('/notes', methods=['POST'])
def add_note ():
    data = request.get_json()
    new = Note(title=data["title"], content=data["content"])
    db.session.add(new)
    db.session.commit()
    return jsonify({"Message": "Note Added Sucessfully!"}), 201

@app.route('/notes/<int:id>', methods=['DELETE'])
def del_note(id):
     note = Note.query.get(id)
     if note is None:
         return {"error" : "note is not found"}
    
     db.session.delete(note)
     db.session.commit()
     return {"message" : f"Succesful deleted note at: {id}"}, 200
    


if __name__ == '__main__':
    app.run(debug=True)
