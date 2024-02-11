from fastapi import FastAPI, Response, Body
from actions import *

app = FastAPI()


@app.post('/clientes/{client_id}/transacoes')
def read_root(
    client_id: int, response: Response, request: dict = Body(...)
) -> Response:
    # print(request)
    if result := do_transaction(client_id, request):
        return result
    response.status_code = 422
    return response


@app.get('/clientes/{client_id}/extrato')
def read_item(client_id: int, response: Response) -> dict:
    if result := get_extrato(client_id):
        return result
    response.status_code = 404
    return response
