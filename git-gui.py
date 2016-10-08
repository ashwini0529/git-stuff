#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

def window():
    def msgbtn():
        print nm.text()
    def enterPress():
        print nm.text()

    app = QApplication(sys.argv)
    win = QWidget()

    l1 = QLabel("Github Username")
    nm = QLineEdit()
    nm.editingFinished.connect(enterPress)

    l2 = QLabel("Repository")
    add1 = QLineEdit()

    fbox = QFormLayout()
    fbox.addRow(l1,nm)
    vbox = QVBoxLayout()

    vbox.addWidget(add1)
    fbox.addRow(l2,vbox)
    submitButton = QPushButton("Submit")
    cancelButton = QPushButton("Cancel")
    fbox.addRow(submitButton,cancelButton)
    submitButton.clicked.connect(msgbtn)

    win.setLayout(fbox)
   
    win.setWindowTitle("Github GUI")
    win.show()
    sys.exit(app.exec_())


def msgbtn(i):
   print i.text()
def textchanged(text):
   print "contents of text box: "+text
if __name__ == '__main__':
   window()