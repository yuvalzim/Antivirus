from project.consts import LENGTH_FIELD_SIZE  # Importing LENGTH_FIELD_SIZE from consts module

def send_data(socket, msg):
    """
    Sends data over a socket connection. The data is preceded by its length
    encoded as a fixed-size string.

    Args:
        socket (socket.socket): The socket object to send data through.
        msg (bytes): The message to be sent.
    """
    # Convert the length of the message to a fixed-size string
    data_len = str(len(msg)).zfill(LENGTH_FIELD_SIZE)
    # Send the length of the message encoded in bytes
    socket.send(data_len.encode())
    # Send the actual message
    socket.send(msg)

def get_data(socket):
    """
    Receives data from a socket connection. The function first reads the
    fixed-size length field to determine the length of the incoming data.

    Args:
        socket (socket.socket): The socket object to receive data from.

    Returns:
        bytes: The received data.
    """
    # Receive the length of the incoming data
    data_length = int(socket.recv(LENGTH_FIELD_SIZE).decode())
    # Receive the actual data based on the received length
    data = socket.recv(data_length)
    return data
