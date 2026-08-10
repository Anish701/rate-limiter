from fastapi import Request

def get_client_ip(request: Request) -> str:
    ip_header = request.headers.get('x-forwarded-for')
    if ip_header:
        return ip_header.split(',')[0].strip()

    if request.client and request.client.host:
        return request.client.host
    
    return '127.0.0.1'