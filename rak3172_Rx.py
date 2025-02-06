import serial
import time

# Configuración del puerto y velocidad
PORT = '/dev/ttyUSB0'  # Cambia según tu puerto detectado
BAUDRATE = 115200  # Velocidad predeterminada del módulo

def send_at_command(command):
    """Envía un comando AT al módulo y devuelve la respuesta."""
    try:
        with serial.Serial(PORT, BAUDRATE, timeout=5) as ser:
            ser.reset_input_buffer()  # Limpia el buffer de entrada
            ser.reset_output_buffer()  # Limpia el buffer de salida
            print(f"Enviando comando: {command}")
            ser.write((command + '\r\n').encode())  # Enviar comando
            time.sleep(1.5)  # Aumentar tiempo de espera para respuesta
            response = ser.read_all().decode(errors='ignore')  # Leer respuesta
            return response.strip() or "Sin respuesta"
    except serial.SerialException as e:
        return f"Error de conexión: {e}"
    except Exception as e:
        return f"Error: {e}"

# Código para el módulo receptor
if __name__ == "__main__":
    print("Configurando módulo como receptor P2P...")

    # Detener recepción si ya está activada
    send_at_command("AT+PRECV=0")

    # Configurar el módulo en modo P2P    
    send_at_command("AT+NWM=0") # Cambiar a modo P2P
    send_at_command("AT+P2P=915000000,7,125,1,14,8")  
    # Ejemplo Frecuencia 915 MHz, SF=7, BW=125kHz, CRC=ON, TxPower=14 dBm
    
    print("Esperando mensaje del transmisor...")
    response = send_at_command("AT+PRECV=65535") # Modo Continuo para recibir mensajes
    print(f"Datos recibidos: {response}")

    # Verificar la versión del firmware
    response = send_at_command("AT+VER=?") # Obtener versión del firmware
    print(f"Versión del firmware: {response}")
