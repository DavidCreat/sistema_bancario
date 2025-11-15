
import unittest
from sistema_bancario import CuentaAhorro, CuentaCorriente, CuentaInversion, procesar_transacciones, realizar_transferencia

class TestSistemaBancario(unittest.TestCase):

    def setUp(self):
        """Configuración inicial para las pruebas."""
        self.cuenta_ahorro = CuentaAhorro("Ahorro-001", "David fonseca", 1000000, 0.02)
        self.cuenta_corriente = CuentaCorriente("Corriente-002", "Maryam perez", 50000, 100000, 1000)
        self.cuenta_inversion = CuentaInversion("Inversion-003", "David fonseca", 5000000, 0.09)

    def test_deposito_ahorro(self):
        self.cuenta_ahorro.depositar(50000)
        self.assertEqual(self.cuenta_ahorro.consultar_saldo(), 1050000)

    def test_retiro_ahorro_exitoso(self):
        self.cuenta_ahorro.retirar(200000)
        self.assertEqual(self.cuenta_ahorro.consultar_saldo(), 800000)

    def test_retiro_ahorro_fallido(self):
        with self.assertRaises(ValueError):
            self.cuenta_ahorro.retirar(2000000)

    def test_aplicar_interes(self):
        self.cuenta_ahorro.aplicar_interes()
        self.assertEqual(self.cuenta_ahorro.consultar_saldo(), 1020000)

    def test_deposito_corriente(self):
        self.cuenta_corriente.depositar(20000)
        self.assertEqual(self.cuenta_corriente.consultar_saldo(), 70000)

    def test_retiro_corriente_con_sobregiro(self):
        self.cuenta_corriente.retirar(100000)
        self.assertEqual(self.cuenta_corriente.consultar_saldo(), -51000)

    def test_aplicar_rendimiento_inversion(self):
        self.cuenta_inversion.aplicar_rendimiento()
        self.assertEqual(self.cuenta_inversion.consultar_saldo(), 5450000)

    def test_transferencia_exitosa_sin_comision(self):
        """Prueba que una transferencia desde una C. Corriente no aplique comisión."""
        origen = CuentaCorriente("Origen-CC", "Test", 10000, 5000, 500)
        destino = CuentaAhorro("Destino-CA", "Test", 5000, 0.01)
        
        realizar_transferencia(origen, destino, 3000)
        
        self.assertEqual(origen.consultar_saldo(), 7000) # Sin comisión
        self.assertEqual(destino.consultar_saldo(), 8000)

    def test_transferencia_fallida_fondos_insuficientes(self):
        origen = CuentaAhorro("Origen", "Test", 1000, 0.01)
        destino = CuentaCorriente("Destino", "Test", 5000, 1000, 100)
        resultado = realizar_transferencia(origen, destino, 2000)
        self.assertFalse(resultado)
        self.assertEqual(origen.consultar_saldo(), 1000)
        self.assertEqual(destino.consultar_saldo(), 5000)

    def test_comparacion_cuentas(self):
        self.assertTrue(self.cuenta_inversion > self.cuenta_ahorro)
        self.assertTrue(self.cuenta_ahorro > self.cuenta_corriente)
        
    def test_operadores_sobrecargados(self):
        cuenta = CuentaAhorro("Op-Test", "Operador", 50000, 0.01)
        cuenta += 10000
        self.assertEqual(cuenta.consultar_saldo(), 60000)
        cuenta -= 5000
        self.assertEqual(cuenta.consultar_saldo(), 55000)
        with self.assertRaises(ValueError):
            cuenta -= 100000

    def test_polimorfismo(self):
        cuentas = [
            CuentaAhorro("Ahorro-Pol", "Test", 100000, 0.02),
            CuentaCorriente("Cor-Pol", "Test", 50000, 20000, 500),
            CuentaInversion("Inv-Pol", "Test", 200000, 0.05)
        ]
        procesar_transacciones(cuentas)
        self.assertEqual(cuentas[0].consultar_saldo(), 100500)
        self.assertEqual(cuentas[1].consultar_saldo(), 50000)
        self.assertEqual(cuentas[2].consultar_saldo(), 200500)

if __name__ == '__main__':
    print("Generando transacciones para el archivo de log...")
    cuenta_a = CuentaAhorro("Log-Ahorro-001", "Log User", 500000, 0.02)
    cuenta_c = CuentaCorriente("Log-Corriente-002", "Log User", 20000, 10000, 500)
    cuenta_i = CuentaInversion("Log-Inversion-003", "Log User", 100000, 0.05)

    realizar_transferencia(cuenta_a, cuenta_c, 5000)
    cuenta_i += 20000
    cuenta_a -= 2000
    cuenta_c -= 3000
    cuenta_i.aplicar_rendimiento()
    try:
        cuenta_c -= 25000
    except ValueError as e:
        print(f"Log: Se intentó un retiro con sobregiro y fue manejado ({e}).")
    cuenta_a += 4000
    realizar_transferencia(cuenta_i, cuenta_a, 10000)
    print("Archivo 'transacciones.log' actualizado.")

    print("\n" + "="*40)
    print("Estado de Cuentas (Salida de Ejemplo)")
    print("="*40)
    
    cuenta_ahorro_demo = CuentaAhorro("CuentaAhorro-001", "David fonseca", 1000000, 0.02)
    cuenta_ahorro_demo.aplicar_interes()
    
    cuenta_corriente_demo = CuentaCorriente("CuentaCorriente-002", "Maryam perez", 100000, 200000, 1000)
    try:
        cuenta_corriente_demo -= 149000
    except ValueError as e:
        print(f"Error en la simulación: {e}")

    cuenta_inversion_demo = CuentaInversion("CuentaInversion-003", "David fonseca", 5023041.47, 0.085)
    cuenta_inversion_demo.aplicar_rendimiento()

    print(cuenta_ahorro_demo)
    print(cuenta_corriente_demo)
    print(cuenta_inversion_demo)
    print("="*40)
