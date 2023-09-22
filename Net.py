import socket
import threading

HOST = ''  # Listening to any
PORT = 8000  # The port number of the server

exit_flag = threading.Event()  # Event for indicating when to exit

# Function to send a command to the GPS tracker
def send_command(conn, command):
    conn.sendall(command.encode('utf-8'))
    print(f'Sent command to GPS Tracker: {command}')

# Function to receive data from the GPS tracker
def receive_data(conn):
    while not exit_flag.is_set():
        data = conn.recv(1024)
        if not data:
            break

        decoded_data = data.decode('utf-8', errors='ignore')
        print(f'Received data from GPS Tracker: {decoded_data}')

# Create a socket using IPv4 and TCP protocol
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        # Bind the socket to the specified IP address and port
        s.bind((HOST, PORT))

        # Listen for incoming connections
        s.listen(1)
        print(f"TCP Server is listening on {HOST}:{PORT}")

        # Accept a client connection
        conn, addr = s.accept()
        print(f"Connected by {addr}")

        with conn:
            # Start a thread for receiving data from the GPS tracker
            receive_thread = threading.Thread(target=receive_data, args=(conn,))
            receive_thread.start()

            while not exit_flag.is_set():
                # Get user input for sending commands
                command = input("Enter command for GPS Tracker (or 'exit' to quit): ")
                if command.lower() == 'exit':
                    exit_flag.set()
                    break

                # Send the command to the GPS tracker
                send_command(conn, command)

            receive_thread.join()  # Wait for the receive thread to finish

    except Exception as e:
        print(f"An error occurred: {e}")
