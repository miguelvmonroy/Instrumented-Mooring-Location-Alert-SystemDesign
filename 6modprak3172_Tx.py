import threading
import serial
import time
import keyboard
import configTX  # Debe definir PORT y BAUDRATE

ACK_EXPECTED = "ACK"
DELAY_BEFORE = 1000      # milisegundos antes de iniciar
DELAY_BETWEEN = 2000     # milisegundos entre envíos
MESSAGE = "17726674746566"

# Variables globales
ser = None
ack_received = False

def receive_continuous():
    """
    Hilo que mantiene el puerto en modo recepción continua y verifica si llega el ACK.
    """
    global ack_received, ser
    try:
        # Activar recepción continua
        ser.write("AT+PRECV=65535\r\n".encode())
        time.sleep(1)
        print("TX: Modo de recepción continua activado.")
        while True:
            if ser.in_waiting:
                data = ser.read_all().decode(errors='ignore')
                print("TX: Datos recibidos:", data)
                if ACK_EXPECTED in data:
                    print("TX: Se detectó ACK en la recepción continua.")
                    ack_received = True
            time.sleep(0.1)
    except Exception as e:
        print("TX: Error en la recepción continua:", e)

def send_message(message):
    """
    Envía el mensaje usando el comando AT+PSEND.
    """
    global ser
    try:
        # Limpiar buffers para evitar lecturas de datos antiguos
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        cmd = f"AT+PSEND={message}"
        print("TX: Enviando comando:", cmd)
        ser.write((cmd + "\r\n").encode())
        time.sleep(1)
        response = ser.read_all().decode(errors='ignore')
        print("TX: Respuesta al envío:", response.strip())
    except Exception as e:
        print("TX: Error al enviar mensaje:", e)

def main():
    global ser, ack_received
    # Espera inicial
    time.sleep(DELAY_BEFORE / 1000.0)
    
    # Abrir el puerto una sola vez
    try:
        ser = serial.Serial(configTX.PORT, configTX.BAUDRATE, timeout=1)
    except Exception as e:
        print(f"TX: Error al abrir el puerto {configTX.PORT}: {e}")
        return

    # Configurar el módulo en modo P2P (ajusta los comandos según tus requerimientos)
    print("TX: Configurando módulo como transmisor P2P...")
    ser.write("AT+NWM=0\r\n".encode())
    time.sleep(0.5)
    ser.write("AT+P2P=915000000,7,0,1,8,14\r\n".encode())
    time.sleep(0.5)
    
    # Iniciar el hilo de recepción continua
    rx_thread = threading.Thread(target=receive_continuous, daemon=True)
    rx_thread.start()
    
    print("TX: Presiona 'q' para detener el envío.")
    i = 1
    while True:
        if keyboard.is_pressed('q'):
            print("TX: Deteniendo el envío...")
            break
        
        print(f"TX: Envío {i}: Enviando mensaje: {MESSAGE}")
        ack_received = False  # Reiniciar la bandera de confirmación
        send_message(MESSAGE)
        
        # Espera hasta 3 segundos para recibir el ACK
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
