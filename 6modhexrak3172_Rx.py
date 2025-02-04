import serial
import time
import configRX  

ACK_MESSAGE = "41434B"  # "ACK" en hexadecimal (ASCII -> HEX)
DELAY_BETWEEN_CHECKS = 0.1

def send_at_command(command, port, baudrate, timeout=1):
    """
    Envía un comando AT y retorna la respuesta.
    """
    try:
        with serial.Serial(port, baudrate, timeout=timeout) as ser:
            ser.write((command + '\r\n').encode())
            time.sleep(0.1)
            return ser.read_all().decode(errors='ignore').strip()
    except Exception as e:
        return f"Error: {e}"

def process_rx_event(response, port, baudrate):
    """
    Procesa el mensaje recibido y envía el ACK.
    """
    if "+EVT:RXP2P" in response:
        parts = response.split(":")
        if len(parts) >= 4:
            hex_data = parts[-1].strip()
            try:
                text = bytes.fromhex(hex_data).decode('utf-8')
                print(f"RX: Mensaje recibido: {text} (HEX: {hex_data})")

                # **ESPERAR PARA QUE TX ENTRE EN RECEPCIÓN**
                time.sleep(1.5)

                print("RX: Enviando confirmación ACK...")
                ack_response = send_at_command(f"AT+PSEND={ACK_MESSAGE}", port, baudrate)
                print(f"RX: Respuesta al envío del ACK: {ack_response}")

                return
            except Exception:
                print(f"RX: Datos en hex no convertidos: {hex_data}")
    print(f"RX: Respuesta cruda: {response}")

def main():
    port = configRX.PORT
    baudrate = configRX.BAUDRATE
    send_at_command("AT+NWM=0", port, baudrate)
    send_at_command(f"AT+P2P={configRX.P2P_CONFIG}", port, baudrate)
    send_at_command("AT+PRECV=65535", port, baudrate)

    try:
        with serial.Serial(port, baudrate, timeout=1) as ser:
            print("RX: Escuchando mensajes...")
            while True:
                if ser.in_waiting > 0:
                    response = ser.read_all().decode(errors='ignore')
                    if response:
                        process_rx_event(response, port, baudrate)
                time.sleep(DELAY_BETWEEN_CHECKS)
    except KeyboardInterrupt:
        print("\nRX: Operación detenida.")
    except Exception as e:
        print(f"RX: Error: {e}")

if __name__ == "__main__":
    main()
