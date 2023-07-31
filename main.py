import os
from fastapi import FastAPI, Request, Form, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# from pydantic import BaseModel

# class Taco_Fast_Food(BaseModel):
#     nombre: str
#     plato_favorito: str

app = FastAPI(title='Taco FastFood')

# templates = Jinja2Templates(directory="templates")
# templates = Jinja2Templates(directory=os.path.abspath(os.path.expanduser('templates')))
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))


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

@app.get('/taco-clients', response_class=HTMLResponse)
async def get_clients(request: Request):
    return templates.TemplateResponse(
        "index.html", 
        {"request": request,"taco_clients": taco_clients}
    )
 
#  Post urls
@app.get('/form', response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse(
        "post.html", 
        {"request": request}
    )

# obs:pip install python-multipart 
@app.post('/post-client')
async def post_client(nombre: str = Form(...), plato_favorito: str = Form(...)):
    taco_client_dict = {
        'id': len(taco_clients) + 1,
        'nombre': nombre,
        'plato_favorito': plato_favorito,
    } 
    
    taco_clients.append(taco_client_dict)
    return RedirectResponse(url=app.url_path_for("get_clients"), status_code=status.HTTP_303_SEE_OTHER)

# update urls
@app.get('/edit-client/{id}')
async def get_by_id(id: int, request: Request):
    id_int = int(id)
    client = get_client_by_id(id_int)
    return templates.TemplateResponse(
        "edit.html", 
        {"request": request, 'client': client}
    )

def get_client_by_id(id):
    client_id = {}
    for client in taco_clients:
       if client['id'] == id:
            client_id = client
    return client_id
    
@app.post('/update-client/{id}')
async def update_client(id: int, nombre: str = Form(...), plato_favorito: str = Form(...)):
    id_int = int(id)
    for client in taco_clients:
        if client['id'] == id_int:
            client['nombre'] = nombre
            client['plato_favorito'] = plato_favorito

    return RedirectResponse(url=app.url_path_for("get_clients"), status_code=status.HTTP_303_SEE_OTHER)

#  delete url
@app.get('/delete-client/{id}')
async def delete_client(id: int):
    id_int = int(id)
    for client in taco_clients:
        if client['id'] == id_int:
            taco_clients.remove(client)

    return RedirectResponse(url=app.url_path_for("get_clients"), status_code=status.HTTP_303_SEE_OTHER)




# Solução template
'''
raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: index.html
'''
#  https://www.appsloveworld.com/python/241/fastapi-jinja2-exceptions-templatenotfound-index-html