from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtCore import QThread
import serial
import settings
import time
import threading

connected = False

import sys

ser = serial.Serial()

class reciveThread(QThread):
    def run(self):
        time.sleep(1)
        while 1:
            print("ok")



class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('mainwindow.ui', self) # Load the .ui file
        self.exit_button.clicked.connect(self.exit_click)
        self.accept_button.clicked.connect(self.accept_click)
        self.clear_btn.clicked.connect(self.celar_click)
        self.terminal.setReadOnly(True)
        self.settings_button.clicked.connect(self.settings_click)

        t = threading.Thread(target=self.recive)
        t.start()


        self.show() # Show the GUI


    def settings_click(self):

        self.popup = settings.Settings_Form(ser)
        self.popup.show()

    def recive(self):
        while (1):
            try:
                recv = ser.readline()
                print(len(recv))
                a = []
                for x in range(0, len(recv)):
                    a.append(int(str(recv[x])))


                msg = a[3:len(a)]

                hex_msg = []
                id = a[0]
                id0 = chr(a[0])
                id1 = chr(a[1])
                id2 = chr(a[2])

                addr = ""
                addr = str(id0) + str(id1) + str(id2)

                id = int(str(id0))*16*16 + int(str(id1))*16 + int(str(id2));
                print(id)

                for x in range(0, len(msg)):
                    hex_msg.append(hex(msg[x]))

                hex_string = (' '.join(hex_msg))
                hex_string = hex_string.upper()

                if(settings.filtering_enabled == False):
                    self.pusti_id = True
                else:
                    if(settings.filtering_mode == "except"):
                        if(settings.addr_min <= int(id) and settings.addr_max >= int(id)):
                            self.pusti_id = True
                        else:
                            self.pusti_id = False
                    else:
                        if (settings.addr_min >= int(id) and settings.addr_max <= int(id)):
                            self.pusti_id = True
                        else:
                            self.pusti_id = False

                if(self.pusti_id == True):

                    if(settings.encoding == "ASCII"):
                        v = self.terminal.verticalScrollBar().maximum()
                        self.terminal.verticalScrollBar().setValue(v)
                        recv_temp = recv[3:len(recv)]
                        self.terminal.append(str(hex(id)).upper() + ": " + "".join(map(chr, recv_temp)))

                    else:
                        v = self.terminal.verticalScrollBar().maximum()
                        self.terminal.verticalScrollBar().setValue(v)
                        self.terminal.append(str(hex(id)).upper() + ": " + hex_string)










            except:
                pass


    def send_click(self):
        try:
            s = self.send_text.text()
            self.terminal.append("PC: " + s)
            s = s + "\n"
            s = bytes(s, 'utf-8')
            ser.write(s)
            self.send_text.setText("")
        except:
            self.connection_button.setText("FAIL")

    def celar_click(self):
        self.terminal.clear()




    def accept_click(self):
        try:
            global ser
            global connected

            port = self.port_text.text()
            baud = self.baud_text.text()
            baud = int(baud)
            ser = serial.Serial(port, baud, timeout = 0.1)
            connected = True
            self.connection_button.setText("OK")
        except:
            self.connection_button.setText("FAIL");

    def exit_click(self):

        try:
            global ser
            ser.close()
        except:
            pass

        self.close()

if __name__ == "__main__":
    thr = reciveThread()
    thr.start()
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()