from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json
import os
from datetime import datetime

app = FastAPI(title="Doña Tinajita HAIOS - Tienda Quisqueya Soberana")

# Cargar productos
def cargar_productos():
    try:
        with open("data/productos_quisqueya.json","r",encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

@app.get("/", response_class=HTMLResponse)
async def home():
    productos = cargar_productos()
    html_productos = ""
    for p in productos:
        html_productos += f'''
        <div style="border:2px solid #002d62;border-radius:15px;padding:15px;margin:10px 0;background:#fffbeb">
            <b>{p['nombre']}</b> - {p['tipo']} - \ {p['moneda']}<br>
            <small>{p['descripcion']}</small><br>
            <span style="background:green;color:white;padding:2px 8px;border-radius:10px">{p['status']}</span>
        </div>
        '''

    return f'''
    <html><head><title>Doña Tinajita - Tienda</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    body{{background:#fef3c7;font-family:Arial;padding:20px;margin:0}}
    .box{{max-width:900px;margin:auto;background:white;padding:30px;border-radius:20px;border:5px solid #002d62}}
    h1{{color:#ce1126;text-align:center}} .bandera{{height:10px;background:linear-gradient(to right, #002d62 33%, white 33%, white 66%, #ce1126 66%);margin:20px 0}}
    .status{{background:#dcfce7;padding:15px;border-radius:10px;border-left:5px solid green}}
    </style></head>
    <body><div class='box'>
    <div style='font-size:60px;text-align:center'>🏺🛒</div>
    <h1>DOÑA TINAJITA HAIOS<br>TIENDA QUISQUEYA SOBERANA</h1>
    <div class='bandera'></div>
    <div class='status'>
    <b>Status:</b> OPERATIVO_VERIFICADO ✅ TIENDA ACTIVA<br>
    <b>País:</b> DOMINICANA<br>
    <b>Creador:</b> Julio Merejo - Winter Garden FL -> Azua RD<br>
    <b>Uptime:</b> {datetime.now().isoformat()}<br>
    <b>Productos:</b> {len(productos)} productos con Sabor Humo Humor
    </div>
    <h3>🛒 Productos con Sabor, Humo y Humor:</h3>
    {html_productos}
    <div class='bandera'></div>
    <p style='text-align:center'>
    <a href="/api/identity">Identity</a> | <a href="/api/productos">Productos API</a> | <a href="/api/radiografia">Radiografia</a> | <a href="/docs">Docs</a>
    </p>
    <p style='text-align:center'><b>Formula:</b> SABOR + HUMO + HUMOR = BESTSELLER<br><i>Recordar es Vivir</i></p>
    </div></body></html>
    '''

@app.get("/api/identity")
async def identity():
    return {{"name":"DOÑA TINAJITA","country":"DOMINICANA","role":"Identidad cultural y educativa dominicana + Tienda Quisqueya Soberana","status":"OPERATIVO_VERIFICADO","creator":"Julio Merejo","products":len(cargar_productos()),"domain":"https://dona-tinajita.onrender.com"}}

@app.get("/api/productos")
async def productos():
    return cargar_productos()

@app.get("/api/radiografia")
async def radiografia():
    return {{"proyecto":"Quisqueya Soberana","capitulos":["Tinajita","Café Colao","Capicúa","Banca 07-33","Chichigua","Dulce Coco","Tarea con Vela"],"formula":"SABOR + HUMO + HUMOR","productos":cargar_productos()}}

@app.get("/health")
async def health():
    return {{"status":"ok","tinajita":"operativa","tienda":"activa"}}
