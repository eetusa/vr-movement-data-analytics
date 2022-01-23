from PyQt5.QtCore import QLine, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QFormLayout, QLineEdit, QVBoxLayout, QDialogButtonBox, QDialog


class LoginDialog(QWidget):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)

        lay = QFormLayout()

        self.okButton = QPushButton("OK")
        self.okButton.clicked.connect(self.clicked)
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.clicked)

        usernameInput = QLineEdit()
        passwordInput = QLineEdit()
        

        lay.addRow("Username", usernameInput)
        lay.addRow("Password", passwordInput)
        #lay.addWidget(self.usernameInput)
        #lay.addWidget(self.passwordInput)   
        lay.addWidget(self.okButton)   
        lay.addWidget(self.cancelButton)
        #lay.addChildLayout(buttons)
        self.setLayout(lay)

class CustomDialog(QDialog):


    def __init__(self, parent = None):
        super(CustomDialog, self).__init__(parent)

        usernamelabel = "Käyttäjätunnus"
        passowordlabel = "Salasana"
        titlelabel = "Sisäänkirjautuminen"

        self.setWindowTitle(titlelabel)

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.usernameInput = QLineEdit()
        self.passwordInput = QLineEdit()
        self.passwordInput.setEchoMode(QLineEdit.Password)

        self.layout = QFormLayout()
        self.layout.addRow(usernamelabel, self.usernameInput)
        self.layout.addRow(passowordlabel, self.passwordInput)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
    
        # static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def getUserPassword(parent = None):
        dialog = CustomDialog(parent)
        result = dialog.exec_()
        username = dialog.usernameInput.text()
        password = dialog.passwordInput.text()
        return (username, password, result == QDialog.Accepted)
