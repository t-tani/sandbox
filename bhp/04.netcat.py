import sys
import argparse
import socket as s
import threading
import subprocess


def get_args():
    parser = argparse.ArgumentParser(description='t0nny netcat tools')
    parser.add_argument('-l', '--listen',
                        action='store_true',
                        default=False)
    parser.add_argument('-e', '--execute',
                        action='store',
                        default="")
    parser.add_argument('-c', '--command',
                        action='store_true',
                        default=False)
    parser.add_argument('-u', '--upload',
                        action='store',
                        default="")
    parser.add_argument('-t', '--target',
                        action='store',
                        default='0.0.0.0')
    parser.add_argument('-p', '--port',
                        type=int,
                        default=0)
    parser.add_argument('-d', '--dummy',
                        action='append')
    args = parser.parse_args()
    return args


def client_sender(buffer, target, port):
    client = s.socket(s.AF_INET, s.SOCK_STREAM)

    try:
        client.connect((target, port))

        if len(buffer):
            client.sent(buffer)

        while True:
            recv_len = 1
            res = ""

            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                res += data

                if recv_len < 4096:
                    break

            print res,

            buffer = raw_input("")
            buffer += "\n"

            client.send(buffer)

    except:
        print "[*] Exception! Exiting."
        client.close()


def server_loop(target, port, upload, execute, command):
    server = s.socket(s.AF_INET, s.SOCK_STREAM)
    server.bind((target, port))

    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        client_thread = threading.Thread(
            target=client_hander,
            args=(client_socket, upload, execute, command))
        client_thread.start()


def run_command(command):
    command = command.rstrip()
    try:
        output = subprocess.check_output(
            command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = "Faild to excute command. \r\n"
    return output


def client_hander(client_socket, upload, execute, command):
    if len(upload):
        file_buffer = ""

        while True:
            data = client_socket.recv(1024)

            if len(data) == 0:
                break
            else:
                file_buffer += data

        try:
            file_descriptor = open(upload, "wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            client_socket.send(
                "Successfully saved file to %s\r\n" % upload)
        except:
            client_socket.send(
                "Faild to save file to %s\r\n" % upload)

    if len(execute):
        output = run_command(execute)

        client_socket.send(output)

    if command:
        prompt = ">>"
        client_socket.send(prompt)

        while True:

            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)

            res = run_command(cmd_buffer)
            res += prompt

            client_socket.send(res)


def main():
    args = get_args()

    if not args.listen and len(args.target) and args.port > 0:
        buffer = sys.stdin.read()

        client_sender(buffer, args.target, args.port)

    if args.listen:
        server_loop(args.target, args.port,
                    args.upload, args.execute, args.command)


if __name__ == '__main__':
    main()
