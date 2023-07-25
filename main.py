from fastapi import FastAPI
from pydantic import BaseModel

class Taco_Fast_Food(BaseModel):
    nombre: str
    plato_favorito: str

app = FastAPI(title='Taco FastFood')

taco_clients = [
    {
        'id': 1,
        'nombre': 'Jóse',
        'plato_favorito': 'Cuacamole',
    },
    {
        'id': 2,
        'nombre': 'Valetina',
        'plato_favorito': 'Chilli com carne',
    },
]

@app.get('/taco-clients/')
async def get():
    return taco_clients

@app.get('/taco-clients/{id}')
async def get(id: int):
    id_int = int(id)
    for client in taco_clients:
        if client['id'] == id_int:
            return client
    return {'Error': 'no encontrado'}

@app.post('/taco-clients/')
async def post_client(taco_client: Taco_Fast_Food):
    # taco_client_dict = taco_client.dict()
    taco_client_dict = taco_client.model_dump()
    taco_client_dict = {
        'id': len(taco_clients) + 1,
        'nombre': taco_client_dict['nombre'],
        'plato_favorito': taco_client_dict['plato_favorito'],
    }
    
    taco_clients.append(taco_client_dict)
    return taco_client_dict

@app.put('/taco-clients/{id}')
async def update_client(id: int, taco_client: Taco_Fast_Food):
    id_int = int(id)

    for client in taco_clients:
        if client['id'] == id_int:
            client['nombre'] = taco_client.nombre
            client['plato_favorito'] = taco_client.plato_favorito
            return client
    return {'Error': 'no encontrado'}

@app.delete('/taco-clients/{id}')
async def delete_client(id: int):
    id_int = int(id)
    for client in taco_clients:
        if client['id'] == id_int:
            taco_clients.remove(client)
            return {'msg': 'cliente eliminado'}
    return {'Error': 'no encontrado'}
