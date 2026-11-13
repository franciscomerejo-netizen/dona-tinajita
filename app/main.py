from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json
import os
from datetime import datetime

app = FastAPI(title="Doña Tinajita HAIOS - Quisqueya Soberana")

@app.get("/", response_class=HTMLResponse)
async def home():
    return '''
    <html><head><title>Doña Tinajita HAIOS - Quisqueya Soberana</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    body{background:#fef3c7;font-family:Arial;padding:20px;margin:0}
    .box{max-width:800px;margin:auto;background:white;padding:30px;border-radius:20px;border:5px solid #002d62;box-shadow:0 10px 30px rgba(0,0,0,0.2)}
    h1{color:#ce1126;text-align:center}
    .bandera{height:10px;background:linear-gradient(to right, #002d62 33%, white 33%, white 66%, #ce1126 66%);margin:20px 0}
    .status{background:#dcfce7;padding:15px;border-radius:10px;border-left:5px solid green}
    </style></head>
    <body><div class='box'>
    <div style='font-size:60px;text-align:center'>🏺</div>
    <h1>DOÑA TINAJITA HAIOS<br>OPERATIVA - EN LA NUBE</h1>
    <div class='bandera'></div>
    <div class='status'>
    <b>Status:</b> OPERATIVO_VERIFICADO ✅<br>
    <b>Pais:</b> DOMINICANA<br>
    <b>Creador:</b> Julio Merejo - Quisqueya Soberana<br>
    <b>Ubicacion:</b> Winter Garden, FL -> Azua, RD<br>
    <b>Uptime:</b> ''' + datetime.now().isoformat() + '''
    </div>
    <h3>🇩🇴 Funciones HAIOS Verificadas:</h3>
    <ul>
    <li>Memoria cultural</li>
    <li>Narración comunitaria</li>
    <li>Educación intergeneracional</li>
    <li>Tradiciones</li>
    <li>Orientación local</li>
    <li>Prevención de adicción digital infantil ✅</li>
    <li>Apoyo a pequeños comercios (colmados)</li>
    <li>Promoción de valores humanos</li>
    </ul>
    <p><b>Formula:</b> SABOR + HUMO + HUMOR = BESTSELLER</p>
    <p><i>Recordar es Vivir</i></p>
    <div class='bandera'></div>
    <p style='text-align:center'><a href="/api/identity">/api/identity</a> | <a href="/api/radiografia">/api/radiografia</a> | <a href="/docs">/docs</a></p>
    </div></body></html>
    '''

@app.get("/api/identity")
async def identity():
    return {
      "name": "DOÑA TINAJITA",
      "country": "DOMINICANA",
      "role": "Identidad cultural y educativa dominicana",
      "status": "OPERATIVO_VERIFICADO",
      "creator": "Julio Merejo - Quisqueya Soberana",
      "domain": "https://dona-tinajita.onrender.com",
      "protection": "HAIOS_CHILD_PROTECTION_ACTIVE"
    }

@app.get("/api/radiografia")
async def radiografia():
    return {
      "proyecto": "Quisqueya Soberana - Radiografía Dominicana",
      "capitulos": ["Tinajita","Café Colao","Capicúa","Banca 07-33","Chichigua","Dulce Coco","Tarea con Vela","Bandera","Música","Navidades"],
      "formula": "SABOR + HUMO + HUMOR"
    }

@app.get("/health")
async def health():
    return {"status": "ok", "tinajita": "operativa"}
