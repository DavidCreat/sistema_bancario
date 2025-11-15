
from abc import ABC, abstractmethod
import logging
from datetime import datetime

# Configura el log para que guarde todo en un archivo.
logging.basicConfig(filename='transacciones.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def realizar_transferencia(origen, destino, cantidad):
    """
    Realiza una transferencia segura entre dos cuentas.
    Si el débito inicial falla, la operación se detiene inmediatamente.
    """
    try:
        # Intenta sacar la plata de la cuenta origen.
        origen._transferir(cantidad)
    except ValueError as e:
        # Si no se pudo (ej. no hay fondos), se cancela todo.
        logging.error(f"Transferencia fallida: Débito desde {origen.numero_cuenta} falló. Razón: {e}")
        return False

    # Si lo de arriba funcionó, ahora intenta depositar.
    try:
        destino.depositar(cantidad)
    except ValueError as e:
        # Si el depósito falla, hay que devolver la plata a la cuenta origen.
        logging.error(f"Transferencia fallida: Crédito a {destino.numero_cuenta} falló. Razón: {e}. Revirtiendo débito.")
        origen.depositar(cantidad) # Reversión
        return False
        
    logging.info(f"Transferencia exitosa de ${cantidad:,.2f} desde {origen.numero_cuenta} hacia {destino.numero_cuenta}")
    return True

# --- Clase Base Abstracta ---
# Es el "molde" para todas las demás cuentas.
class CuentaBancaria(ABC):
    def __init__(self, numero_cuenta, titular, saldo):
        self.numero_cuenta = numero_cuenta
        self.titular = titular
        self.saldo = saldo
        logging.info(f"Cuenta creada: {self.numero_cuenta}")

    # Obliga a que las clases hijas tengan su propia versión de depositar.
    @abstractmethod
    def depositar(self, cantidad):
        pass

    # Obliga a que las clases hijas tengan su propia versión de retirar.
    @abstractmethod
    def retirar(self, cantidad):
        pass
        
    # Saca plata sin aplicar comisiones (para transferencias).
    def _transferir(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad a transferir debe ser positiva.")
        if self.saldo < cantidad:
            raise ValueError("Fondos insuficientes para transferir.")
        self.saldo -= cantidad

    def consultar_saldo(self):
        return self.saldo

    # Define cómo se ve la cuenta al hacer print().
    def __str__(self):
        return f"{self.numero_cuenta}: Saldo: ${self.saldo:,.2f}"

    # Para poder comparar cuentas con el operador >
    def __gt__(self, other):
        return self.saldo > other.saldo
        
    # Para poder usar el operador + para depositar.
    def __add__(self, cantidad):
        self.depositar(cantidad)
        return self

    # Para poder usar el operador - para retirar.
    def __sub__(self, cantidad):
        self.retirar(cantidad)
        return self

# --- Tipos de Cuentas Específicas ---

class CuentaAhorro(CuentaBancaria):
    def __init__(self, numero_cuenta, titular, saldo, tasa_interes):
        super().__init__(numero_cuenta, titular, saldo)
        self.tasa_interes = tasa_interes

    # Personaliza el print() para la cuenta de ahorro.
    def __str__(self):
        return f"{super().__str__()} (Interés: {self.tasa_interes:.1%})"

    def depositar(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad a depositar debe ser positiva.")
        self.saldo += cantidad
        logging.info(f"Depósito en {self.numero_cuenta}: ${cantidad:,.2f}")

    def retirar(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad a retirar debe ser positiva.")
        if self.saldo >= cantidad:
            self.saldo -= cantidad
            logging.info(f"Retiro de {self.numero_cuenta}: ${cantidad:,.2f}")
        else:
            raise ValueError("Fondos insuficientes.")

    # Calcula y añade el interés al saldo.
    def aplicar_interes(self):
        interes = self.saldo * self.tasa_interes
        self.saldo += interes
        logging.info(f"Interés aplicado en {self.numero_cuenta}: ${interes:,.2f}")

class CuentaCorriente(CuentaBancaria):
    def __init__(self, numero_cuenta, titular, saldo, limite_sobregiro, comision_transaccion):
        super().__init__(numero_cuenta, titular, saldo)
        self.limite_sobregiro = limite_sobregiro
        self.comision_transaccion = comision_transaccion

    # Añade "(Sobregiro usado)" al print() si el saldo es negativo.
    def __str__(self):
        estado_sobregiro = " (Sobregiro usado)" if self.saldo < 0 else ""
        return f"{super().__str__()}{estado_sobregiro}"

    def depositar(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad a depositar debe ser positiva.")
        self.saldo += cantidad
        logging.info(f"Depósito en {self.numero_cuenta}: ${cantidad:,.2f}")

    # Al retirar, cobra una comisión.
    def retirar(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad a retirar debe ser positiva.")
        costo_total = cantidad + self.comision_transaccion
        if self.saldo + self.limite_sobregiro >= costo_total:
            self.saldo -= costo_total
            logging.info(f"Retiro de {self.numero_cuenta}: ${cantidad:,.2f} (Comisión: ${self.comision_transaccion:,.2f})")
        else:
            raise ValueError("Límite de sobregiro excedido.")

    # Permite transferir usando el sobregiro.
    def _transferir(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad a transferir debe ser positiva.")
        if self.saldo + self.limite_sobregiro < cantidad:
            raise ValueError("Fondos insuficientes (incluyendo sobregiro) para transferir.")
        self.saldo -= cantidad

class CuentaInversion(CuentaBancaria):
    def __init__(self, numero_cuenta, titular, saldo, tasa_rendimiento):
        super().__init__(numero_cuenta, titular, saldo)
        self.tasa_rendimiento = tasa_rendimiento

    # Personaliza el print() para la cuenta de inversión.
    def __str__(self):
        return f"{super().__str__()} (Rendimiento: {self.tasa_rendimiento:.1%})"

    def depositar(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad a depositar debe ser positiva.")
        self.saldo += cantidad
        logging.info(f"Depósito (inversión) en {self.numero_cuenta}: ${cantidad:,.2f}")

    def retirar(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad a retirar debe ser positiva.")
        if self.saldo >= cantidad:
            self.saldo -= cantidad
            logging.info(f"Retiro (desinversión) de {self.numero_cuenta}: ${cantidad:,.2f}")
        else:
            raise ValueError("Fondos insuficientes para desinvertir.")

    # Calcula y añade el rendimiento al saldo.
    def aplicar_rendimiento(self):
        rendimiento = self.saldo * self.tasa_rendimiento
        self.saldo += rendimiento
        logging.info(f"Rendimiento aplicado en {self.numero_cuenta}: ${rendimiento:,.2f}")

# Una función polimórfica para procesar una lista de cuentas mixtas.
def procesar_transacciones(cuentas):
    for cuenta in cuentas:
        print(f"Procesando cuenta: {cuenta.numero_cuenta}")
        cuenta.depositar(1000)
        try:
            cuenta.retirar(500)
        except ValueError as e:
            print(f"Error al retirar: {e}")
        print(f"Saldo final: {cuenta.consultar_saldo()}")
        print("-" * 20)
