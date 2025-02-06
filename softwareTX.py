import serial
import time
import keyboard  # Biblioteca para detectar teclas presionadas
import configTX  # Importar el archivo de configuración

#####################################################################
# Función para manejar retardos en milisegundos
def delay_ms(milliseconds):
    """Retardo en milisegundos."""
    time.sleep(milliseconds / 1000.0)

# Configuración del retardo
DELAY_BEFORE = 1000  # Retardo antes del mensaje (en ms)
DELAY_BETWEEN = 500  # Retardo entre cada envío (en ms)

# Mensaje a enviar (en hexadecimal)
MESSAGE = "17726674746566"

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
    send_at_command("AT+P2P=915000000,7,0,1,8,14", port, baudrate)  # Parámetros ajustados

def main():
    """Función principal para enviar mensajes en un bucle continuo."""
    print(f"Esperando {DELAY_BEFORE} ms antes de iniciar el envío...")
    delay_ms(DELAY_BEFORE)

    configure_p2p_mode(configTX.PORT, configTX.BAUDRATE)

    print("Presiona 'q' en cualquier momento para salir del ciclo de envío.")

    try:
        i = 1
        while True:
            if keyboard.is_pressed('q'):  # Verificar si se presiona la tecla 'q'
                print("Deteniendo el envío de mensajes...")
                break

            print(f"Envío {i}: Enviando mensaje: {MESSAGE}")
            response = send_at_command(f"AT+PSEND={MESSAGE}", configTX.PORT, configTX.BAUDRATE)
            print(f"Respuesta al envío {i}: {response}")

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