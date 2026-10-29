"""Registration screen. Staff email only, strong password, one account per email."""
import sys
from PySide6.QtWidgets import QApplication, QFrame, QWidget, QLineEdit, QFormLayout, QHBoxLayout, QPushButton, QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, Signal
from pathlib import Path
from app.screens.login import LoginScreen # This line should be move to main.py when merged with rest of code

class RegisterScreen(QWidget):
    joinRequested = Signal()

    def __init__(self, parent=None):
        super(RegisterScreen, self).__init__(parent)
        self.setWindowTitle("Register")
        self.setObjectName("registerScreen")

        PADDING = 32
        FIELD_WIDTH = 300 
        BOX_WIDTH = FIELD_WIDTH + (2 * PADDING)

        # Creating email and password inputs
        self.emailInput = QLineEdit()
        self.passwordInput = QLineEdit()
        self.passwordInput.setEchoMode(QLineEdit.EchoMode.Password) # Masks the typed password on screen

        self.emailInput.setObjectName("emailInput")
        self.passwordInput.setObjectName("passwordInput")

        self.passwordInput.setPlaceholderText("Password")
        self.emailInput.setPlaceholderText("@make-it-all.co.uk")
        self.emailInput.setMinimumWidth(300)
        self.passwordInput.setMinimumWidth(300)
        self.emailInput.setMaximumWidth(300)
        self.passwordInput.setMaximumWidth(300)

        self.confirmPasswordInput = QLineEdit()
        self.confirmPasswordInput.setObjectName("confirmPasswordInput")
        self.confirmPasswordInput.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirmPasswordInput.setPlaceholderText("Re-enter password")
        self.confirmPasswordInput.setMinimumWidth(300)
        self.confirmPasswordInput.setMaximumWidth(300)

        self.passwordHint = QLabel("At least 12 characters")
        self.passwordHint.setObjectName("hintLabel")
        self.passwordHint.setWordWrap(True)

        # Error message, empty until a check fails
        self.errorLabel = QLabel("")
        self.errorLabel.setObjectName("errorLabel")
        self.errorLabel.setWordWrap(True)

        self.loginLink = QPushButton("Already have an account? Login here")
        self.loginLink.setObjectName("linkButton")                    
        self.loginLink.setFlat(True)                                  # no button background
        self.loginLink.setCursor(Qt.CursorShape.PointingHandCursor)   # hand cursor on hover
        self.loginLink.clicked.connect(self.joinRequested.emit)      

        # Creating the register box and register button
        registerForm = QFormLayout()
        registerBox = QFrame()
        registerBox.setObjectName("registerBox")

        self.registerButton = QPushButton("Register")
        self.registerButton.setObjectName("registerButton")
        self.registerButton.setMinimumWidth(300)
        self.registerButton.setMaximumWidth(300)
        self.registerButton.clicked.connect(self.handleRegister)
        self.emailInput.returnPressed.connect(self.handleRegister)
        self.passwordInput.returnPressed.connect(self.handleRegister)

        # Adding the image
        logoPath = Path(__file__).resolve().parent.parent / "assets" / "Make-it-All-Logo.png"
        logo = QPixmap(str(logoPath)).scaledToWidth(
            BOX_WIDTH, Qt.TransformationMode.SmoothTransformation)
        self.logoLabel = QLabel()
        self.logoLabel.setPixmap(logo)
        self.logoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Creating the register form box
        registerForm.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.FieldsStayAtSizeHint) # Stops fields growing beyond their size
        registerForm.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows) # Puts each label above its field instead of beside it
        registerForm.setContentsMargins(PADDING, 24, PADDING, PADDING)
        registerForm.addRow("Email", self.emailInput)
        registerForm.addRow("Password", self.passwordInput)
        registerForm.addRow(self.passwordHint)                
        registerForm.addRow("Confirm password", self.confirmPasswordInput)
        registerForm.addRow(self.errorLabel)              
        registerForm.addRow(self.registerButton)
        registerForm.addRow(self.loginLink)

        # Styles the inside of the register box
        boxLayout = QVBoxLayout()
        boxLayout.setContentsMargins(0, 0, 0, 0) 
        boxLayout.setSpacing(0)
        boxLayout.addWidget(self.logoLabel)       
        boxLayout.addLayout(registerForm) 
        registerBox.setLayout(boxLayout)

        # Centres the register box
        outer_layout = QHBoxLayout()
        outer_layout.addStretch(1) # Factor 1 so the stretches take all the spare width. With 0, the box gets a third of the window and sits off-centre
        outer_layout.addWidget(registerBox, alignment=Qt.AlignmentFlag.AlignVCenter)
        outer_layout.addStretch(1)               
        self.setLayout(outer_layout)
        
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True) # Sets background colour from styles.qss

    def handleRegister(self):
        # this function loads the login page
        print(self.emailInput.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet((Path(__file__).resolve().parent.parent / "styles.qss").read_text())
    # Create and show the form
    window = RegisterScreen()
    window.showMaximized()
    # Run the main Qt loop

    def openLogin():
        window.loginScreen = LoginScreen()  
        window.loginScreen.showMaximized()
        window.hide()

    window.joinRequested.connect(openLogin)
    

    sys.exit(app.exec())