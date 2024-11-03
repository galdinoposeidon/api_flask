from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///escola.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelos
class Professor(db.Model):
    __tablename__ = 'professores'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    materia = db.Column(db.String(50), nullable=False)
    observacoes = db.Column(db.String(200))

class Turma(db.Model):
    __tablename__ = 'turmas'
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'), nullable=False)
    professor = db.relationship("Professor", backref="turmas")

class Aluno(db.Model):
    __tablename__ = 'alunos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    nota_primeiro_semestre = db.Column(db.Float, nullable=False)
    nota_segundo_semestre = db.Column(db.Float, nullable=False)
    media_final = db.Column(db.Float, nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey('turmas.id'), nullable=False)
    turma = db.relationship("Turma", backref="alunos")

    def __init__(self, nome, idade, data_nascimento, nota_primeiro_semestre, nota_segundo_semestre, media_final, turma_id):
        self.nome = nome
        self.idade = idade
        if isinstance(data_nascimento, str):
            self.data_nascimento = datetime.strptime(data_nascimento, '%Y-%m-%d').date()
        else:
            self.data_nascimento = data_nascimento
        self.nota_primeiro_semestre = nota_primeiro_semestre
        self.nota_segundo_semestre = nota_segundo_semestre
        self.media_final = media_final
        self.turma_id = turma_id

# Rotas Professor
@app.route('/professores/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_professor(id):
    professor = Professor.query.get(id)
    if not professor:
        return jsonify({"error": "Professor não encontrado"}), 404

    if request.method == 'GET':
        return jsonify({
            "id": professor.id,
            "nome": professor.nome,
            "idade": professor.idade,
            "materia": professor.materia,
            "observacoes": professor.observacoes
        })

    elif request.method == 'PUT':
        data = request.get_json()
        professor.nome = data.get('nome', professor.nome)
        professor.idade = data.get('idade', professor.idade)
        professor.materia = data.get('materia', professor.materia)
        professor.observacoes = data.get('observacoes', professor.observacoes)
        db.session.commit()
        return jsonify({"message": "Professor atualizado com sucesso"})

    elif request.method == 'DELETE':
        db.session.delete(professor)
        db.session.commit()
        return jsonify({"message": "Professor deletado com sucesso"})

# Rotas Turma
@app.route('/turmas/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_turma(id):
    turma = Turma.query.get(id)
    if not turma:
        return jsonify({"error": "Turma não encontrada"}), 404

    if request.method == 'GET':
        return jsonify({
            "id": turma.id,
            "descricao": turma.descricao,
            "ativo": turma.ativo,
            "professor_id": turma.professor_id
        })

    elif request.method == 'PUT':
        data = request.get_json()
        turma.descricao = data.get('descricao', turma.descricao)
        turma.ativo = data.get('ativo', turma.ativo)
        turma.professor_id = data.get('professor_id', turma.professor_id)
        db.session.commit()
        return jsonify({"message": "Turma atualizada com sucesso"})

    elif request.method == 'DELETE':
        db.session.delete(turma)
        db.session.commit()
        return jsonify({"message": "Turma deletada com sucesso"})

# Rotas Aluno
@app.route('/alunos/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_aluno(id):
    aluno = Aluno.query.get(id)
    if not aluno:
        return jsonify({"error": "Aluno não encontrado"}), 404

    if request.method == 'GET':
        return jsonify({
            "id": aluno.id,
            "nome": aluno.nome,
            "idade": aluno.idade,
            "data_nascimento": aluno.data_nascimento.strftime('%Y-%m-%d'),
            "nota_primeiro_semestre": aluno.nota_primeiro_semestre,
            "nota_segundo_semestre": aluno.nota_segundo_semestre,
            "media_final": aluno.media_final,
            "turma_id": aluno.turma_id
        })

    elif request.method == 'PUT':
        data = request.get_json()
        aluno.nome = data.get('nome', aluno.nome)
        aluno.idade = data.get('idade', aluno.idade)
        if 'data_nascimento' in data:
            aluno.data_nascimento = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()
        aluno.nota_primeiro_semestre = data.get('nota_primeiro_semestre', aluno.nota_primeiro_semestre)
        aluno.nota_segundo_semestre = data.get('nota_segundo_semestre', aluno.nota_segundo_semestre)
        aluno.media_final = data.get('media_final', aluno.media_final)
        aluno.turma_id = data.get('turma_id', aluno.turma_id)
        db.session.commit()
        return jsonify({"message": "Aluno atualizado com sucesso"})

    elif request.method == 'DELETE':
        db.session.delete(aluno)
        db.session.commit()
        return jsonify({"message": "Aluno deletado com sucesso"})

# Inicializa o banco de dados e executa a aplicação
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
