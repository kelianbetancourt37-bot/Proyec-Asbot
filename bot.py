import sys
import os
import json
import time

# ==========================================
# 1. CONFIGURACIÓN INICIAL Y ARCHIVOS
# ==========================================
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

DB_FILE = "usuarios.json"

def cargar_todos_los_datos():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def guardar_todos_los_datos(datos):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

base_datos = cargar_todos_los_datos()


# ==========================================
# 2. LECTURA DE DATOS (MENSAJES Y USUARIO)
# ==========================================
args = sys.argv[1:]
mensaje_recibido = ".menu"
parametro = ""
usuario_id = "usuario_general"

if len(sys.argv) > 1 and str(sys.argv[1]) != "None":
    texto_completo = str(sys.argv[1]).strip()
    partes_iniciales = texto_completo.split(" ", 1)
    mensaje_recibido = partes_iniciales[0].lower()
    if len(partes_iniciales) > 1:
        parametro = partes_iniciales[1].strip()

if len(sys.argv) > 2 and str(sys.argv[2]) != "None" and str(sys.argv[2]).strip() != "":
    parametro = str(sys.argv[2]).strip()

if len(sys.argv) > 3 and str(sys.argv[3]) != "None":
    usuario_id = str(sys.argv[3]).strip()

tiempo_actual = time.time()
if len(sys.argv) > 4 and str(sys.argv[4]) != "None":
    try:
        tiempo_mensaje = float(sys.argv[4])
        if (tiempo_actual - tiempo_mensaje) > 30:
            sys.exit(0)
    except (ValueError, TypeError):
        pass

# Crear perfil básico si el usuario es nuevo
if usuario_id not in base_datos:
    base_datos[usuario_id] = {
        "monedas": 500, "banco": 0, "racha": 0, "nivel": 1, "experiencia": 0,
        "nivel_progreso": "[░░░░░░░░░░] 0%", "inventario": [],
        "ultimo_trabajo": 0, "ultimo_diario": 0, "ultimo_cofre": 0, "ultimo_crimen": 0
    }
    guardar_todos_los_datos(base_datos)

datos_usuario = base_datos[usuario_id]
monedas_usuario = datos_usuario.get("monedas", 500)
banco_usuario = datos_usuario.get("banco", 0)
racha_usuario = datos_usuario.get("racha", 0)
ultimo_trabajo = datos_usuario.get("ultimo_trabajo", 0)
ultimo_diario = datos_usuario.get("ultimo_diario", 0)
ultimo_cofre = datos_usuario.get("ultimo_cofre", 0)
ultimo_crimen = datos_usuario.get("ultimo_crimen", 0)


# ==========================================
# 3. IMPORTACIÓN DE MÓDULOS (CON RESPALDOS)
# ==========================================

# Módulo: Menú y Administración
try:
    from menu import mostrar_menu
except ImportError:
    def mostrar_menu(): return "📜 *MENÚ PRINCIPAL*\nUsa .help para ayuda."

# Módulo: Economía y Juegos
try:
    from economy import (procesar_trabajar, procesar_diario, procesar_cofre,
                         procesar_crimen, procesar_depositar, procesar_retirar, 
                         procesar_banco, procesar_Mercado, procesar_comprar, procesar_inventario, procesar_apostar)
except ImportError:
    def procesar_trabajar(u, m, t): return m, t, "⚠️ Módulo de economía no disponible."
    def procesar_diario(u, m, r, t): return m, r, t, "⚠️ Módulo de economía no disponible."
    def procesar_cofre(u, m, r, t): return m, r, t, "⚠️ Módulo de economía no disponible."
    def procesar_crimen(u, m, t): return m, t, "⚠️ Módulo de economía no disponible."
    def procesar_depositar(m, b, c): return m, b, "⚠️ Módulo de economía no disponible."
    def procesar_retirar(m, b, c): return m, b, "⚠️ Módulo de economía no disponible."
    def procesar_banco(m, b): return m, b, "⚠️ Módulo de economía no disponible."
    def procesar_Mercado(m, b, p): return "🛒 *MERCADO GENERAL*\n• `.mercado` - Ver artículos disponibles."
    def procesar_comprar(datos_usuario, parametro=""): return "🛍️ *TIENDA*\n• `.comprar <item>` - Adquiere artículos."
    def procesar_inventario(u, d): return "⚠️ Módulo de inventario no disponible."
    def procesar_apostar(d, p): return "⚠️ Módulo de apuesta no disponible."

