import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy as SQLAlchemy
from flask_marshmallow import Marshmallow as Marshmallow

# initialize Flask application

app = Flask(__name__)

# configure SQLite database

# Configure SQLite Database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'notes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# initialize SQLAlchemy and Marshmallow

db = SQLAlchemy(app)
ma = Marshmallow(app)


# define Note class


# Note Model
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __init__(self, title, content):
        self.title = title
        self.content = content


        # define schema for Note class

        class NoteSchema(ma.Schema):
            class Meta:
               model = Note

# Initialize schema
note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)



# Create a Note

@app.route('/notes', methods=['POST'])
def add_note():
    title = request.json['title']
    content = request.json['content']

    new_note = Note(title, content)

    db.session.add(new_note)
    db.session.commit()

    return note_schema.jsonify(new_note)

# Get All Notes
@app.route('/notes', methods=['GET'])
def get_notes():
    all_notes = Note.query.all()
    result = notes_schema.dump(all_notes)
    return jsonify(result)


# Get Single Note
@app.route('/note/<id>', methods=['GET'])
def get_note(id):
    note = Note.query.get(id)
    return note_schema.jsonify(note)

# Update a Note
@app.route('/note/<id>', methods=['PUT'])
def update_note(id):
    note = Note.query.get(id)
    
    title = request.json['title']
    content = request.json['content']
    
    note.title = title
    note.content = content
    db.session.commit()
    
    return note_schema.jsonify(note)


# Delete Note
@app.route('/note/<id>', methods=['DELETE'])
def delete_note(id):
    note = Note.query.get(id)
    db.session.delete(note)
    db.session.commit()
    
    return note_schema.jsonify(note)


from app import db
db.create_all()
exit()
