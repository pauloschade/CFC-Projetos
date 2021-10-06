import utils
import time
import datetime
class Server():
    def __init__(self, com1):
        self.id = 11
        self.package = b''
        self.com1 = com1
        self.rx_buffer = b''
        self.rx_size = None
        self.payload_size = 0
        self.type = 0
        self.ocioso = False
        self.package_number = 0
        self.done = False
        self.index = 0
        self.rx = b''
        self.timeout = False
        self.transmission=1
        self.sending_type=1
        self.timer2 = 0
        self.handshake=True
        self.crc = None
    
    def check_crc(self):
        if self.type == 3 and self.rx is not None:
            crc_rx = utils.crc16(self.rx)
            if crc_rx != self.crc:
                print("invalid CRC")
                time.sleep(0.05)
                self.send_error()



    def count_timer2(self):
        if self.timer2 > 3:
            self.sending_type=5
            self.send_package(5)
            print("Client is inactive, ending com")
            self.done = True
        self.timer2 += 1

    def send_error(self):
        self.send_package(6)

    def check_number(self, n):
        if self.package_number != n:
            print("Wrong Package")
            self.transmission=2
            self.sending_type=6
            self.send_error()
            time.sleep(2)


    def set_timeout(self):
        self.timeout = True
        self.com1.rx.clearBuffer()
        print("server None")
        print(f"waiting for package{self.index}")
        time.sleep(2)



    def set_package(self, tipo):
        self.package =  utils.make_package(tipo, self.index)

    def send_package(self, tipo):
        self.sending_type = tipo
        self.set_package(tipo)
        self.com1.sendData(self.package)
        self.log("envio")

    def read_head(self):
        for i in range(10):
            rx, n = self.com1.getData(1)

            if rx == None:
                self.set_timeout()
                self.count_timer2()
                break

            else:
                self.handshake = False
                self.transmission=1
                self.timeout = False
                rx_int = int.from_bytes(rx, byteorder='big')

                if i == 0:
                    self.type = rx_int
                
                if i == 3 and self.type == 1:
                    self.rx_size = rx_int

                if i == 4:
                    self.package_number = rx_int

                if i == 5:
                    self.payload_size = rx_int

                if i == 8:
                    self.crc = rx
                if i == 9:
                    self.crc += rx
                    self.crc = int.from_bytes(self.crc, byteorder='big')

    def read_eoc(self):
        time.sleep(0.005)
        rx, n = self.com1.getData(4)
        if rx != b'\xFF\xAA\xFF\xAA':
            print("EOC not valid")
            print(rx)
            self.transmission=2
            self.sending_type = 6
            time.sleep(1)
            self.com1.rx.clearBuffer()
            self.send_error()
            
        elif self.type == 1:
            self.log("recebeu")
            self.send_package(2)
            self.index += 1
        else:
            self.log("recebeu")
            self.send_package(4)
            self.index += 1
            self.rx_buffer += self.rx


    def read_package(self):
        self.read_head()
        if not self.done:
            if self.handshake:
                self.send_package(2)
                pass
            else:
                if not self.timeout:
                    self.check_number(self.index)
                    self.sending_type = self.type
                    self.rx, n = self.com1.getData(self.payload_size)
                    time.sleep(0.01)
                    self.check_crc()
                    self.read_eoc()
                    self.com1.rx.clearBuffer()
                    if self.index == self.rx_size + 1:
                        self.done = True
                    
                else:
                    pass

    def log(self, envio):
        time=datetime.datetime.now()
        if envio == "recebeu":
            s = [time,envio, self.sending_type, 14, self.crc]
        else:
            s = [time,envio, self.sending_type, 14]
        with open(f"Server{5}.txt", "a") as f:
            for i in s:
                f.write(str(i) + " / ")
            f.write("\n")

