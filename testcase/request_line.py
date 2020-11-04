import sys
sys.path.append('../')
import config
import socket
from http.client import HTTPResponse

# test rfc7230 section 3.3.1: Request Line

def run():
    request_headers = []
    expected_status = []

    # multiple spaces
    request_headers.append('GET  /  HTTP/1.1\r\nHost:{}\r\n\r\n'.format(config.SERVER_ADDR))
    expected_status.append(400)

    # too long URI
    target = '/' + 'A' * (config.MAX_URI_LENGTH - 1)
    request_headers.append('GET {} HTTP/1.1\r\nHost:{}\r\n\r\n'.format(target, config.SERVER_ADDR))
    expected_status.append(414)

    # run cases
    for i in range(len(request_headers)):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((config.SERVER_ADDR, config.SERVER_PORT))
        request_header = request_headers[i]
        status = expected_status[i]
        client.send(request_header.encode())
        # read and parse http response
        http_response = HTTPResponse(client)
        http_response.begin()
        # 505 error is expected for invalid http version
        if http_response.status != status:
            print('error: {}'.format(__file__))
            print('expected status: {}, actual status: {}'.format(str(status), str(http_response.status)))
        client.close()

if __name__ == '__main__':
    run()