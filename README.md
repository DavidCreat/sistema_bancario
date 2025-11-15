
# Sistema Bancario para el Taller de Herencia y Polimorfismo

Este es el proyecto para el taller. Es un sistema de banco que hice en Python para manejar tres tipos de cuentas diferentes.

## ¿Cómo está hecho? (Características Técnicas)

Aquí explico las partes más importantes y cómo las implementé:

*   **Herencia y Clases Abstractas:**
    Creé una clase "molde" llamada `CuentaBancaria` que es una **clase abstracta** (`ABC`). Esta obliga a que cualquier tipo de cuenta que herede de ella tenga sí o sí los métodos `depositar` y `retirar`.
    Las clases `CuentaAhorro`, `CuentaCorriente` y `CuentaInversion` **heredan** de `CuentaBancaria` y usan `super()` para llamar al constructor padre.

*   **Polimorfismo en Acción:**
    La función `procesar_transacciones` es el mejor ejemplo de esto. Recibe una lista que puede tener mezcladas cuentas de ahorro, corrientes y de inversión, y opera con ellas sin problemas usando el mismo código `cuenta.depositar()`, demostrando el polimorfismo.

*   **Sobrecarga de Operadores:**
    Para que el código fuera más intuitivo, sobrecargué varios operadores:
    *   `cuenta + 500`: Funciona como un depósito.
    *   `cuenta - 200`: Funciona como un retiro.
    *   `cuenta_a > cuenta_b`: Compara cuál de las dos cuentas tiene más saldo.
    *   `print(cuenta)`: Muestra el estado de la cuenta en un formato legible.

*   **Manejo de Errores y Transacciones Seguras:**
    El sistema no se rompe si intentas sacar más dinero del que tienes. Lanza una excepción `ValueError` que se maneja correctamente. Además, la función `realizar_transferencia` es segura: si el retiro funciona pero el depósito falla, la operación se revierte para no perder dinero.

*   **Log de Auditoría:**
    Cada operación importante (crear cuenta, depositar, retirar, transferir, etc.) queda registrada con fecha y hora en el archivo `transacciones.log`.

## Los Archivos del Proyecto

*   `sistema_bancario.py`: Aquí está todo el código principal, con la definición de las clases.
*   `test_sistema.py`: Este archivo tiene dos funciones:
    1.  Contiene las **pruebas unitarias** para validar que todo funcione.
    2.  Si se ejecuta directamente, genera la **salida final** que pide el taller.
*   `transacciones.log`: El archivo donde se guardan todos los movimientos.

## Comandos Clave

Para revisar el proyecto:

### 1. Para generar la salida final del taller:
Este comando ejecuta el script que prepara y muestra el "Estado de Cuentas" como lo pide el enunciado.

```bash
python test_sistema.py
```

### 2. Para correr todas las pruebas y ver que todo está OK:
Este es el comando estándar para ejecutar las 12 pruebas unitarias y asegurarse de que no hay errores en la lógica.

```bash
python -m unittest test_sistema.py
```

### 3. Para ver el resultado de cada prueba, una por una:
reporte detallado de qué hace cada prueba y ver que todas pasan individualmente, usa el modo "verbose".

```bash
python -m unittest -v test_sistema.py
```

## Evidencias

<img width="679" height="198" alt="image" src="https://github.com/user-attachments/assets/cacae1f5-7304-4975-aa39-970a0fbf180f" />
<img width="704" height="254" alt="image" src="https://github.com/user-attachments/assets/cc348bf6-7314-46d8-8757-047c0fffbec3" />
<img width="911" height="341" alt="image" src="https://github.com/user-attachments/assets/cf1fba27-8a23-4c2d-87e0-4ea94b898bca" />


