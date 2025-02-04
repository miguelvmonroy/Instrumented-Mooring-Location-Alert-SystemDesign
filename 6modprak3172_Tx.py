import threading
import serial
import time
import keyboard
import configTX

# Constants
ACK_EXPECTED = "ACK"
DELAY_BEFORE = 1000  # ms before starting
DELAY_BETWEEN = 3000  # ms between transmissions
ACK_TIMEOUT = 3  # seconds to wait for ACK
MESSAGE = "17726674746566"

class LoRaTransmitter:
    def __init__(self):
        self.ser = None
        self.ack_received = False

    def send_at_command(self, command, wait_time=1.5):
        """
        Sends an AT command to the module and returns the response.
        """
        try:
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
            print(f"TX: Sending command: {command}")
            self.ser.write((command + "\r\n").encode())
            time.sleep(wait_time)  # Wait for response
            response = self.ser.read_all().decode(errors='ignore').strip()
            print(f"TX: Command response: {response}")
            return response
        except Exception as e:
            print(f"TX: Error sending command {command}: {e}")
            return ""

    def receive_continuous(self):
        """
        Thread that keeps the port in continuous receive mode and checks for ACK.
        """
        try:
            while True:
                if self.ser.in_waiting:
                    data = self.ser.read_all().decode(errors='ignore').strip()
                    print("TX: Data received:", data)
                    if ACK_EXPECTED in data:
                        print("TX: ACK detected in reception.")
                        self.ack_received = True
                time.sleep(0.1)
        except Exception as e:
            print("TX: Error in continuous reception:", e)

    def send_message(self, message):
        """
        Sends the message and waits for confirmation.
        """
        # Disable reception to avoid AT_BUSY_ERROR
        self.send_at_command("AT+PRECV=0", wait_time=1)

        # Send message
        response = self.send_at_command(f"AT+PSEND={message}", wait_time=2)

        # Check if the message was sent successfully
        if "+EVT:TXP2P DONE" in response:
            print("TX: Message sent successfully.")
        else:
            print("TX: Error sending message.")

        # Re-enable reception immediately after sending
        self.send_at_command("AT+PRECV=65535", wait_time=1)

    def main(self):
        """
        Main function to configure the module and handle message transmission.
        """
        time.sleep(DELAY_BEFORE / 1000.0)

        try:
            self.ser = serial.Serial(configTX.PORT, configTX.BAUDRATE, timeout=1)
        except Exception as e:
            print(f"TX: Error opening port {configTX.PORT}: {e}")
            return

        print("TX: Configuring module as P2P transmitter...")

        # Configure module
        self.send_at_command("AT+PRECV=0", wait_time=1)
        self.send_at_command("AT+NWM=0")
        self.send_at_command("AT+P2P=915000000,7,125,1,12,10")

        # Start reception thread
        rx_thread = threading.Thread(target=self.receive_continuous, daemon=True)
        rx_thread.start()

        print("TX: Press 'q' to stop transmission.")
        i = 1
        while True:
            if keyboard.is_pressed('q'):
                print("TX: Stopping transmission...")
                break

            print(f"TX: Transmission {i}: Sending message: {MESSAGE}")
            self.ack_received = False
            self.send_message(MESSAGE)

            # Wait for ACK
            timeout = time.time() + ACK_TIMEOUT
            while time.time() < timeout:
                if self.ack_received:
                    print("TX: ACK confirmation received.")
                    break
                time.sleep(0.1)
            else:
                print("TX: No confirmation received.")

            time.sleep(DELAY_BETWEEN / 1000.0)
            i += 1

        self.ser.close()
        print("TX: Operation completed.")

if __name__ == "__main__":
    transmitter = LoRaTransmitter()
    transmitter.main()