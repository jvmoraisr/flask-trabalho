from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Rota principal - Exibe lista de missões
@app.route('/')
def index():
    conn = get_db_connection()
    missoes = conn.execute('SELECT * FROM missoes ORDER BY data_lancamento DESC;').fetchall()
    conn.close()
    return render_template('index.html', missoes=missoes)

# Rota para criar nova missão
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        nome = request.form['nome']
        data_lancamento = request.form['data_lancamento']
        destino = request.form['destino']
        estado = request.form['estado']
        tripulacao = request.form['tripulacao']
        carga_util = request.form['carga_util']
        duracao = request.form['duracao']
        custo = request.form['custo']
        status = request.form['status']

        conn = get_db_connection()
        conn.execute('INSERT INTO missoes (nome, data_lancamento, destino, estado, tripulacao, carga_util, duracao, custo, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                     (nome, data_lancamento, destino, estado, tripulacao, carga_util, duracao, custo, status))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('create.html')

# Rota para editar missão existente
@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    conn = get_db_connection()
    missao = conn.execute('SELECT * FROM missoes WHERE id = ?;', (id,)).fetchone()

    if request.method == 'POST':
        nome = request.form['nome']
        data_lancamento = request.form['data_lancamento']
        destino = request.form['destino']
        estado = request.form['estado']
        tripulacao = request.form['tripulacao']
        carga_util = request.form['carga_util']
        duracao = request.form['duracao']
        custo = request.form['custo']
        status = request.form['status']

        conn.execute('UPDATE missoes SET nome = ?, data_lancamento = ?, destino = ?, estado = ?, tripulacao = ?, carga_util = ?, duracao = ?, custo = ?, status = ? WHERE id = ?;',
                     (nome, data_lancamento, destino, estado, tripulacao, carga_util, duracao, custo, status, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit.html', missao=missao)

# Rota para deletar missão
@app.route('/delete/<int:id>', methods=('POST',))
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM missoes WHERE id = ?;', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Inicializa o banco de dados
def init_db():
    conn = get_db_connection()
    conn.execute('''
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
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
