def make_head(lista):
    head = b''
    for i in lista:
        bytes_i = (i).to_bytes(1, byteorder='big')
        head += bytes_i
    return head

def make_package(tipo, n):
    lista_head = [tipo, 10, 11, 0, 0, 0, n,0,0,0]
    head = make_head(lista_head)
    package = head + b'' + b'\xFF\xAA\xFF\xAA'
    return package

def crc16(data: bytes):
    '''
    CRC-16-ModBus Algorithm
    '''
    data = bytearray(data)
    poly = 0xA001
    crc = 0xFFFF
    for b in data:
        crc ^= (0xFF & b)
        for _ in range(0, 8):
            if (crc & 0x0001):
                crc = ((crc >> 1) & 0xFFFF) ^ poly
            else:
                crc = ((crc >> 1) & 0xFFFF)

    return np.uint16(crc)










