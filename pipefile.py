import os
import time


def post_file(message, target):
    
    with open(f'{target}.pipe', 'w') as file:
        file.write(message)


def listen_file(name):
    
    while not os.path.exists(f'{name}.pipe'):
        time.sleep(1)
        
    with open(f'{name}.pipe', 'r') as file:
        content = file.read()

    # Delete the shared file
    os.remove(f'{name}.pipe')

    return content
