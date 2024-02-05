import socket
import os
import re
import sys
import fcntl
import errno
from time import sleep

connection = None
server = None
socket_path = '/tmp/domain_socket'
def main():
    remove_existing_socket(socket_path)
    create_socket()
    bind_socket(socket_path)
    listen_connections()
    try:
        while True:
            
            data = accept_connection()
            # decode and manipulate data
            decoded_data = check_data(data)
            words = get_words(decoded_data)
            word_count = get_word_count(words)
            char_count = get_char_count(words)
            char_freq = get_char_freq(words)
            sorted_chars = sort_dict(char_freq)
            response = format_response(word_count, char_count, sorted_chars)
            # Send a response back to the client
            send_response(response)
    except Exception as e:
        print(f"Error: Failed to receive data from client")

def bind_socket(path):
    try:
        server.bind(path)
    except Exception as e:
        print(f"Error: Failed to bind socket path")
        exit(1)

def create_socket():
    try:
        global server
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    except Exception as e:
        print(f"Error: Faield to create socket server")
        exit(1)
        
def remove_existing_socket(path):
    try:
        os.unlink(path)
    except OSError:
        if os.path.exists(path):
            print(f"Error: Path already exists")
            exit(1)

def listen_connections():
    try:
        server.listen(1)
        print('Server is listening for incoming connections...')
    except Exception as e:
        print(f"Error: Failed to listen to connections")
        exit(1)

def accept_connection():
    try:
        global connection
        connection, client_addr = server.accept()
        
        print('Connection Received: ', str(connection).split(", ")[0][-4:])
        expected_data = connection.recv(1024)
        decoded_expected = int(expected_data.decode())

        connection.sendall('0'.encode())

        received_data = b''
        while len(received_data) < decoded_expected:
            try:
                data = connection.recv(1024)
                received_data += data
            except Exception as e:
                print("Error: Failed to receive data")
        return received_data
                


    except Exception as e:
        print(f"Error: {e}")

def check_data(data):
    try:
        if not data:
            raise Exception("Failed to receive data")
            
        res = data.decode()
        return res
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
        
def send_response(response):
    try:
        connection.sendall(response.encode())
    except Exception as e:
        print(e)
        print(f"Error: Failed to send response to client")
        exit(1)

def close_socket_server(connection, socket_path):
    try:
        connection.close()
        os.unlink(socket_path)
    except Exception as e:
        print(f"Error: Failed to close the socket")
        exit(1)

def get_words(word_string):
    formatted_string = remove_whitespace(word_string)
    words = formatted_string.split(" ")
    words = [x for x in words if x]
    return words

def get_word_count(words):
    return len(words)

def remove_whitespace(word_string):
    try:
        return re.sub(' +', ' ', word_string)
    except Exception as e:
        print(e)
        print(f"Error: Failed to remove whitespaces in data")
        exit(1)

def get_char_count(words):
    count = 0
    for word in words:
        count += len(word)
    return count

def get_char_freq(words):
    char_dict = {}
    words = [word.lower() for word in words]
    words = "".join(words)
    for c in words:
        if c in char_dict:
            char_dict[c] += 1
        else:
            char_dict[c] = 1
    return char_dict

def format_response(word_count, char_count, char_freq):
    response = "Word Count: %d\nCharacter Count: %d\nCharacter Frequencies:"%(word_count, char_count)

    for key, value in char_freq.items():
        response += "\n%s: %d"%(key, value)
    return response

def sort_dict(char_freq):
    keys = list(char_freq.keys())
    keys.sort()
    return {i: char_freq[i] for i in keys}

main()
