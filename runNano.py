import argparse
# from Clients.NanoClient import NanoClient
import Clients.NanoClient as NanoClient

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
    parser.add_argument(
        '--server-port',  type=int, default=8000,
        help='The connection port of the server.')
    args = parser.parse_args()

    NanoClient.NanoClient(args.camera, args.server_addr,
                          args.stream_fps, args.server_port)
    # NanoClient(args.server_addr, args.server_port,
    #            args.stream_fps, args.camera)
