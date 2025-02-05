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
            time.sleep(2)  # Aumentar tiempo de espera para asegurar la respuesta
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

    # Configuración inicial
    send_at_command("AT+NWM=0")
    send_at_command("AT+P2P=915000000,7,0,1,8,14")
    send_at_command("AT+PRECV=65534")

    while True:
        # Intentar recibir un mensaje
        response = send_at_command("AT+RECV=?")

        if "AT_MODE_NO_SUPPORT" in response:
            print("Error: Modo no soportado. Reconfigurando...")
            # Reconfiguración del módulo
            send_at_command("AT+NWM=0")
            send_at_command("AT+P2P=915000000,7,0,1,8,14")
            send_at_command("AT+PRECV=65534")
        else:
            process_rx_event(response)

        time.sleep(1)
