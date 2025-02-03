import serial
import time
import configTX  # Importar el archivo de configuración

#####################################################################
# Función para manejar retardos en milisegundos
def delay_ms(milliseconds):
    """Retardo en milisegundos."""
    time.sleep(milliseconds / 1000.0)

# Configuración del retardo
DELAY_BEFORE = 1000  # Retardo antes del mensaje (en ms)
DELAY_BETWEEN = 500  # Retardo entre cada envío (en ms)
LISTEN_TIMEOUT = 2000  # Tiempo de espera para recibir mensajes (en ms)

# Mensaje a enviar (en hexadecimal)
MESSAGE = "6772657474656c"  # "grettel" en hexadecimal

#####################################################################

def send_at_command(command, port, baudrate, timeout=5):
    """Envía un comando AT al módulo y devuelve la respuesta."""
    try:
        with serial.Serial(port, baudrate, timeout=timeout) as ser:
            ser.reset_input_buffer()  # Limpia el buffer de entrada
            ser.reset_output_buffer()  # Limpia el buffer de salida
            print(f"Enviando comando: {command}")
            ser.write((command + '\r\n').encode())  # Enviar comando
            time.sleep(1)  # Espera respuesta
            response = ser.read_all().decode(errors='ignore')  # Leer respuesta
            return response.strip() or "Sin respuesta"
    except serial.SerialException as e:
        return f"Error de conexión: {e}"
    except Exception as e:
        return f"Error: {e}"

def configure_p2p_mode(port, baudrate):
    """Configura el módulo en modo P2P."""
    print("Configurando módulo como transmisor P2P...")
    send_at_command("AT+NWM=0", port, baudrate)  # Cambiar a modo P2P
    send_at_command("AT+P2P=915000000,7,125,1,8,14", port, baudrate)  # Parámetros ajustados

def listen_for_messages(port, baudrate, timeout):
    """Escucha mensajes entrantes durante un tiempo determinado."""
    try:
        with serial.Serial(port, baudrate, timeout=1) as ser:
            start_time = time.time()
            while (time.time() - start_time) * 1000 < timeout:
                if ser.in_waiting > 0:
                    message = ser.read_all().decode(errors='ignore')
                    print(f"Datos crudos recibidos: {message}")  # Debug
                    if "+EVT:RXP2P" in message:
                        return process_received_message(message)
            print("No se recibieron mensajes en el tiempo de espera.")
            return None
    except Exception as e:
        print(f"Error escuchando: {e}")
        return None

def process_received_message(message):
    """Procesa mensajes recibidos."""
    if "61636b" in message:  # Busca 'ack' en hexadecimal
        print("¡ACK recibido!")
        return True
    else:
        print(f"Mensaje no reconocido: {message}")
        return False

def main():
    """Función principal para enviar y recibir mensajes en un bucle continuo."""
    print(f"Esperando {DELAY_BEFORE} ms antes de iniciar el envío...")
    delay_ms(DELAY_BEFORE)

    configure_p2p_mode(configTX.PORT, configTX.BAUDRATE)

    print("Presiona Ctrl+C para salir del ciclo de envío/recepción.")

    try:
        i = 1
        while True:
            # Enviar mensaje
            print(f"Envío {i}: Enviando mensaje: {MESSAGE}")
            response = send_at_command(f"AT+PSEND={MESSAGE}", configTX.PORT, configTX.BAUDRATE)
            print(f"Respuesta al envío {i}: {response}")

            # Esperar un momento antes de escuchar
            delay_ms(500)

            # Escuchar mensajes
            print(f"Escuchando mensajes durante {LISTEN_TIMEOUT} ms...")
            received_message = listen_for_messages(configTX.PORT, configTX.BAUDRATE, LISTEN_TIMEOUT)
            if received_message:
                print("Mensaje recibido y procesado correctamente.")

            print(f"Esperando {DELAY_BETWEEN} ms antes del próximo envío...")
            delay_ms(DELAY_BETWEEN)
            i += 1  # Incrementar contador

    except KeyboardInterrupt:
        print("Interrupción manual detectada. Saliendo...")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        print("Operación completada.")

if __name__ == "__main__":
    main()