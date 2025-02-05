import serial
import time
import configRX

def send_at_command(command):
    """Envía un comando AT al módulo y devuelve la respuesta."""
    try:
        with serial.Serial(configRX.PORT, configRX.BAUDRATE, timeout=5) as ser:
            ser.reset_input_buffer()  # Limpia el buffer de entrada
            ser.reset_output_buffer()  # Limpia el buffer de salida
            ser.write((command + '\r\n').encode())  # Enviar comando
            time.sleep(2)  # Aumentar el tiempo de espera para asegurar la respuesta
            response = ser.read_all().decode(errors='ignore').strip()  # Leer respuesta
            print(f"Respuesta del comando {command}: {response}")  # Imprimir respuesta para depuración
            return response or "Sin respuesta"
    except Exception as e:
        return f"Error: {e}"

def process_rx_event(response):
    """Procesa los eventos de recepción de datos."""
    if "+EVT:RXP2P" in response:
        parts = response.split(":")
        if len(parts) >= 4:
            hex_data = parts[-1].strip()
            print(f"Datos codificados: {hex_data}")
            try:
                text = bytes.fromhex(hex_data).decode('utf-8', errors='replace')
                print(f"Datos decodificados: {text}")
            except ValueError:
                print("Error en la conversión de datos.")
    else:
        print(f"Respuesta inesperada: {response}")

if __name__ == "__main__":
    print("Configurando módulo como receptor P2P...")

    # Deshabilitar la recepción P2P antes de cambiar el modo
    send_at_command("AT+PRECV=0")  # Deshabilitar recepción si está habilitada
    send_at_command("AT+NWM=0")  # Configura el módulo en modo normal
    send_at_command("AT+P2P=915000000,7,0,1,8,14")  # Configuración del modo P2P (evitar si ya está configurado)
    send_at_command("AT+PRECV=65534")  # Habilitar la recepción

    while True:
        # Comprobamos si hay eventos de recepción
        response = send_at_command("AT+PSEND=?")  # Intentamos usar un comando que puede estar disponible

        if "AT_MODE_NO_SUPPORT" in response:
            print("Error: Modo no soportado. Verificando estado de recepción...")
            # Si el comando no es soportado, solo procesamos los eventos de recepción
            process_rx_event(response)

        elif "AT_BUSY_ERROR" in response:
            print("Error: El módulo está ocupado. Esperando para reintentar...")
            time.sleep(2)  # Esperar un poco antes de reintentar
        else:
            process_rx_event(response)

        time.sleep(1)
