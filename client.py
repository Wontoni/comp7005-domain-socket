import socket
import sys

socket_path = '/tmp/domain_socket'
client = None

def main():
    global socket_path, client
    check_args(sys.argv)
    words = read_file(sys.argv[1])

    if words:
        create_socket()
        connect_client(socket_path)
        send_message(words)
        receieve_response()

        close_socket_client(client)

def check_args(args):
    try:
        if len(args) != 2:
            raise Exception("Invalid number of arguments")
        elif not args[1].endswith('.txt'):
            raise Exception("Invalid file extension, please input a .txt file")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

def create_socket():
    try: 
        global client
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    except Exception as e:
        print(f"Error: Failed to create client socket")
        exit(1)

def connect_client(path):
    try: 
        client.connect(path)
    except Exception as e:
        print(f"Error: Failed to connect to socket path")
        exit(1)

def send_message(words):
    try: 
        encoded = words.encode()
        x = str(len(words)).encode()
        client.sendall(x)
        client.recv(1)

        client.sendall(encoded)
    except Exception as e:
        print(e)
        print(f"Error: Failed to send words")
        exit(1)

def receieve_response():
    try: 
        response = client.recv(1024)
        print(f'Received response\n{response.decode()}')
    except Exception as e:
        print(f"Error: Failed to receive response")
        exit(1)

def close_socket_client(client):
    try: 
        client.close()
    except Exception as e:
        print(f"Error: Failed to close socket")
        exit(1)

def read_file(file_name):
    try:
        with open(file_name, 'r') as file:
            content = file.read()
            if not content:
                raise Exception("File is empty.")
            formatted_data = replace_new_lines(content)
            return formatted_data
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
    except Exception as e:
        print(f"Error: {e}")

def replace_new_lines(text_data):
    try:
        res = text_data.replace('\n', ' ')
        return res
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()