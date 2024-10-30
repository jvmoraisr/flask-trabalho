from flask import Flask, render_template, request, redirect, url_for
from models import Missao
from database import Database

app = Flask(__name__)

# Rota principal - Exibe lista de missões
@app.route('/')
def index():
    db = Database()
    missoes = db.execute_query('SELECT * FROM missoes ORDER BY data_lancamento DESC;')
    return render_template('index.html', missoes=missoes)

# Rota para criar nova missão
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        try:
            missao = Missao(
                nome=request.form['nome'],
                data_lancamento=request.form['data_lancamento'],
                destino=request.form['destino'],
                estado=request.form['estado'],
                tripulacao=request.form['tripulacao'],
                carga_util=request.form['carga_util'],
                duracao=request.form['duracao'],
                custo=request.form['custo'],
                status=request.form['status']
            )
            missao.save_to_db()
            return redirect(url_for('index'))
        except Exception as e:
            print(f"Erro ao criar missão: {e}")
            return render_template('error.html', message="Erro ao criar missão.")

    return render_template('create.html')

# Rota para pesquisar missões por intervalo de datas
@app.route('/search', methods=('GET', 'POST'))
def search():
    if request.method == 'POST':
        try:
            data_inicio = request.form['data_inicio']
            data_fim = request.form['data_fim']
            missoes = Missao.search_by_date_range(data_inicio, data_fim)
            return render_template('search_results.html', missoes=missoes)
        except Exception as e:
            print(f"Erro ao pesquisar missões: {e}")
            return render_template('error.html', message="Erro ao pesquisar missões.")

    return redirect(url_for('index'))

# Rota para editar missão existente
@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    db = Database()
    missao = db.execute_query('SELECT * FROM missoes WHERE id = ?;', (id,))

    if request.method == 'POST':
        try:
            Missao.update_missao(
                id=id,
                nome=request.form['nome'],
                data_lancamento=request.form['data_lancamento'],
                destino=request.form['destino'],
                estado=request.form['estado'],
                tripulacao=request.form['tripulacao'],
                carga_util=request.form['carga_util'],
                duracao=request.form['duracao'],
                custo=request.form['custo'],
                status=request.form['status']
            )
            return redirect(url_for('index'))
        except Exception as e:
            print(f"Erro ao editar missão: {e}")
            return render_template('error.html', message="Erro ao editar missão.")

    return render_template('edit.html', missao=missao[0])

# Rota para deletar missão
@app.route('/delete/<int:id>', methods=('POST',))
def delete(id):
    try:
        Missao.delete_missao(id)
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Erro ao deletar missão: {e}")
        return render_template('error.html', message="Erro ao deletar missão.")

# Inicializa o banco de dados
def init_db():
    db = Database()
    db.execute_query('''
        CREATE TABLE IF NOT EXISTS missoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            data_lancamento DATE NOT NULL,
            destino TEXT NOT NULL,
            estado TEXT NOT NULL,
            tripulacao TEXT NOT NULL,
            carga_util TEXT NOT NULL,
            duracao TEXT NOT NULL,
            custo DECIMAL NOT NULL,
            status TEXT
        );
    ''', commit=True)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
