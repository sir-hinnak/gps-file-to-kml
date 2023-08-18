import sys
import pandas as pd

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget, QFileDialog, QTableWidget, QTableWidgetItem, QGroupBox, QRadioButton, QComboBox, QFormLayout, QLabel, QGridLayout

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GPS-Export to KML")

        self.initUI()
        self.selected_file_path = ""

    def initUI(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QGridLayout(self.central_widget)

        self.text_edit = QTextEdit()
        self.layout.addWidget(self.text_edit, 0, 0, 1, 2)

        self.load_button = QPushButton("Datei öffnen")
        self.load_button.clicked.connect(self.loadFile)
        self.layout.addWidget(self.load_button, 1, 0)

        self.separator_input = QTextEdit()
        self.separator_input.setFixedHeight(35)
        self.separator_input.setPlaceholderText("Separator eingeben")
        self.layout.addWidget(self.separator_input, 1, 1)

        self.render_button = QPushButton("Tabelle rendern")
        self.render_button.clicked.connect(self.renderTable)
        self.layout.addWidget(self.render_button, 2, 0, 1, 2)

        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget, 3, 0, 1, 2)

        self.settings_group = QGroupBox("Einstellung")
        self.settings_layout = QVBoxLayout()

        self.form_layout = QFormLayout()

        self.latitude_label = QLabel("Latitude:")
        self.longitude_label = QLabel("Longitude:")
        self.name_label = QLabel("Name:")
        
        self.latitude_combo = QComboBox()
        self.longitude_combo = QComboBox()
        self.name_combo = QComboBox()
        
        self.form_layout.addRow(self.latitude_label, self.latitude_combo)
        self.form_layout.addRow(self.longitude_label, self.longitude_combo)
        self.form_layout.addRow(self.name_label, self.name_combo)

        self.single_option = QRadioButton("Als Route generieren")
        self.form_layout.addRow(self.single_option)

        self.settings_layout.addLayout(self.form_layout)
        self.settings_group.setLayout(self.settings_layout)
        self.layout.addWidget(self.settings_group, 4, 0, 1, 2)

        self.custom_button = QPushButton("KML generieren")
        self.custom_button.clicked.connect(self.customCode)
        self.layout.addWidget(self.custom_button, 5, 0, 1, 2)

    def loadFile(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Datei öffnen", "", "Textdateien (*.txt);;Alle Dateien (*)", options=options)

        if file_name:
            with open(file_name, "r") as file:
                content = file.read()
                self.text_edit.setPlainText(content)
                self.selected_file_path = file_name  

    def renderTable(self):
        content = self.text_edit.toPlainText()
        self.separator = self.separator_input.toPlainText()

        rows = content.split('\n')
        headers = rows[0].split(self.separator)
        data = rows[1:]

        self.table_widget.clear()
        self.table_widget.setRowCount(len(data))
        self.table_widget.setColumnCount(len(headers))
        self.table_widget.setHorizontalHeaderLabels(headers)

        self.latitude_combo.clear()
        self.longitude_combo.clear()
        self.name_combo.clear()

        self.latitude_combo.addItem("None")
        self.longitude_combo.addItem("None")
        self.name_combo.addItem("None")

        self.latitude_combo.addItems(headers)
        self.longitude_combo.addItems(headers)
        self.name_combo.addItems(headers)

        for row_idx, row in enumerate(data):
            cols = row.split(self.separator)
            for col_idx, col in enumerate(cols):
                item = QTableWidgetItem(col)
                self.table_widget.setItem(row_idx, col_idx, item)

    def customCode(self):
        if self.selected_file_path:
            longitude = self.longitude_combo.currentText()
            latitude = self.latitude_combo.currentText()
            name = self.name_combo.currentText()
            tmp_name = "None"

            if self.single_option.isChecked():
                print(f"Radio Button wurde geklickt! Route generieren ausgewählt. Dateipfad: {self.selected_file_path}, Latitude: {latitude}, Longitude: {longitude}")
            else:
                print(f"Radio Button wurde geklickt! Route generieren nicht ausgewählt. Dateipfad: {self.selected_file_path}, Latitude: {latitude}, Longitude: {longitude}")

            df = pd.read_csv(self.selected_file_path, sep=self.separator) 

            f = open(self.selected_file_path+".kml", "a")
            f.write("""<?xml version="1.0" encoding="UTF-8"?>""")
            f.write("""<kml xmlns="http://www.opengis.net/kml/2.2">\n""")
            f.write("<Document>")
            if self.single_option.isChecked():
                f.write("<Placemark><name>Route</name><description></description><LineString><coordinates>\n")
                for ind in df.index:
                    f.write(str(df[longitude][ind]) + ", " +  str(df[latitude][ind]) + "\n")
                f.write("</coordinates></LineString></Placemark>\n")
            else:
                for ind in df.index:
                    if name != "None":
                        tmp_name = str(df[name][ind])
                    f.write("<Placemark><name>"+ tmp_name +"</name><description></description><Point><coordinates>" + str(df[longitude][ind]) + ", " +  str(df[latitude][ind]) + "</coordinates></Point></Placemark>\n")
            f.write("</Document>")
            f.write("</kml>")
            f.close()                

        else:
            print("Bitte wählen Sie eine Datei aus!")

def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
