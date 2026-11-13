from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import json
import os
from datetime import datetime

# Stripe - se activa cuando pongas las keys
try:
    import stripe
    STRIPE_AVAILABLE = True
    stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_pon_tu_key_aqui")
    STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY", "pk_test_pon_tu_key_aqui")
except:
    STRIPE_AVAILABLE = False

app = FastAPI(title="Doña Tinajita HAIOS - Tienda con Pagos")

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
        precio_centavos = int(p['precio'] * 100)
        boton_pago = ""
        if p['precio'] > 0:
            boton_pago = f'''
            <form action="/create-checkout-session/{p['id']}" method="POST" style="margin-top:10px">
                <button type="submit" style="background:#635bff;color:white;padding:10px 20px;border:none;border-radius:20px;cursor:pointer;font-weight:bold">
                    💳 Comprar - \ - Pagar con Stripe
                </button>
            </form>
            '''
        else:
            boton_pago = '<span style="background:gray;color:white;padding:5px 10px;border-radius:10px">PROXIMAMENTE</span>'

        html_productos += f'''
        <div style="border:2px solid #002d62;border-radius:15px;padding:15px;margin:15px 0;background:#fffbeb">
            <b style="font-size:18px">{p['nombre']}</b> - {p['tipo']}<br>
            <small>{p['descripcion']}</small><br>
            <div style="margin:10px 0">
                <span style="font-size:20px;font-weight:bold;color:#ce1126">\ {p['moneda']}</span>
                <span style="background:green;color:white;padding:2px 8px;border-radius:10px;margin-left:10px">{p['status']}</span>
            </div>
            {boton_pago}
        </div>
        '''

    return f'''
    <html><head><title>Doña Tinajita - Tienda con Pagos</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    body{{background:#fef3c7;font-family:Arial;padding:20px;margin:0}}
    .box{{max-width:900px;margin:auto;background:white;padding:30px;border-radius:20px;border:5px solid #002d62}}
    h1{{color:#ce1126;text-align:center}} .bandera{{height:10px;background:linear-gradient(to right, #002d62 33%, white 33%, white 66%, #ce1126 66%);margin:20px 0}}
    .status{{background:#dcfce7;padding:15px;border-radius:10px;border-left:5px solid green}}
    .stripe-info{{background:#f0f0ff;padding:15px;border-radius:10px;border-left:5px solid #635bff;margin:20px 0}}
    </style></head>
    <body><div class='box'>
    <div style='font-size:60px;text-align:center'>🏺🛒💳</div>
    <h1>DOÑA TINAJITA HAIOS<br>TIENDA QUISQUEYA SOBERANA<br><small style="font-size:16px">CON PAGOS STRIPE</small></h1>
    <div class='bandera'></div>
    <div class='status'>
    <b>Status:</b> OPERATIVO_VERIFICADO ✅ TIENDA ACTIVA ✅ PAGOS ACTIVOS<br>
    <b>País:</b> DOMINICANA<br>
    <b>Creador:</b> Julio Merejo - Winter Garden FL -> Azua RD<br>
    <b>Uptime:</b> {datetime.now().isoformat()}<br>
    <b>Productos:</b> {len(productos)} productos<br>
    <b>Pagos:</b> Stripe {'✅ ACTIVO' if STRIPE_AVAILABLE else '⏳ Configurar keys en Render'}
    </div>
    <div class='stripe-info'>
    <b>💳 Pagos con Stripe:</b> Acepta tarjetas 【entity-Visa¦canonical_name=Visa】, 【entity-Mastercard¦canonical_name=Mastercard】, 【entity-Amex¦canonical_name=Amex】 desde RD, USA, Europa. Dinero directo a tu cuenta bancaria. Comisión Stripe 2.9% + 30¢.<br>
    <small>Configura STRIPE_SECRET_KEY y STRIPE_PUBLISHABLE_KEY en Render -> Environment</small>
    </div>
    <h3>🛒 Productos con Sabor, Humo y Humor - Compra Ahora:</h3>
    {html_productos}
    <div class='bandera'></div>
    <p style='text-align:center'>
    <a href="/api/identity">Identity</a> | <a href="/api/productos">Productos API</a> | <a href="/success">Success Demo</a> | <a href="/docs">Docs</a>
    </p>
    <p style='text-align:center'><b>Formula:</b> SABOR + HUMO + HUMOR = BESTSELLER + DOLARES<br><i>Recordar es Vivir y Cobrar también</i></p>
    </div></body></html>
    '''

@app.post("/create-checkout-session/{product_id}")
async def create_checkout(product_id: str, request: Request):
    productos = cargar_productos()
    producto = next((p for p in productos if p['id'] == product_id), None)
    if not producto:
        return {"error": "Producto no encontrado"}

    # Si no hay Stripe keys configuradas, mostrar pagina de configuracion
    if not os.getenv("STRIPE_SECRET_KEY"):
        return HTMLResponse(f'''
        <html><body style="background:#fef3c7;padding:50px;font-family:Arial;text-align:center">
        <div style="max-width:600px;margin:auto;background:white;padding:30px;border-radius:20px;border:5px solid #002d62">
        <h1>⏳ Configurar Stripe</h1>
        <p>Para cobrar por <b>{producto['nombre']}</b> - \</p>
        <p>Ve a <a href="https://dashboard.stripe.com/apikeys" target="_blank">dashboard.stripe.com/apikeys</a> y copia tus keys</p>
        <p>Luego en Render: Dashboard -> dona-tinajita -> Environment -> Add:<br>
        STRIPE_SECRET_KEY = sk_test_...<br>
        STRIPE_PUBLISHABLE_KEY = pk_test_...</p>
        <p><a href="/">Volver a tienda</a></p>
        </div></body></html>
        ''')

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': producto['nombre'], 'description': producto['descripcion']},
                    'unit_amount': int(producto['precio'] * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=str(request.base_url) + 'success',
            cancel_url=str(request.base_url),
        )
        return RedirectResponse(checkout_session.url, status_code=303)
    except Exception as e:
        return HTMLResponse(f"<h1>Error Stripe: {e}</h1><a href='/'>Volver</a>")

@app.get("/success", response_class=HTMLResponse)
async def success():
    return '''
    <html><body style="background:#dcfce7;padding:50px;font-family:Arial;text-align:center">
    <div style="max-width:600px;margin:auto;background:white;padding:40px;border-radius:20px;border:5px solid green">
    <div style="font-size:80px">🎉</div>
    <h1 style="color:green">¡PAGO EXITOSO!</h1>
    <h2>Wepa mi hijo! ¡Gracias por tu compra!</h2>
    <p>Doña Tinajita te manda un abrazo desde Azua con sabor a café colao</p>
    <p><b>Tu libro/producto te llega por email en 5 minutos</b></p>
    <p style="font-size:30px">🏺☕📚</p>
    <p><i>Recordar es Vivir - Julio Merejo - Quisqueya Soberana</i></p>
    <a href="/" style="background:#ce1126;color:white;padding:15px 30px;border-radius:20px;text-decoration:none;font-weight:bold">Volver a Tienda</a>
    </div></body></html>
    '''

@app.get("/api/identity")
async def identity():
    return {"name":"DOÑA TINAJITA","country":"DOMINICANA","status":"OPERATIVO_VERIFICADO","payments":"STRIPE_ACTIVE","domain":"https://dona-tinajita.onrender.com"}

@app.get("/api/productos")
async def productos():
    return cargar_productos()
