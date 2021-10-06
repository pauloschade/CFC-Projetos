import utils
import time
import datetime
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
        self.sending_type = 1
        self.type = 0
        self.error = False
        self.timer2 = 0
        self.timeout = False
        self.transmission = 1
        self.handshake = True

    def count_timer2(self):
        if self.timer2 > 1.9:
            print("Server is inactive, ending com")
            self.sending_type = 5
            self.log("envio")
            self.done = True
            self.handshake = False
        self.timer2 += 1

    def set_timeout(self):
        self.com1.rx.clearBuffer()
        print(f"resending package{self.index + 1}")
        time.sleep(1)
        self.send_packages()

    def set_start(self):
        self.start_package =  utils.make_start_package(self.total_packages, 1)

    def setup_packages(self):
        self.packages = utils.make_packages(self.buffer, 3)
        self.total_packages = len(self.packages)
        self.set_start()

    def send_start_package(self):
        self.sending_type = 1
        self.com1.sendData(self.start_package)
        self.log("envio")
        time.sleep(0.2)

    def send_packages(self):
        self.sending_type = 3
        if self.error and self.index == 7:
            self.com1.sendData(self.packages[self.index + 4] +  b'\xFF\xAA\xFF\xAB') 
            self.error = False
            self.transmission = 2
        else:
            self.packages[self.index] +=  b'\xFF\xAA\xFF\xAA'
            self.com1.sendData(self.packages[self.index])
        self.log("envio")
        if self.index == self.total_packages - 1:
            self.done = True


    def read_head(self):
        for i in range(10):
            rx, n = self.com1.getData(1)
            if rx == None:
                if not self.handshake:
                    self.timeout = True
                    self.set_timeout()
                    self.transmission = 5
                self.count_timer2()
                break
            else:
                self.handshake = False
                self.timeout = False

                rx_int = int.from_bytes(rx, byteorder='big')

                if i == 0:
                    self.type = rx_int

                if i == 1:
                    assert rx_int == self.id, "Not for me"

                if i == 6 and self.type == 6:
                    self.sending_type = 6
                    self.transmission = 2
                    print("Resend package, received error type 6")
                    
                    self.index = rx_int - 1
                    

    def read_eoc(self):
        rx, n = self.com1.getData(4)
        if rx != b'\xFF\xAA\xFF\xAA':
            self.com1.rx.clearBuffer()
            print("EOC not valid")
            time.sleep(0.05)
        else:
            self.sending_type = self.type
            self.log("recebeu")


    
    def receive_package(self):
        self.sending_type = 4
        self.read_head()
        if not self.timeout:
            self.read_eoc()
            self.com1.rx.clearBuffer()
            if self.type == 4:
                self.index += 1
        else:
            pass


    def log(self, envio):

        time=datetime.datetime.now()

        if self.sending_type == 3:
            s = [time,envio, self.sending_type, len(self.packages[self.index]), self.index + 1, self.total_packages]
        else:
            s = [time,envio, self.sending_type, 14]
        with open(f"Client{4}.txt", "a") as f:
            for i in s:
                f.write(str(i) + " / ")
            f.write("\n")



    


    
