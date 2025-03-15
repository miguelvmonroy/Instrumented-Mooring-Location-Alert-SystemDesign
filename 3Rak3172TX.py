import serial
import time
import keyboard
import configTX 

#####################################################################

def delay_ms(milliseconds):
    time.sleep(milliseconds / 1000.0)

delay_before = 1000  # Retardo antes del mensaje (en ms)
delay_between = 500  # Retardo después del mensaje (en ms)

# Mensaje a enviar
message = "486F6C61206D756E646F20636963657365"

def send_at_command(ser, command, timeout=2):
    try:
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        print(f"Enviando comando: {command}")
        ser.write((command + '\r\n').encode())  
        time.sleep(0.1)  
        response = ser.read_until().decode(errors='ignore').strip()  
        print(f"Respuesta: {response}")
        return response
    except Exception as e:
        return f"Error: {e}"

def configurar_modulo(ser):
    print("Configurando módulo como transmisor P2P...")

    if "OK" not in send_at_command(ser, "AT+NWM=0"):
        print("Error al configurar el modo P2P")
        return False
    
# Obtener y mostrar la versión del firmware
    version = send_at_command(ser, "AT+VER=?")
    print(f"Versión del firmware: {version}")

# Otras variables para almacenar respuestas de comandos AT
    VarPFREQ = send_at_command(ser, "AT+PFREQ=?")  
    print(f"Frecuencia del modo P2P AT+PFREQ: {VarPFREQ}")

    VarPSF = send_at_command(ser, "AT+PSF=?")  
    print(f"Factor de dispersión del modo P2P AT+PSF: {VarPSF}")

    VarPBW = send_at_command(ser, "AT+PBW=?")  
    print(f"Ancho de banda del modo P2P AT+PBW: {VarPBW}")


    VarPCR = send_at_command(ser, "AT+PCR=?")  
    print(f"Tasa de código de modo P2P AT+PCR: {VarPCR}")

    VarPPL = send_at_command(ser, "AT+PPL=?")  
    print(f"Longitud del preámbulo del modo P2P AT+PPL: {VarPPL}")


    VarPTP = send_at_command(ser, "AT+PTP=?")  
    print(f"Alimentación TX en modo P2P AT+PTP: {VarPTP}")
##############
#PRESENTAN ANOMALIAS




##############
#PRESENTAN ANOMALIAS

    VarCAD = send_at_command(ser, "AT+CAD=?")  
    print(f"Detección de actividad de canal P2P AT+CAD: {VarCAD}")

    VarENCRY = send_at_command(ser, "AT+ENCRY=?")  
    print(f"Cifrado P2P habilitado AT+ENCRY: {VarENCRY}")

    VarENCKEY = send_at_command(ser, "AT+ENCKEY=?")  
    print(f"Clave de cifrado P2P AT+ENCKEY: {VarENCKEY}")

    VarPCRYPT = send_at_command(ser, "AT+PCRYPT=?")  
    print(f"Estado de la cripta P2P AT+PCRYPT: {VarPCRYPT}")

    VarPKEY = send_at_command(ser, "AT+PKEY=?")  
    print(f"Clave de cifrado y descifrado P2P AT+PKEY: {VarPKEY}")
    
    VarCRYPIV = send_at_command(ser, "AT+CRYPIV=?")  
    print(f"Encriptación P2P IV AT+CRYPIV: {VarCRYPIV}")

    VarIQINVER = send_at_command(ser, "AT+IQINVER=?")  
    print(f" Inversión P2P IQ AT+IQINVER: {VarIQINVER}")

    VarSYNCWORD = send_at_command(ser, "AT+SYNCWORD=?")  
    print(f"  Sincronía P2P en modo P2P AT+SYNCWORD: {VarSYNCWORD}")

    VarRFFREQUENCY = send_at_command(ser, "AT+RFFREQUENCY=?")  
    print(f" Frecuencia en modo P2P AT+RFFREQUENCY: {VarRFFREQUENCY}")

    VarTXOUTPUTPOWER = send_at_command(ser, "AT+TXOUTPUTPOWER=?")  
    print(f" P2P Tx Power (5 - 22) AT+TXOUTPUTPOWER: {VarTXOUTPUTPOWER}")

    VarBANDWIDTH = send_at_command(ser, "AT+BANDWIDTH=?")  
    print(f" Ancho de banda P2P AT+BANDWIDTH: {VarBANDWIDTH}")

    VarSPREADINGFACTOR = send_at_command(ser, "AT+SPREADINGFACTOR=?")  
    print(f" Factor de dispersión P2P AT+SPREADINGFACTOR: {VarSPREADINGFACTOR}")

    VarCODINGRATE = send_at_command(ser, "AT+CODINGRATE=?")  
    print(f" Tasa de codificación P2P AT+CODINGRATE: {VarCODINGRATE}")

    VarPREAMBLELENGTH = send_at_command(ser, "AT+PREAMBLELENGTH=?")  
    print(f"  Longitud del preámbulo P2P AT+PREAMBLELENGTH: {VarPREAMBLELENGTH}")


    VarSYMBOLTIMEOUT = send_at_command(ser, "AT+SYMBOLTIMEOUT=?")  
    print(f"  Tiempo de espera del símbolo P2P AT+SYMBOLTIMEOUT: {VarSYMBOLTIMEOUT}")



