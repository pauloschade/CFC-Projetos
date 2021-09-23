import utils
class Client():
    def __init__(self, buffer, com1):
        self.id = 10
        self.packages = []
        self.buffer = buffer
        self.total_packages = None
        self.start_package = b''
        self.com1 = com1
        self.index = 0
        self.done = False
        self.type = 0

    def set_start(self):
        self.start_package =  utils.make_start_package(self.total_packages)

    def setup_packages(self):
        self.packages = utils.make_packages(self.buffer, 3)
        self.total_packages = len(self.packages)
        self.set_start()

    def send_start_package(self):
        self.com1.sendData(self.start_package)

    def send_packages(self):
        self.com1.sendData(self.packages[self.index]) 
        self.index+=1
        if self.index == self.total_packages:
            self.done = True


    def read_head(self):
        for i in range(10):
            rx, n = self.com1.getData(1)
            rx_int = int.from_bytes(rx, byteorder='big')

            if i == 0:
                self.type = rx_int

            if i == 1:
                assert rx_int == self.id, "Not for me"

            if i == 6 and self.type == 5:
                self.index = rx_int

    def read_eoc(self):
        rx, n = self.com1.getData(4)
        assert rx == b'\xFF\xAA\xFF\xAA', "EOC not valid"
    
    def receive_package(self):
        self.read_head()
        self.read_eoc()
        self.com1.rx.clearBuffer()
        
    


    