# ==========================================
# 4. NÚCLEO DE COMANDOS (EL CEREBRO)
# ==========================================
def ejecutar_bot():
    global base_datos, datos_usuario, monedas_usuario, banco_usuario, racha_usuario, ultimo_trabajo, ultimo_diario, ultimo_cofre, ultimo_crimen

    # --- APARTADO: MENÚS ---
    if mensaje_recibido in [".menu", ".help"]:
        return mostrar_menu()

    # --- APARTADO: ECONOMÍA Y JUEGOS ---
    elif mensaje_recibido in [".trabajar", ".work", ".w", ".wb"]:
        monedas_usuario, ultimo_trabajo, respuesta = procesar_trabajar(usuario_id, monedas_usuario, ultimo_trabajo)
        datos_usuario["monedas"] = monedas_usuario
        datos_usuario["ultimo_trabajo"] = ultimo_trabajo
        guardar_todos_los_datos(base_datos)
        return respuesta

    elif mensaje_recibido in [".crimen", ".crime"]:
        monedas_usuario, ultimo_crimen, respuesta = procesar_crimen(usuario_id, monedas_usuario, ultimo_crimen)
        datos_usuario["monedas"] = monedas_usuario
        datos_usuario["ultimo_crimen"] = ultimo_crimen
        guardar_todos_los_datos(base_datos)
        return respuesta

    elif mensaje_recibido in [".cofre", ".daily"]:
        if mensaje_recibido == ".daily":
            monedas_usuario, racha_usuario, ultimo_diario, respuesta = procesar_diario(usuario_id, monedas_usuario, racha_usuario, ultimo_diario)
            datos_usuario["ultimo_diario"] = ultimo_diario
        else:
            monedas_usuario, racha_usuario, ultimo_cofre, respuesta = procesar_cofre(usuario_id, monedas_usuario, racha_usuario, ultimo_cofre)
            datos_usuario["ultimo_cofre"] = ultimo_cofre
        datos_usuario["monedas"] = monedas_usuario
        datos_usuario["racha"] = racha_usuario
        guardar_todos_los_datos(base_datos)
        return respuesta

    elif mensaje_recibido in [".depositar", ".dep", ".d"]:
        cantidad = parametro.lower()
        cantidad_num = monedas_usuario if (cantidad == "all" or cantidad == "todo") else int(cantidad) if cantidad.isdigit() else 0
        monedas_usuario, banco_usuario, respuesta = procesar_depositar(monedas_usuario, banco_usuario, cantidad_num)
        datos_usuario["monedas"] = monedas_usuario
        datos_usuario["banco"] = banco_usuario
        guardar_todos_los_datos(base_datos)
        return respuesta

    elif mensaje_recibido in [".retirar", ".ret", ".r"]:
        cantidad = parametro.lower()
        cantidad_num = banco_usuario if (cantidad == "all" or cantidad == "todo") else int(cantidad) if cantidad.isdigit() else 0
        monedas_usuario, banco_usuario, respuesta = procesar_retirar(monedas_usuario, banco_usuario, cantidad_num)
        datos_usuario["monedas"] = monedas_usuario
        datos_usuario["banco"] = banco_usuario
        guardar_todos_los_datos(base_datos)
        return respuesta

    elif mensaje_recibido in [".banco", ".bank"]:
        _, _, respuesta = procesar_banco(monedas_usuario, banco_usuario)
        return respuesta

    elif mensaje_recibido in [".comprar", ".buy"]:
        respuesta = procesar_comprar(datos_usuario, parametro)
        guardar_todos_los_datos(base_datos)
        return respuesta

    elif mensaje_recibido.startswith(".apostar"):
        partes = mensaje_recibido.split()
        param = partes[1] if len(partes) > 1 else parametro if parametro else "0"
        respuesta = procesar_apostar(datos_usuario, param)
        guardar_todos_los_datos(base_datos)
        return respuesta

    # --- COMANDO DESCONOCIDO ---
    else:
        return f"❓ Comando '{mensaje_recibido}' no reconocido. Usa *.menu* para ver la lista."