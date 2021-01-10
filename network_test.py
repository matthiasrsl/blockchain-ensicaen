from network import NetworkHandler
import sys

if __name__ == "__main__":
    args = sys.argv
    print(args)
    handler = NetworkHandler(args[2])
    if args[1] == "server":
        handler.start_server()
        handler.run_server()
    else:
        handler.send_message(args[3])