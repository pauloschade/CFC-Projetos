import utils
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

    def check_number(self, n):
        assert self.package_number == n , "Wrong Package"

    def set_package(self, tipo):
        self.package =  utils.make_package(tipo, self.index)

    def send_package(self, tipo):
        self.set_package(tipo)
        self.com1.sendData(self.package)

    def read_head(self):
        for i in range(10):
            rx, n = self.com1.getData(1)
            rx_int = int.from_bytes(rx, byteorder='big')

            if i == 0:
                self.type = rx_int

            if i == 2:
                if rx_int == self.id:
                    self.ocioso = True
                else:
                    self.ocioso = False
            
            if i == 3 and self.type == 1:
                self.rx_size = rx_int

            if i == 4:
                self.package_number = rx_int

            if i == 5:
                self.payload_size = rx_int

    def read_eoc(self):
        rx, n = self.com1.getData(4)
        #assert rx == b'\xFF\xAA\xFF\xAA', "EOC not valid"
        if rx != b'\xFF\xAA\xFF\xAA':
            print("EOC not valid")
            self.send_package(6)
            
        elif self.type == 1:
            self.send_package(2)
            self.index += 1
        else:
            self.send_package(4)
            self.index += 1
            self.rx_buffer += self.rx


    def read_package(self):
        self.read_head()
        assert self.ocioso, "not ready to receive"
        self.check_number(self.index)
        self.rx, n = self.com1.getData(self.payload_size)
        self.read_eoc()
        self.com1.rx.clearBuffer()
        if self.index == self.rx_size + 1:
            self.done = True

    
