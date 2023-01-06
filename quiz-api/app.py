import sqlite3
from flask import Flask, jsonify, request, abort
import jwt
from flask_cors import CORS
import os
import json
from operator import itemgetter
from datetime import datetime , timedelta
from functools import wraps

currentdirectory = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = '74ebc58d13224d0daa4989a8734133ea'

def token_required(func):
    @wraps(func)
    def decorated(*args , **kwargs):
        token = request.args.get('token')
        if not token:
           return jsonify({'Alert!':'Tocken is missing ! '})
        try:
            payload = jwt.decode(token,app.config['SECRET_KEY']) 
        except:
          return jsonify({'Alert!': 'Invalid Token!'})
    return decorated

@app.route('/login',methods=['POST'])
def login():
  if request.form['username'] and request.form['password'] == '123456':
      session['logged_in'] = True 
      token = jwt.encode({
          'user':request.form['username'],
          'expiration':str(datetime.utcnow() + timedelta(seconds=120))
      },
          app.config['SECRET_KEY'])
      return jsonify({'token':token.decode('utf-8')})
  else:
    return make_response(' Password : Wrong ', 401 , {'WWW-Authenticate': 'Basic realm:"Authentification Failed !'})
if __name__ == "__main__":
    app.run(debug=True)

CORS(app)

class Question():
	def init(self, title: str, text, image, position, possibleAnswers):
		self.title = title
		self.text = text
		self.image = image
		self.position = position
		self.possibleAnswers = possibleAnswers



def get_db_connection():
    connection = sqlite3.connect(currentdirectory + "\quiz.db")
    connection.row_factory = sqlite3.Row
    return connection

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	conn = get_db_connection()
	size = conn.execute("SELECT count(*) FROM questions").fetchone()[0]
	participations = conn.execute("SELECT playerName, score FROM participations").fetchall()
	scores = []
	for row in participations:
		scores.append({'playerName' : row[0],'score': row[1]})
	conn.close()
	sorted_scores = sorted(scores, key=itemgetter('score'), reverse=True)
	return {"size": size, "scores": sorted_scores}

@app.route('/get-questions', methods=['GET'])
def GetQuestion():
	c = get_db_connection()
	rows = c.execute("SELECT * FROM questions").fetchall()
	data = []
	for row in rows:
		data.append({'id': row[0], 'title': row[1], 'text': row[2], 'image': row[3], 'position': row[4], 'possibleAnswers': json.loads(row[5])})
	c.close()
	return jsonify(data)

@app.route('/questions', methods=['POST'])
def AddQuestion():
	title = request.json['title']
	text = request.json['text']
	image = request.json['image']
	position = request.json['position']
	possibleAnswers = json.dumps(request.json['possibleAnswers'])
	conn = get_db_connection()
	conn.execute("INSERT INTO questions (title, text, image, position, possibleAnswers) VALUES (?,?,?,?,?)",(title, text, image, position, possibleAnswers))
	conn.commit()
	id = conn.cursor().lastrowid
	conn.close()
	return {"id" : id}, 200

@app.route('/questions', methods=['GET'])
def getQuestionPosition():
	position = request.args.get("position")
	conn = get_db_connection()
	row = conn.execute("SELECT * FROM questions WHERE position = ?",
                        (position,)).fetchone()
	conn.close()
	data = []
	data.append({'id': row[0], 'title': row[1], 'text': row[2], 'image': row[3], 'position': row[4], 'possibleAnswers': json.loads(row[5])})
	return jsonify(data)

@app.route('/questions/<id>', methods=['GET'])
def show_question(id):
	# retrieve the question with the specified ID from the database
	conn = get_db_connection()
	row = conn.execute("SELECT * FROM questions WHERE id = ?",
                        (id)).fetchone()
	conn.close()
	data = []
	data.append({'id': row[0], 'title': row[1], 'text': row[2], 'image': row[3], 'position': row[4], 'possibleAnswers': json.loads(row[5])})
	return jsonify(data)

@app.route('/participations', methods=['POST'])
def AddParticipation():
	playerName = request.json['playerName']
	playerAnswers = request.json['answers']
	if len(playerAnswers) < 10 or len(playerAnswers) > 10:
		abort(400)
	score = 0
	conn = get_db_connection()
	questionsRows = conn.execute("SELECT possibleAnswers FROM questions").fetchall()
	answers = []
	for row in questionsRows:
		answers.append({'answer': json.loads(row[0])})
	correctAnswers = []
	for answer in answers:
		for i, a in enumerate(answer['answer']):
			if a['isCorrect']:
				correctAnswers.append(i+1)
				break
	# Iterate over the elements in array1
	for i in range(len(playerAnswers)):
        # If the elements at index i in the two arrays are equal, increase the score
		if playerAnswers[i] == correctAnswers[i]:
			score += 1
	conn.execute("INSERT INTO participations (playerName, answers, score) VALUES (?,?,?)",(playerName, json.dumps(playerAnswers), score))
	conn.commit()
	conn.close()
	
	return {'playerName' : playerName, 'score' : score}

@app.route('/participations/all', methods=['DELETE'])
def delete_all_participations():
    # Connect to the database
    c = get_db_connection()

    # Delete all participations from the database
    c.execute('DELETE FROM participations')
    c.commit()

    # Close the connection to the database
    c.close()

    # Return a response with status code 204
    return '', 204

@app.route('/questions/all', methods=['DELETE'])
def delete_all_questions():
    # Connect to the database
    c = get_db_connection()

    # Delete all rows from the questions table
    c.execute('DELETE FROM questions')
    c.commit()

    # Close the connection to the database
    c.close()

    # Return a response with status code 204
    return '', 204

if __name__ == "__main__":
    app.run()