import serial
import time
import configRX  # Debe definir PORT, BAUDRATE y P2P_CONFIG

DELAY_BETWEEN_CHECKS = 0.1
ACK_MESSAGE = "ACK"  # Confirmación en formato ASCII

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
    Procesa el evento de recepción y, de encontrar el mensaje, envía el ACK.
    Se asume que el payload viene en hexadecimal tras el último ':'.
    """
    if "+EVT:RXP2P" in response:
        parts = response.split(":")
        if len(parts) >= 4:
            hex_data = parts[-1].strip()
            try:
                text = bytes.fromhex(hex_data).decode('utf-8')
                print("RX: Mensaje recibido:", text)
                # Enviar ACK al transmisor
                print("RX: Enviando confirmación...")
                send_at_command(f"AT+PSEND={ACK_MESSAGE}", port, baudrate)
                return
            except Exception as ex:
                print("RX: Error decodificando el mensaje, datos hex:", hex_data)
    else:
        print("RX: Respuesta cruda:", response)

def configure_p2p_mode(port, baudrate):
    """
    Configura el módulo en modo P2P.
    """
    print("RX: Configurando módulo como receptor P2P...")
    send_at_command("AT+NWM=0", port, baudrate)
    send_at_command(f"AT+P2P={configRX.P2P_CONFIG}", port, baudrate)

def start_reception(port, baudrate):
    """
    Activa la recepción continua.
    """
    print("RX: Activando recepción continua...")
    send_at_command("AT+PRECV=65535", port, baudrate)

def main():
    configure_p2p_mode(configRX.PORT, configRX.BAUDRATE)
    start_reception(configRX.PORT, configRX.BAUDRATE)
    
    try:
        with serial.Serial(configRX.PORT, configRX.BAUDRATE, timeout=1) as ser:
            print("RX: Escuchando mensajes...")
            while True:
                if ser.in_waiting > 0:
                    response = ser.read_all().decode(errors='ignore')
                    if response:
                        process_rx_event(response, configRX.PORT, configRX.BAUDRATE)
                time.sleep(DELAY_BETWEEN_CHECKS)
    except KeyboardInterrupt:
        print("\nRX: Operación detenida.")
    except Exception as e:
        print("RX: Error:", e)

if __name__ == "__main__":
    main()
