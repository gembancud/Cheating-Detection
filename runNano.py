import argparse
from NanoClient import nanoClient

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Video Stream')
    parser.add_argument(
            '--camera', type=int, default='0',
            help='The camera index to stream from.')
    parser.add_argument(
            '--server-addr',  type=str, default='localhost',
            help='The IP address or hostname of the SocketIO server.')
    parser.add_argument(
            '--stream-fps',  type=float, default=60.0,
            help='The rate to send frames to the server.')
    args = parser.parse_args()
    nanoClient(args.camera, args.server_addr, args.stream_fps)