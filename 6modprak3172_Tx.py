import threading
import serial
import time
import keyboard
import configTX  # Asegúrate de definir PORT y BAUDRATE en configTX.py

ACK_EXPECTED = "ACK"
DELAY_BEFORE = 1000  # ms antes de iniciar
DELAY_BETWEEN = 3000  # ms entre envíos
MESSAGE = "17726674746566"

# Variables globales
ser = None
ack_received = False

def send_at_command(command, wait_time=1.5):
    """
    Envía un comando AT al módulo y devuelve la respuesta.
    """
    global ser
    try:
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        print(f"TX: Enviando comando: {command}")
        ser.write((command + "\r\n").encode())
        time.sleep(wait_time)  # Esperar respuesta
        response = ser.read_all().decode(errors='ignore').strip()
        print(f"TX: Respuesta al comando: {response}")
        return response
    except Exception as e:
        print(f"TX: Error al enviar comando {command}: {e}")
        return ""

def receive_continuous():
    """
    Hilo que mantiene el puerto en modo recepción continua y verifica si llega el ACK.
    """
    global ack_received, ser
    try:
        while True:
            if ser.in_waiting:
                data = ser.read_all().decode(errors='ignore').strip()
                print("TX: Datos recibidos:", data)
                if ACK_EXPECTED in data:
                    print("TX: Se detectó ACK en la recepción.")
                    ack_received = True
            time.sleep(0.1)
    except Exception as e:
        print("TX: Error en la recepción continua:", e)

def send_message(message):
    """
    Envía el mensaje y espera la confirmación.
    """
    global ser

    # Desactivar recepción para evitar AT_BUSY_ERROR
    send_at_command("AT+PRECV=0", wait_time=1)

    # Enviar mensaje
    response = send_at_command(f"AT+PSEND={message}", wait_time=2)

    # Verificar si el mensaje se envió correctamente
    if "+EVT:TXP2P DONE" in response:
        print("TX: Mensaje enviado exitosamente.")
    else:
        print("TX: Error al enviar el mensaje.")

    # **Esperar brevemente antes de activar la recepción**
    time.sleep(0.5)

    # Reactivar recepción continua
    send_at_command("AT+PRECV=65535", wait_time=1)

def main():
    global ser, ack_received

    time.sleep(DELAY_BEFORE / 1000.0)

    try:
        ser = serial.Serial(configTX.PORT, configTX.BAUDRATE, timeout=1)
    except Exception as e:
        print(f"TX: Error al abrir el puerto {configTX.PORT}: {e}")
        return

    print("TX: Configurando módulo como transmisor P2P...")

    # **🔹 Solución 1: Desactivar P2P RX antes de configurar**
    send_at_command("AT+PRECV=0", wait_time=1)

    # **🔹 Solución 2: Detectar los parámetros correctos antes de configurar P2P**
    print("TX: Detectando parámetros correctos para AT+P2P...")
    p2p_params = send_at_command("AT+P2P=?")
    print(f"TX: Parámetros disponibles: {p2p_params}")

    # Intentamos configurar con un valor seguro
    send_at_command("AT+P2P=915000000,7,125,1,12,10")

    # Iniciar hilo de recepción
    rx_thread = threading.Thread(target=receive_continuous, daemon=True)
    rx_thread.start()

    print("TX: Presiona 'q' para detener el envío.")
    i = 1
    while True:
        if keyboard.is_pressed('q'):
            print("TX: Deteniendo el envío...")
            break

        print(f"TX: Envío {i}: Enviando mensaje: {MESSAGE}")
        ack_received = False
        send_message(MESSAGE)

        timeout = time.time() + 3
        while time.time() < timeout:
            if ack_received:
                print("TX: Confirmación ACK recibida.")
                break
            time.sleep(0.1)
        else:
            print("TX: No se recibió confirmación.")

        time.sleep(DELAY_BETWEEN / 1000.0)
        i += 1

    ser.close()
    print("TX: Operación completada.")

if __name__ == "__main__":
    main()
