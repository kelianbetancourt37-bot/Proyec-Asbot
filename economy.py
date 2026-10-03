import random
import time

def procesar_trabajar(usuario_id, monedas_actuales, ultimo_trabajo):
    tiempo_actual = time.time()
    tiempo_espera = 300  # 5 minutos exactos de cooldown
    
    if ultimo_trabajo > 0:
        tiempo_transcurrido = tiempo_actual - ultimo_trabajo
        if tiempo_transcurrido < tiempo_espera:
            tiempo_restante = int(tiempo_espera - tiempo_transcurrido)
            minutos = tiempo_restante // 60
            segundos = tiempo_restante % 60
            return monedas_actuales, ultimo_trabajo, f"⏳ Estás cansado. Debes esperar *{minutos} min y {segundos} seg* para volver a trabajar."

    ganancia = random.randint(10, 50)
    total = monedas_actuales + ganancia
    mensaje = f"👷‍♂️ ¡Trabajaste duro y ganaste {ganancia} monedas! Total: {total}"
    return total, tiempo_actual, mensaje

def procesar_apostar(usuario_id, monedas_mano, ultimo_t):
    ahora = time.time()
    cooldwn = 600 # 10 minutos en segundos

    if ahora - ultimo_t < cooldwn:
        restante = int(cooldwn - (ahora - ultimo_t))
        mins, segs = divmod(restante, 60)
        return monedas_mano, ultimo_t, f"Espera {mins} minutos {segs} segundos para poder apostar"

    if random.choice([True, False]):
        ganancia = random.randint(100, 300)
        nuevo_total = monedas_mano + ganancia
        mensaje = f"Apostaste y ganaste {ganancia} monedas"
    else:
        multa = random.randint(100, 300)
        nuevo_total = max(0, monedas_mano - multa)
        mensaje = f"Perdiste {multa} monedas"

    return nuevo_total, ahora, mensaje

def procesar_crimen(usuario_id, monedas_mano, ultimo_t):
    ahora = time.time()
    cooldwn = 600 # 10 minutos en segundos

    if ahora - ultimo_t < cooldwn:
        restante = int(cooldwn - (ahora - ultimo_t))
        mins, segs = divmod(restante, 60)
        return monedas_mano, ultimo_t, f"Espera {mins} minutos {segs} segundos para poder criminalizar"

    if random.choice([True, False]):
        multa = random.randint(100, 300)
        nuevo_total = max(0, monedas_mano - multa)
        mensaje = f"Te atraparon con las manos en la masa y perdiste {multa} monedas"
    else:
        ganancia = random.randint(100, 300)
        nuevo_total = monedas_mano + ganancia
        mensaje = f"Le robaste a Jasper y ganaste {ganancia} monedas"

    return nuevo_total, ahora, mensaje

def procesar_daily(usuario_id, monedas, ultimo_t):
    ahora = time.time()
    cooldwn = 864000 # 24 horas en segundos

    if ahora - ultimo_t < cooldwn:
        restante = int(cooldwn - (ahora - ultimo_t))
        mins, segs = divmod(restante, 60)
        return monedas, ultimo_t, f"Espera {mins} minutos {segs} segundos para poder hacer un diario"

    ganancia = random.randint(100, 300)
    nueva_total = monedas + ganancia
    mensaje = f"Haciste un diario y ganaste {ganancia} monedas"

    return nueva_total, ahora, mensaje

def procesar_depositar(usuario_id, efectivo, banco, monto):
    if efectivo <monto:
        return efectivo, banco, f"No tienes suficiente efectivo en mano."

    nuevo_efectivo = efectivo - monto
    nuevo_banco = banco + monto
    mensaje = f"Depositaste ${monto}. Efectivo: ${nuevo_efectivo} | Banco: ${nuevo_banco}"
    return nuevo_efectivo, nuevo_banco, mensaje

def procesar_retirar(usuario_id, efectivo, banco, monto):
    if banco < monto:
        return efectivo, banco, f"No tienes suficiente dinero en el banco."

    nuevo_efectivo = efectivo + monto
    nuevo_banco = banco - monto
    mensaje = f"Retiraste ${monto}. Efectivo: ${nuevo_efectivo} | Banco: ${nuevo_banco}"
    return nuevo_efectivo, nuevo_banco, mensaje

def procesar_cofre(usuario_id, monedas, ultimo_t):
    ahora = time.time()
    cooldwn = 1500 # 15 minutos en segundos

    if random.choice([True, False]):
        ganancia = random.randint(100, 300)
        nuevo_total = monedas + ganancia
        mensaje = f"Cofreaste y ganaste {ganancia} monedas"
    else:
        multa = random.randint(100, 300)
        nuevo_total = max(0, monedas - multa)
        mensaje = f"Perdiste {multa} monedas"

    return nuevo_total, ahora, mensaje

def procesar_banco(monedas_mano, monedas_banco):
    if monedas_banco > 0:
        mensaje = (
                    f"🏦 *ESTADO DE TU CUENTA BANCARIA*\n\n"
                    f"💵 ´Dinero en mano:´ *0* monedas\n"
                    f"💰 ´Dinero en el banco:´ *0* monedas\n"
                    f"⚠️ *Tu cuenta bancaria está vacía.* Usa `.depositar [cantidad]` para guardar dinero."
                )
    else:
        mensaje = (
            f"🏦 *ESTADO DE TU CUENTA BANCARIA*\n\n"
            f"💵 ´Dinero en mano:´ *0* monedas\n"
            f"💰 ´Dinero en el banco:´ *0* monedas\n"
            f"⚠️ *Tu cuenta bancaria está vacía.* Usa `.depositar [cantidad]` para guardar dinero."
        )
    return monedas_mano, monedas_banco, mensaje