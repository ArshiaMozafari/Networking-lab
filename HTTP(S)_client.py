import socket
import ssl


def url_parser(url):
    if url.startswith('http://'):
        url = url[7:]
        default_port = 80
    elif url.startswith('https://'):
        url = url[8:]
        default_port = 443
    else:
        default_port = 80
    

    if '/' in url:
        host_part, path = url.split('/', 1)
        path = '/' + path
    else:
        host_part = url
        path = '/'

    if ':' in host_part:
        host, port_str = host_part.split(':', 1)
        port = int(port_str)
    else:
        host = host_part
        port = default_port

    return host, port,  path



def HTTP_client(url):
    host, port, path = url_parser(url)
    c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c_socket.settimeout(10)

    if port == 443:
        context = ssl.create_default_context()
        ssl_socket = context.wrap_socket(c_socket, server_hostname=host)
        c_socket = ssl_socket

    try:
        print(f'Connecting to {host}:{port}...')
        c_socket.connect((host, port))
        print(f'Connected!')

        request = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            "Connection: close\r\n"
            "User-Agent: MyRawHTTPClient/1.0\r\n"
            "\r\n"
        )
        c_socket.sendall(request.encode())

        response = b""
        while True:
            chunk = c_socket.recv(4096)
            if not chunk:
                break
            response += chunk
    finally:
        c_socket.close()

    header_end = response.find(b"\r\n\r\n")
    headers_raw = response[:header_end]
    body = response[header_end + 4:]
    
    header_lines = headers_raw.decode().split("\r\n")
    status_parts = header_lines[0].split(" ", 2)
    status_code = int(status_parts[1])
    
    headers = {}
    for line in header_lines[1:]:
        if ":" in line:
            key, value = line.split(":", 1)
            headers[key.strip()] = value.strip()
    
    return status_code, headers, body



# HTTP
url = "http://example.com"
status, headers, body = HTTP_client(url)
print(f'HTTP Status: {status}')

# HTTPS
url = "https://www.google.com"
status, headers, body = HTTP_client(url)
print(f'HTTPS Status: {status}')

