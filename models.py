from database import Database

class Missao:
    def __init__(self, nome, data_lancamento, destino, estado, tripulacao, carga_util, duracao, custo, status):
        self.nome = nome
        self.data_lancamento = data_lancamento
        self.destino = destino
        self.estado = estado
        self.tripulacao = tripulacao
        self.carga_util = carga_util
        self.duracao = duracao
        self.custo = custo
        self.status = status

    def save_to_db(self):
        query = '''
            INSERT INTO missoes (nome, data_lancamento, destino, estado, tripulacao, carga_util, duracao, custo, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        params = (self.nome, self.data_lancamento, self.destino, self.estado, self.tripulacao, self.carga_util, self.duracao, self.custo, self.status)
        db = Database()
        db.execute_query(query, params, commit=True)

    @staticmethod
    def update_missao(id, nome, data_lancamento, destino, estado, tripulacao, carga_util, duracao, custo, status):
        query = '''
            UPDATE missoes SET nome = ?, data_lancamento = ?, destino = ?, estado = ?, tripulacao = ?, carga_util = ?, duracao = ?, custo = ?, status = ?
            WHERE id = ?
        '''
        params = (nome, data_lancamento, destino, estado, tripulacao, carga_util, duracao, custo, status, id)
        db = Database()
        db.execute_query(query, params, commit=True)

    @staticmethod
    def delete_missao(id):
        query = 'DELETE FROM missoes WHERE id = ?'
        db = Database()
        db.execute_query(query, (id,), commit=True)

    @staticmethod
    def search_by_date_range(data_inicio, data_fim):
        query = '''
            SELECT * FROM missoes
            WHERE data_lancamento BETWEEN ? AND ?
            ORDER BY data_lancamento DESC
        '''
        db = Database()
        return db.execute_query(query, (data_inicio, data_fim))
