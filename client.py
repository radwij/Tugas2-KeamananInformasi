import socket
import threading
import sys
from encryption import *

nickname = input("Enter your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

def receive():
  while True:
    try:
      message = client.recv(1024).decode('utf-8')
      # print(message)

      if ":" in message:
        msg_type, content = message.split(":", 1)
        if msg_type == "system":
          print(content)
        elif msg_type == "user":
          decrypted_message = main('d', content, 'mysecret')
          print(decrypted_message)
      else:
        # Handle single messages like "NICK" for nickname request
        if message == 'NICK':
          client.send(nickname.encode('utf-8'))
        else:
          print(message)

    except Exception as e:
      print(f"An error occurred in receive function: {e}")
      break  # Exit the loop on error

  client.close()  # Ensure socket is closed if loop exits

def write():
  while True:
    try:
      message = f'{nickname}: {input("")}'
      encrypted_message = main('e', message, 'mysecret')
      # print(f"Encrypted message: {encrypted_message}")
      client.send(encrypted_message.encode('utf-8'))

    except Exception as e:
      print(f"An error occurred in write function: {e}")
      client.close()
      break  # Exit the loop

try:
  receive_thread = threading.Thread(target=receive)
  receive_thread.start()

  write_thread = threading.Thread(target=write)
  write_thread.start()

  receive_thread.join()
  write_thread.join()

except KeyboardInterrupt:
  print("\nDisconnecting from the server...")
  client.close()
  sys.exit(0)
