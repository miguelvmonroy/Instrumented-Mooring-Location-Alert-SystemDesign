import serial
import time
import keyboard
import configTX

#####################################################################
# Función para manejar retardos en milisegundos
def delay_ms(milliseconds):
    """Retardo en milisegundos."""
    time.sleep(milliseconds / 1000.0)

# Configuración del retardo
DELAY_BEFORE = 1000  # Retardo antes del mensaje (en ms)
DELAY_BETWEEN = 2000  # Ahora espera 2 segundos entre envíos

# Mensaje a enviar
MESSAGE = "17726674746566"
ACK_EXPECTED = "ACK"  # Mensaje esperado de confirmación

#####################################################################

def send_at_command(command, port, baudrate, timeout=2):
    """Envía un comando AT y recibe la respuesta."""
    try:
        with serial.Serial(port, baudrate, timeout=timeout) as ser:
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            print(f"Enviando comando: {command}")
            ser.write((command + '\r\n').encode())
            time.sleep(1)
            response = ser.read_all().decode(errors='ignore').strip()
            return response or "Sin respuesta"
    except Exception as e:
        return f"Error: {e}"

def configure_p2p_mode(port, baudrate):
    """Configura el módulo como P2P transmisor."""
    print("Configurando módulo como transmisor P2P...")
    send_at_command("AT+NWM=0", port, baudrate)
    send_at_command("AT+P2P=915000000,7,0,1,8,14", port, baudrate)

def main():
    """Función principal para enviar mensajes y esperar confirmación."""
    print(f"Esperando {DELAY_BEFORE} ms antes de iniciar el envío...")
    delay_ms(DELAY_BEFORE)

    configure_p2p_mode(configTX.PORT, configTX.BAUDRATE)

    print("Presiona 'q' en cualquier momento para salir.")

    try:
        i = 1
        while True:
            if keyboard.is_pressed('q'):
                print("Deteniendo el envío...")
                break

            print(f"Envío {i}: Enviando mensaje: {MESSAGE}")
            response = send_at_command(f"AT+PSEND={MESSAGE}", configTX.PORT, configTX.BAUDRATE)
            print(f"Respuesta al envío {i}: {response}")

            # Esperar confirmación
            print("Esperando confirmación...")
            ack_response = send_at_command("AT+PRECV=1000", configTX.PORT, configTX.BAUDRATE)

            if ACK_EXPECTED in ack_response:
                print(f"Confirmación recibida: {ack_response}")
            else:
                print("No se recibió confirmación.")

            print(f"Esperando {DELAY_BETWEEN} ms para el próximo envío...")
            delay_ms(DELAY_BETWEEN)
            i += 1

    except KeyboardInterrupt:
        print("Interrupción manual detectada. Saliendo...")
    finally:
        print("Operación completada.")

if __name__ == "__main__":
    main()
