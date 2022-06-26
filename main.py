from urllib import response
from fastapi import FastAPI
from starlette.responses import RedirectResponse

app = FastAPI()

# redirection to DB
@app.get('/')
async def Redirect():
    return RedirectResponse(url='/dashboard')

@app.get('/dashboard')
def dashboard():
    return {'data' :{'dashboard'}}

@app.get('/heroes')
def Heroes():
    return {'data' :{'heroes page'}}

@app.get('/detail/{id}')
def detail(id : int):
    # id gestion for players
    return {'data': id}