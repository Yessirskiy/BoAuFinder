from PyQt6.QtWidgets import QApplication, QWidget
import sys

app = QApplication([])

window = QWidget()

window.show()
sys.exit(app.exec())

