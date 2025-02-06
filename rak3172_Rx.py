import serial
import time

# Configuración del puerto y velocidad
PORT = '/dev/ttyUSB0'  # Ajusta según tu puerto
BAUDRATE = 115200  

def send_at_command(command, timeout=5):
    """Envía un comando AT y devuelve la respuesta."""
    try:
        with serial.Serial(PORT, BAUDRATE, timeout=timeout) as ser:
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            print(f"Enviando comando: {command}")
            ser.write((command + '\r\n').encode())  
            time.sleep(0.5)
            response = ser.read_all().decode(errors='ignore')
            return response.strip() or "Sin respuesta"
    except serial.SerialException as e:
        return f"Error de conexión: {e}"
    except Exception as e:
        return f"Error inesperado: {e}"

if __name__ == "__main__":
    print("Configurando módulo como receptor P2P...")
    send_at_command("AT+NWM=0")  
    send_at_command("AT+P2P=915000000,7,125,1,14,8")  

    print("Esperando mensajes del transmisor...")

    try:
        while True:
            # Resetear recepción antes de escuchar de nuevo
            send_at_command("AT+PRECV=0")  
            time.sleep(0.5)
            response = send_at_command("AT+PRECV=65535", timeout=10)

            if "+EVT:RXP2P" in response:
                print(f"Datos recibidos: {response}")
            elif "AT_BUSY_ERROR" in response:
                print("Error: El módulo está ocupado. Intentando de nuevo...")
                send_at_command("AT+PRECV=0")  # Reiniciar recepción
            else:
                print("No se recibió mensaje.")

            time.sleep(1)  # Pequeña espera antes de la siguiente recepción
    except KeyboardInterrupt:
        print("Recepción interrumpida manualmente.")
