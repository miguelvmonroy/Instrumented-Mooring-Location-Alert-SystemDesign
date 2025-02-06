# -*- coding: utf-8 -*-
import serial
import time
import configRX  # Sigue usando configRX para el puerto y baudrate

DELAY_BETWEEN_CHECKS = 0.1

def send_at_command(command, port, baudrate, timeout=1):
    try:
        with serial.Serial(port, baudrate, timeout=timeout) as ser:
            ser.write((command + '\r\n').encode())
            time.sleep(0.1)
            return ser.read_all().decode(errors='ignore').strip()
    except Exception as e:
        return f"Error: {e}"

def process_rx_event(response):
    if "+EVT:RXP2P" in response:
        parts = response.split(":")
        if len(parts) >= 4:
            hex_data = parts[-1].strip()
            try:
                text = bytes.fromhex(hex_data).decode('utf-8')
                print(f"Mensaje recibido: {text}")
                return
            except Exception:
                print(f"Datos en hex: {hex_data}")
    print(f"Respuesta cruda: {response}")

def configure_p2p_mode(port, baudrate):
    print("Configurando módulo como receptor P2P...")
    send_at_command("AT+NWM=0", port, baudrate)
    send_at_command("AT+P2P=915000000,7,0,1,8,14", port, baudrate)  # Parámetros fijos

def start_reception(port, baudrate):
    print("Activando recepción continua...")
    send_at_command("AT+PRECV=65535", port, baudrate)

def main():
    configure_p2p_mode(configRX.PORT, configRX.BAUDRATE)
    start_reception(configRX.PORT, configRX.BAUDRATE)
    
    try:
        with serial.Serial(configRX.PORT, configRX.BAUDRATE, timeout=1) as ser:
            print("Escuchando mensajes...")
            while True:
                if ser.in_waiting > 0:
                    response = ser.read_all().decode(errors='ignore')
                    if response:
                        process_rx_event(response)
                time.sleep(DELAY_BETWEEN_CHECKS)
    except KeyboardInterrupt:
        print("\nOperación detenida.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
