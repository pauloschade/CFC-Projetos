import math
import numpy as np

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

    return crc & 0xFFFF

def make_head(lista):
    head = b''
    for i in lista:
        bytes_i = (i).to_bytes(1, byteorder='big')
        head += bytes_i
    return head

def make_payload(buffer):
    bytes_per_package = 114
    size = len(buffer)
    full_packages = math.floor(size/114)
    remaining = size%114
    payload_size = []
    payload_list=[]
    for i in range (1, full_packages + 1):
        payload_list.append(buffer[(i-1)*bytes_per_package:i*bytes_per_package])
        payload_size.append(114)
    payload_list.append(buffer[size-remaining: size])
    payload_size.append(remaining)

    return payload_list, payload_size


    


def make_packages(buffer, tipo):
    heads = []
    payloads, payload_sizes = make_payload(buffer)
    total_size = len(payloads)
    for i in range(total_size):
        # tipos.append(3)
        print(hex(crc16(payloads[i])))
        lista_head = [tipo, 10, 11, total_size, i+1, payload_sizes[i], 0,0,0,0]
        heads.append(make_head(lista_head))
    packages = []
    for i in range(total_size):
        package = heads[i] + payloads[i]
        packages.append(package)
    return packages

def make_start_package(size, type_):
    lista_head = [type_, 10, 11, size, 0, 0, 0,0,0,0]
    head = make_head(lista_head)
    package = head + b'' + b'\xFF\xAA\xFF\xAA'
    return package




print(crc16(b'\x31\x32\x33\x34\x35\x36\x37\x38\x39'))