# Variable3 = send_at_command(ser, "AT+P2P=?")  
# print(f"Clave de cifrado y descifrado P2P: {Variable3}")



    configuraciones_p2p = [
        "AT+P2P=915000000:7:0:0:8:14",
        "AT+P2P=915000000:7:125:0:8:14",
        "AT+P2P=915000000:7:0:1:8:14",
        "AT+P2P=915000000:7:125:1:8:14"

#send_at_command("AT+P2P=915000000,7,125,1,22,8")  

# Ejemplo Frecuencia 915 MHz, SF=7, BW=125kHz, CRC=ON, TxPower=10 dBm

#Parámetros del comando:
# Frecuencia: 915000000 (915 MHz, ajusta según tu región: 868 MHz en Europa, 915 MHz en América).
# SF (Spreading Factor): 7 (equilibrio entre alcance y velocidad).
# BW (Bandwidth): 125 (ancho de banda en kHz).
# CRC: 1 para habilitar el chequeo de errores (recomendado).
# Potencia de Transmisión: 14 dBm.
# Paquete: 8 bytes como tamaño máximo del paquete.
    
    ]

    for config in configuraciones_p2p:
        response = send_at_command(ser, config)
        if "OK" in response:
            print(f"Configuración P2P establecida: {config}")
            break
    else:
        print("No se pudo configurar P2P. Verifica los parámetros o el firmware.")
        return False

    if "OK" not in send_at_command(ser, "AT+PRECV=0"):
        print("Error al desactivar la recepción")
        return False

    print("Módulo configurado correctamente.")
    return True

def enviar_mensajes(ser):
    print("Presiona 'q' en cualquier momento para salir del ciclo de envío.")

    i = 1
    try:
        while True:
            if keyboard.is_pressed('q'):
                print("Deteniendo el envío de mensajes...")
                break

            print(f"Envío {i}: {message}")
            response = send_at_command(ser, f"AT+PSEND={message}")
            
            if "OK" not in response:
                print("Error en el envío del mensaje.")
            
            delay_ms(delay_between)
            i += 1
    except KeyboardInterrupt:
        print("Interrupción manual detectada. Saliendo...")

if __name__ == "__main__":
    print(f"Esperando {delay_before} ms antes de iniciar el envío...")
    delay_ms(delay_before)

    try:
        with serial.Serial(configTX.PORT, configTX.BAUDRATE, timeout=5) as ser:
            if configurar_modulo(ser):
                enviar_mensajes(ser)
    except serial.SerialException as e:
        print(f"Error al abrir el puerto serie: {e}")
    finally:
        print("Operación completada.")
