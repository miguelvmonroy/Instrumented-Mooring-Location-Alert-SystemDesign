import serial
import time
import configRX  # Importar el archivo de configuración

# Constantes de configuración
DELAY_BETWEEN_CHECKS = 1  # Retardo entre ciclos (en segundos)
LISTEN_TIMEOUT = 2000     # Tiempo de espera para recepción (en ms)
RESPONSE_MESSAGE = "61636b"  # "ack" en hexadecimal (respuesta automática)

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

def process_rx_event(response):
    """Procesa un evento de recepción y envía ACK automático."""
    try:
        if "+EVT:RXP2P" in response:
            parts = response.split(":")
            if len(parts) >= 4:
                hex_data = parts[-1].strip()  # Extraer la parte hexadecimal
                text = bytes.fromhex(hex_data).decode('utf-8', errors='replace')
                print(f"Mensaje recibido: {text}")

                # Enviar ACK automático
                print("Enviando ACK...")
                ack_response = send_at_command(f"AT+PSEND={RESPONSE_MESSAGE}", configRX.PORT, configRX.BAUDRATE)
                print(f"Respuesta ACK: {ack_response}")
                return True
        return False
    except Exception as e:
        print(f"Error procesando evento: {e}")
        return False

def configure_p2p_mode():
    """Configura el módulo en modo P2P."""
    print("Configurando módulo como receptor P2P...")
    send_at_command("AT+NWM=0", configRX.PORT, configRX.BAUDRATE)  # Cambiar a modo P2P
    send_at_command("AT+P2P=915000000,7,125,1,8,14", configRX.PORT, configRX.BAUDRATE)  # Parámetros ajustados

def start_reception():
    """Inicia la recepción continua de mensajes."""
    print("Activando recepción continua...")
    send_at_command("AT+PRECV=65534", configRX.PORT, configRX.BAUDRATE)  # Activar recepción continua

def main():
    """Función principal para recibir y procesar mensajes."""
    configure_p2p_mode()
    start_reception()

    print("Modo receptor activado. Esperando mensajes...")
    print("Presiona Ctrl+C para salir.")

    try:
        while True:
            # Leer datos recibidos
            response = send_at_command("AT+RECV=?", configRX.PORT, configRX.BAUDRATE)
            
            # Procesar y mostrar el dato si es un evento válido
            if "+EVT:RXP2P" in response:
                process_rx_event(response)  # Procesa el mensaje y envía ACK
            else:
                print(f"Respuesta inesperada: {response}")
            
            time.sleep(DELAY_BETWEEN_CHECKS)  # Espera antes de la próxima consulta

    except KeyboardInterrupt:
        print("Interrupción manual detectada. Saliendo...")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        print("Operación completada.")

if __name__ == "__main__":
    main()