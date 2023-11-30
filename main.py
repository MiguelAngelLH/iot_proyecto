import fastapi
import sqlite3
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Create the database
conn = sqlite3.connect("sql/iot.db")  # Updated database name

app = fastapi.FastAPI()

class Contacto(BaseModel):
    id: int
    dispositivo: str
    valor: str

class Dispositivo(BaseModel):
    valor: str

# Origins
origins = [
    "http://localhost:8080",
]

# Cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    """Welcome message."""
    return {"message": "Bienvenido a mi api de iot!"}

@app.get("/dispositivos")
async def obtener_dispositivos():
    """Obtiene todos los dispositivos."""
    c = conn.cursor()
    c.execute('SELECT * FROM dispositivos;')  # Update query if needed
    response = []
    for row in c:
        dispositivo = {"id_dispositivo": row[0], "dispositivo": row[1], "valor": row[2]}
        response.append(dispositivo)
    return response

@app.get("/dispositivos/{id_dispositivo}")
async def obtener_valor_dispositivo(id_dispositivo: int):
    """Obtiene el valor de un dispositivo por su id_dispositivo."""
    c = conn.cursor()
    c.execute('SELECT valor FROM dispositivos WHERE id_dispositivo = ?', (id_dispositivo,))
    valor = c.fetchone()
    return {"valor": valor[0] if valor else None}


@app.put("/dispositivos/{id_dispositivo}/{nuevo_valor}")
async def actualizar_valor_dispositivo(id_dispositivo: int, nuevo_valor: str):
    """Actualiza el valor de un dispositivo por su id_dispositivo."""
    c = conn.cursor()
    c.execute('UPDATE dispositivos SET valor = ? WHERE id_dispositivo = ?', (nuevo_valor, id_dispositivo))
    conn.commit()
    return {"mensaje": "Valor actualizado"}