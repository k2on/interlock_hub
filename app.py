from local_server import LocalServer

server = LocalServer()

if __name__ == '__main__':
    try:
        server.run()
    except KeyboardInterrupt:
        server.stop()
