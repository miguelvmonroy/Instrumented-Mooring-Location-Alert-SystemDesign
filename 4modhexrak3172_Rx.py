import serial
import time
import configRX

def send_at_command(command):
    try:
        with serial.Serial(configRX.PORT, configRX.BAUDRATE, timeout=5) as ser:
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            ser.write((command + '\r\n').encode())
            time.sleep(1)
            return ser.read_all().decode(errors='ignore').strip() or "Sin respuesta"
    except Exception as e:
        return f"Error: {e}"

def process_rx_event(response):
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
    send_at_command("AT+NWM=0")
    send_at_command("AT+P2P=915000000,7,0,1,8,14")
    send_at_command("AT+PRECV=65534")

    while True:
        response = send_at_command("AT+RECV=?")
        process_rx_event(response)
        time.sleep(1)
