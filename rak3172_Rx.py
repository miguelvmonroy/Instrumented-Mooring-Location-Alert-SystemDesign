import serial
import time
import sys
import codecs

# Forzar la codificación UTF-8
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

# Configuración del puerto y velocidad
PORT = '/dev/ttyUSB0'  # Cambia según tu puerto detectado
BAUDRATE = 115200      # Velocidad predeterminada del módulo

def send_at_command(command):
    """Envía un comando AT al módulo y devuelve la respuesta."""
    try:
        with serial.Serial(PORT, BAUDRATE, timeout=5) as ser:
            ser.reset_input_buffer()   # Limpia el buffer de entrada
            ser.reset_output_buffer()  # Limpia el buffer de salida
            print(f"Enviando comando: {command}")
            ser.write((command + '\r\n').encode())  # Enviar comando
            time.sleep(3)  # Aumenta el tiempo de espera para la respuesta
            response = ser.read_all().decode(errors='ignore')  # Leer respuesta
            print(f"Respuesta recibida: {response}")  # Depuración adicional
            return response.strip() or "Sin respuesta"
    except serial.SerialException as e:
        return f"Error de conexión: {e}"
    except Exception as e:
        return f"Error: {e}"

def is_module_ready(max_retries=5):
    """Verifica si el módulo está listo para recibir un nuevo comando."""
    retries = 0
    while retries < max_retries:
        response = send_at_command("AT")
        if "OK" in response:
            return True
        print(f"Intento {retries + 1}: El módulo está ocupado. Esperando a que esté listo...")
        time.sleep(2)  # Espera antes de reintentar
        retries += 1
    return False

def stop_continuous_reception():
    """Detiene el modo de recepción continua si está activado."""
    response = send_at_command("AT+PRECV=0")
    if "OK" in response:
        print("Modo de recepción continua detenido.")
    else:
        print("No se pudo detener el modo de recepción continua.")

def start_continuous_reception():
    """Inicia el modo de recepción continua."""
    response = send_at_command("AT+PRECV=65535")
    if "OK" in response:
        print("Modo de recepción continua iniciado.")
    elif "P2P_RX_ON already" in response:
        print("El módulo ya está en modo de recepción continua.")
    else:
        print(f"Error al iniciar el modo de recepción continua: {response}")

if __name__ == "__main__":
    print("Configurando módulo como receptor P2P...")

    # Detener recepción continua si ya está activada
    stop_continuous_reception()

    # Configurar el módulo en modo P2P
    if "OK" not in send_at_command("AT+NWM=0"):
        print("Error al configurar el modo P2P.")
        exit()

    response_p2p = send_at_command("AT+P2P=915000000,7,125,1,14,8")
    if "OK" not in response_p2p:
        print(f"Error al configurar los parámetros P2P: {response_p2p}")
        exit()

    print("Esperando mensaje del transmisor...")

    # Iniciar el modo de recepción continua
    start_continuous_reception()

    try:
        while True:
            # Verificar si el módulo está listo
            if not is_module_ready():
                print("El módulo no está listo. Intentando nuevamente...")
                time.sleep(2)
                continue

            # Leer datos recibidos
            response = send_at_command("")
            if "RX " in response:
                print(f"Mensaje recibido en hexadecimal: {response.split(' ')[1]}")
            elif "AT_BUSY_ERROR" in response:
                print("El módulo está ocupado. Esperando a que esté listo...")
                time.sleep(2)
                continue

            time.sleep(1)  # Retardo para evitar saturación

    except KeyboardInterrupt:
        print("Interrupción manual detectada. Saliendo...")
    finally:
        # Detener el modo de recepción continua al finalizar
        stop_continuous_reception()
        print("Operación completada.")