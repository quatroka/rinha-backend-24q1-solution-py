from db_pool import pool
from datetime import datetime
from psycopg.rows import dict_row


def client_data(cursor, client_id) -> dict | None:
    cursor.execute(
        """SELECT id, saldo, limite FROM clientes WHERE id = %s LIMIT 1;""",
        (client_id,),
    )
    return cursor.fetchone()


def do_transaction(client_id: int, transaction: dict) -> dict | None:
    if transaction['valor'] == 0:
        return
    if isinstance(transaction['valor'], float):
        return
    if transaction['descricao'] is None:
        return
    if len(transaction['descricao']) == 0:
        return
    if len(transaction['descricao']) > 10:
        return
    if transaction['tipo'] not in ('c', 'd'):
        return
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            with conn.transaction():
                cliente = client_data(cursor, client_id)
                if cliente is None:
                    return
                saldo_transaction = (
                    cliente['saldo'] - transaction['valor']
                    if transaction['tipo'] == 'd'
                    else cliente['saldo'] + transaction['valor']
                )
                if saldo_transaction >= -cliente['limite']:
                    conn.execute(
                        """INSERT INTO transactions(client_id, valor, tipo, descricao) 
                            VALUES (%s, %s, %s, %s);""",
                        (
                            client_id,
                            transaction['valor'],
                            transaction['tipo'],
                            transaction['descricao'],
                        ),
                    )
                    conn.execute(
                        """UPDATE clientes SET saldo = %s WHERE id = %s""",
                        (
                            saldo_transaction,
                            client_id,
                        ),
                    )
                    return {'limite': cliente['limite'], 'saldo': saldo_transaction}


def get_extrato(client_id: int) -> dict:
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            with conn.transaction():
                cursor.execute(
                    """SELECT id, saldo, limite FROM clientes WHERE id = %s LIMIT 1;""",
                    (client_id,),
                )
                cliente = cursor.fetchone()
                if cliente is None:
                    return
                cursor.execute(
                    """SELECT valor, tipo, descricao, realizada_em FROM transactions WHERE client_id = %s ORDER BY id DESC LIMIT 10;""",
                    (client_id,),
                )
                transactions = cursor.fetchall()
                return {
                    'saldo': {
                        'total': cliente['saldo'],
                        'data_extrato': format_datetime(datetime.now()),
                        'limite': cliente['limite'],
                    },
                    'ultimas_transacoes': [
                        {
                            'valor': x['valor'],
                            'tipo': x['tipo'],
                            'descricao': x['descricao'],
                            'realizada_em': format_datetime(x['realizada_em']),
                        }
                        for x in transactions
                    ],
                }


def format_datetime(date: datetime) -> str:
    return date.strftime('%Y-%m-%dT%H:%m:%S.%fZ')
