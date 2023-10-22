import sys
import pymysql
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem, QFrame, QHeaderView

class OrderAnalyzerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Orders Analyzer")
        self.setGeometry(100, 100, 600, 400)

        self.analyze_button = QPushButton("Analyze Orders")
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.MultiSelection)  
        self.table.setHorizontalHeaderLabels(["Name", "Surname", "Email", "Order Count"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.horizontalHeader().setHighlightSections(False)
        
        frame = QFrame(self)  # Tworzenie pojemnika na elementy
        frame.setLayout(QVBoxLayout())  # Ustawienie układu w pojemniku
        frame.layout().addWidget(self.analyze_button)
        frame.layout().addWidget(self.table)
        
        layout = QVBoxLayout(self)
        layout.addWidget(frame)  # Dodanie pojemnika do układu głównego
        self.setLayout(layout)

        self.analyze_button.clicked.connect(self.analyze_orders)

    
    def analyze_orders(self):
        self.analyze_button.setEnabled(False)
        
        # Logika analizy zamówień
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='',  # Podaj hasło do swojej bazy danych
            db='wypiekarnia'  # Zmień na nazwę Twojej bazy danych
        )
        try:
            with conn.cursor() as cursor:
                # Pobierz informacje o użytkownikach (imie, nazwisko, email)
                cursor.execute("SELECT name, surname, email FROM klijeci")
                users = cursor.fetchall()
                results = []

                for user in users:
                    imie, nazwisko, email = user
                    cursor.execute(
                        "SELECT COUNT(id) FROM zamowienia WHERE email = %s", (email,))
                    total_orders = cursor.fetchone()[0]
                    results.append([imie, nazwisko, email, total_orders])

                # Wyczyść tabelę przed dodaniem nowych wyników
                self.table.setRowCount(0)
                
                # Wypełnij tabelę nowymi wynikami
                for row, data in enumerate(results):
                    self.table.insertRow(row)
                    for col, item in enumerate(data):
                        item = QTableWidgetItem(str(item))  # Dodaj przecinek
                        item.setFlags(item.flags() ^ Qt.ItemIsEditable)  # Wyłącz edycję
                        self.table.setItem(row, col, item)

        except Exception as e:
            print(f"Błąd podczas analizy: {str(e)}")
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
