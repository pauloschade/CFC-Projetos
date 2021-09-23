def make_head(lista):
    head = b''
    for i in lista:
        bytes_i = (i).to_bytes(1, byteorder='big')
        head += bytes_i
    return head

def make_package(tipo, n):
    lista_head = [tipo, 10, 11, 0, 0, n, 0,0,0,0]
    head = make_head(lista_head)
    package = head + b'' + b'\xFF\xAA\xFF\xAA'
    return package










