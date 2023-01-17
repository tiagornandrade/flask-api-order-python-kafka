from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

@app.route("/", methods=["POST"])
def create_event():
    if request.method == 'POST':
        content = request.get_json()
        return jsonify(content) 
        msg = ''
    if request.method == 'POST': 
        email       = request.form['email']
        password    = request.form['password']
        first_name  = request.form['first_name']
        last_name   = request.form['last_name']
        criacao     = datetime.now().strftime('%Y%m%d')
        alteracao   = None
    
        cursor.execute('INSERT INTO usuario (email, password, first_name, last_name, criacao, alteracao) VALUES (?,?,?,?,?,?)', (email,password,first_name,last_name,criacao,alteracao))
        cursor.commit()
        msg = 'Registro efetuado com sucesso!'
        return redirect(url_for('registrar'))
    else:
        None

@app.route("/test", methods=["GET"])
def open_event():
    response = requests.get('http://localhost:5000').text
    # data = json.loads(response)
    data = response
    return data

if __name__ == "__main__":
    app.run(debug=True)