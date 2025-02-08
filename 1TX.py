import serial
import time
import keyboard  # Biblioteca para detectar teclas presionadas

#####################################################################
# Función para manejar retardos en milisegundos
def delay_ms(milliseconds):
    time.sleep(milliseconds / 1000.0)

# Configuración del retardo
delay_before = 1000  # Retardo antes del mensaje (ms)
delay_between = 500  # Retardo entre cada envío (ms)

# Mensaje a enviar (en hexadecimal)
message = "486f6c61206d756e6410"

# Configuración del puerto serie
PORT = 'COM8'  # Ajusta el puerto según corresponda
BAUDRATE = 115200  # Velocidad del módulo

def send_at_command(ser, command, timeout=2):
    """Envía un comando AT y devuelve la respuesta."""
    try:
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        print(f"Enviando comando: {command}")
        ser.write((command + '\r\n').encode())  # Enviar comando
        time.sleep(0.1)  # Pequeña pausa
        response = ser.read_until().decode(errors='ignore').strip()  # Leer respuesta
        print(f"Respuesta: {response}")
        return response
    except Exception as e:
        return f"Error: {e}"

def configurar_modulo(ser):
    """Configura el módulo LoRa en modo P2P."""
    print("Configurando módulo como transmisor P2P...")

    if "OK" not in send_at_command(ser, "AT+NWM=0"):
        print("Error al configurar el modo P2P")
        return False

    # Verificar la versión del firmware
    version = send_at_command(ser, "AT+VER=?")
    print(f"Versión del firmware: {version}")

    # Verificar si AT+P2P está disponible
    respuesta_p2p = send_at_command(ser, "AT+P2P=?")
    if "AT_COMMAND_NOT_FOUND" in respuesta_p2p or "AT_PARAM_ERROR" in respuesta_p2p:
        print("El comando AT+P2P no está disponible en este firmware. Actualiza el módulo.")
        return False

    # Intentar configurar P2P con diferentes formatos
    configuraciones_p2p = [
        "AT+P2P=915000000:7:0:0:8:14",
        "AT+P2P=915000000:7:125:0:8:14",
        "AT+P2P=915000000:7:0:1:8:14",
        "AT+P2P=915000000:7:125:1:8:14"
    ]

    for config in configuraciones_p2p:
        response = send_at_command(ser, config)
        if "OK" in response:
            print(f"Configuración P2P establecida: {config}")
            break
    else:
        print("No se pudo configurar P2P. Verifica los parámetros o el firmware.")
        return False

    if "OK" not in send_at_command(ser, "AT+PRECV=0"):
        print("Error al desactivar la recepción")
        return False

    print("Módulo configurado correctamente.")
    return True

def enviar_mensajes(ser):
    """Envía mensajes en un bucle continuo hasta que se presione 'q'."""
    print("Presiona 'q' en cualquier momento para salir del ciclo de envío.")

    i = 1
    try:
        while True:
            if keyboard.is_pressed('q'):
                print("Deteniendo el envío de mensajes...")
                break

            print(f"Envío {i}: {message}")
            response = send_at_command(ser, f"AT+PSEND={message}")
            
            if "OK" not in response:
                print("Error en el envío del mensaje.")
            
            delay_ms(delay_between)
            i += 1
    except KeyboardInterrupt:
        print("Interrupción manual detectada. Saliendo...")

if __name__ == "__main__":
    print(f"Esperando {delay_before} ms antes de iniciar el envío...")
    delay_ms(delay_before)

    try:
        with serial.Serial(PORT, BAUDRATE, timeout=5) as ser:
            if configurar_modulo(ser):
                enviar_mensajes(ser)
    except serial.SerialException as e:
        print(f"Error al abrir el puerto serie: {e}")
    finally:
        print("Operación completada.")
