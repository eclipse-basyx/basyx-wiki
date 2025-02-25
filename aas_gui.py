import sys
import requests
#from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QMainWindow
from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QMainWindow, QPushButton, QVBoxLayout, QWidget

API_URL = "http://localhost:8080/api/v3.0/shells"  # Server URL

class AASViewer(QMainWindow):
    def __init__(self): #def __init__(self, json_file):
        super().__init__()
        self.setWindowTitle("AAS Viewer")
        self.setGeometry(100, 100, 600, 400)        

        # Create main layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create Refresh Button
        self.refresh_button = QPushButton("Refresh Data", self)
        self.refresh_button.clicked.connect(self.load_aas_data)
        layout.addWidget(self.refresh_button)

        # Create a Tree Widget
        self.tree = QTreeWidget(self)
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabels(["Asset Administration Shell"])
        self.setCentralWidget(self.tree)

        # Load and display AAS data
        self.load_aas_data()
        #self.load_aas_data(json_file)

    def load_aas_data(self):
        try:
            response = requests.get(API_URL)
            aas_data = response.json()

            # Clear existing items
            self.tree.clear()
            
            # Create root node
            root = QTreeWidgetItem(self.tree, ["AAS"])
            self.tree.addTopLevelItem(root)

            # Recursively populate the tree
            self.populate_tree(aas_data, root)
            self.tree.expandAll()

        except Exception as e:
            print(f"Error fetching AAS data: {e}")

    def populate_tree(self, data, parent):
        if isinstance(data, dict):
            for key, value in data.items():
                child = QTreeWidgetItem(parent, [key])
                self.populate_tree(value, child)
        elif isinstance(data, list):
            for idx, item in enumerate(data):
                child = QTreeWidgetItem(parent, [f"Item {idx}"])
                self.populate_tree(item, child)
        else:
            QTreeWidgetItem(parent, [str(data)])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = AASViewer()
    viewer.show()
    sys.exit(app.exec_())    

    