import serial
import time
import configRX  # Importar el archivo de configuración

# Constantes de configuración
DELAY_BETWEEN_CHECKS = 1  # Retardo entre consultas de recepción (en segundos)

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
    """Procesa un evento de recepción y extrae el mensaje en texto."""
    try:
        # Buscar eventos +EVT:RXP2P en la respuesta
        if "+EVT:RXP2P" in response:
            parts = response.split(":")
            if len(parts) >= 4:
                hex_data = parts[-1].strip()  # Extraer la parte hexadecimal
                print(f"Datos codificados (hexadecimal): {hex_data}")  # Imprimir hexadecimal
                
                # Convertir el dato hexadecimal a texto
                text = bytes.fromhex(hex_data).decode('utf-8', errors='replace')
                print(f"Datos decodificados (texto): {text}")  # Imprimir texto decodificado
                return text
        return "Evento no reconocido o sin datos."
    except ValueError:
        return f"Datos no válidos para conversión: {response}"
    except Exception as e:
        return f"Error procesando evento: {e}"

def configure_p2p_mode(port, baudrate):
    """Configura el módulo en modo P2P."""
    print("Configurando módulo como receptor P2P...")
    send_at_command("AT+NWM=0", port, baudrate)  # Cambiar a modo P2P
    send_at_command("AT+P2P=915000000,7,125,1,14,8", port, baudrate)  # Configuración P2P

def start_reception(port, baudrate):
    """Inicia la recepción continua de mensajes."""
    print("Esperando mensajes del transmisor...")
    send_at_command("AT+PRECV=65534", port, baudrate)  # Activar recepción continua

def main():
    """Función principal para recibir y procesar mensajes."""
    configure_p2p_mode(configRX.PORT, configRX.BAUDRATE)
    start_reception(configRX.PORT, configRX.BAUDRATE)

    try:
        while True:
            # Leer datos recibidos
            response = send_at_command("AT+RECV=?", configRX.PORT, configRX.BAUDRATE)
            
            # Procesar y mostrar el dato si es un evento válido
            if "+EVT:RXP2P" in response:
                process_rx_event(response)  # Proceso incluye impresión
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