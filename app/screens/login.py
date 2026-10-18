"""Login screen. Validates against auth.py and opens the main window on success."""
import sys
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QLineEdit, QFormLayout, QHBoxLayout
from PySide6.QtCore import Qt

class loginScreen(QWidget):
    def __init__(self, parent=None):
        super(loginScreen, self).__init__(parent)
        self.setWindowTitle("Login")

        self.emailInput = QLineEdit()
        self.passwordInput = QLineEdit()
        self.passwordInput.setEchoMode(QLineEdit.EchoMode.Password) # Masks the typed password on screen

        self.passwordInput.setPlaceholderText("Example: ")
        self.emailInput.setPlaceholderText("Example: ")
        self.emailInput.setMinimumWidth(300)
        self.passwordInput.setMinimumWidth(300)
        self.emailInput.setMaximumWidth(300)
        self.passwordInput.setMaximumWidth(300)

        loginForm = QFormLayout()
        
        loginForm.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.FieldsStayAtSizeHint) # Stops fields growing beyond their natural size
        loginForm.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows) # Puts each label above its field instead of beside it
        loginForm.addRow("Email", self.emailInput)
        loginForm.addRow("Password", self.passwordInput)

        loginForm.setFormAlignment(Qt.AlignmentFlag.AlignVCenter) # Centers the form vertically

        # Centres the form horizontally using stretchable space on both sides
        outer_layout = QHBoxLayout()
        outer_layout.addStretch(1) # Factor 1 so the stretches take all the spare width. With 0, the form gets a third of the window and sits off-centre
        outer_layout.addLayout(loginForm)  
        outer_layout.addStretch(1)               
        self.setLayout(outer_layout)            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Create and show the form
    window = loginScreen()
    window.showMaximized()
    # Run the main Qt loop
    sys.exit(app.exec())