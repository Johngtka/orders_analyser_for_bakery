import sys
import pymysql
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem, QFrame, QHeaderView, QLabel

class OrderAnalyzerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Orders Analyzer")
        self.setGeometry(100, 100, 600, 400)

        self.analyze_button = QPushButton("Daily Report")
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.MultiSelection)  
        self.table.setHorizontalHeaderLabels(["Name", "Surname", "Login", "Order Count"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.horizontalHeader().setHighlightSections(False)

        frame = QFrame(self)
        frame_layout = QVBoxLayout()
        frame_layout.addWidget(self.analyze_button)
        frame_layout.addWidget(self.table)
        frame.setLayout(frame_layout)
        
        self.loading_label = QLabel(self)
        self.loading_movie = QMovie("giphy.gif")  
        self.loading_label.setMovie(self.loading_movie)
        self.loading_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout(self)
        layout.addWidget(frame)
        layout.addWidget(self.loading_label)
        self.setLayout(layout)

        self.analyze_button.clicked.connect(self.analyze_orders)

    def analyze_orders(self):
        self.analyze_button.setEnabled(False)
        self.loading_movie.start()
        QTimer.singleShot(3000, self.process_data)

    def process_data(self):
        self.loading_movie.stop()
        self.loading_label.clear()

        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            db='wypiekarnia'
        )
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT name, surname, login FROM klijeci")
                users = cursor.fetchall()
                results = []

                for user in users:
                    name, surName, login = user
                    cursor.execute(
                        "SELECT COUNT(id) FROM zamowienia WHERE userLogin = %s", (login,))
                    total_orders = cursor.fetchone()[0]
                    results.append([name, surName, login, total_orders])

                self.table.setRowCount(0)

                for row, data in enumerate(results):
                    self.table.insertRow(row)
                    for col, item in enumerate(data):
                        item = QTableWidgetItem(str(item))
                        item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                        self.table.setItem(row, col, item)

        except Exception as e:
            print(f"An error has been ocurred while orders analyzing: {str(e)}")
        finally:
            conn.close()
        
        self.analyze_button.setEnabled(True)

def main():
    app = QApplication(sys.argv)
    window = OrderAnalyzerApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
