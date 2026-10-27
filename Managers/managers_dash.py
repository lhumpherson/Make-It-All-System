from datetime import datetime
import sys
import matplotlib.pyplot as plt
import numpy as np
from PySide6 import QtCore, QtGui, QtWidgets


class managersDashboard(QtWidgets.QWidget):

  def __init__(self):
    super().__init__()

    self.title = QtWidgets.QLabel(
        "Choose a project to see it's task delegation and progession and assign tasks",
        alignment=QtCore.Qt.AlignCenter,
    )
    

    self.projectSearch = QtWidgets.QComboBox()
    self.projectSearch.setPlaceholderText("Project:")
    self.projectSearch.addItems([
        "Project 1",
        "Project 3",
        "Project 4"
    ])
    self.projectSearch.setEditable(True)

    self.projectSearch.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
    self.submitProject = QtWidgets.QPushButton("Submit")
    self.submitProject.setStyleSheet("background-color: #f5a623; color: #1e1e1e")

    self.taskButton = QtWidgets.QPushButton("Assign Tasks")
    


    self.outputTask = QtWidgets.QWidget()
    self.outputLayout = QtWidgets.QVBoxLayout(self.outputTask)



    self.mainLayout = QtWidgets.QVBoxLayout(self)
    self.mainLayout.setAlignment(QtCore.Qt.AlignTop)
    self.mainLayout.setSpacing(10)

    
    self.searchRowLayout = QtWidgets.QHBoxLayout()
    self.searchRowLayout.addWidget(QtWidgets.QLabel("Project:"))
    self.searchRowLayout.addWidget(self.projectSearch, 1)

    
    self.taskButton.hide()

    
    self.mainLayout.addWidget(self.title)
    self.mainLayout.addLayout(self.searchRowLayout)
    self.mainLayout.addWidget(self.submitProject)
    self.mainLayout.addWidget(self.outputTask)
    self.mainLayout.addWidget(self.taskButton)   

    self.submitProject.clicked.connect(self.submitClicked)
    self.taskButton.clicked.connect(self.assignTaskButton)

  def clearOutput(self):
    while self.outputLayout.count():
      child = self.outputLayout.takeAt(0)
      if child.widget():
        child.widget().deleteLater()

  
  @QtCore.Slot()
  def submitClicked(self):
    self.clearOutput()
    self.taskButton.hide()
    try:
      delegationFile = open("projectDelegation.txt", "r").readlines()
    except FileNotFoundError:
      self.outputLayout.addWidget(
          QtWidgets.QLabel("Error: projectDelegation.txt not found.")
      )
      return

    statEmployee1 = 0
    statEmployee2 = 0
    statEmployee3 = 0
    statEmployee4 = 0
    statEmployee5 = 0
    searchVal = self.projectSearch.currentText()

    if searchVal == "":
      self.outputLayout.addWidget(QtWidgets.QLabel("Please enter a search"))
    else:
      for line in delegationFile[1:]:
        cleanline = line.strip()
        delegationRecord = cleanline.split(",")
        if len(delegationRecord) > 3:
          if delegationRecord[0] == searchVal:
            employee = delegationRecord[1]
            if employee==("Alice"):
              statEmployee1 += 1
            elif employee==("Bert"):
              statEmployee2 += 1
            elif employee==("Clara"):
              statEmployee3 += 1
            elif employee==("Dilip"):
              statEmployee4 += 1
            elif employee==("Emma"):
              statEmployee5 += 1

      employee = ["Alice", "Bert", "Clara", "Dilip","Emma"]
      counts = [statEmployee1, statEmployee2, statEmployee3, statEmployee4, statEmployee5]

      
      if sum(counts) == 0:
        self.outputLayout.addWidget(QtWidgets.QLabel(f"No employee tasks found for {searchVal}."))
        return

      plt.figure(figsize=(5, 4))
      colours = ['#f5a623', "#e5e5e5", "#ffb84d", "#A1A1A1","#555555"]
      plt.pie(counts, labels=employee, autopct="%1.1f%%", colors=colours)
      plt.title(f"Task Delegation for {searchVal}")
      plt.savefig("DelegationStat.png")
      plt.close()

      img_label = QtWidgets.QLabel()
      pixmap = QtGui.QPixmap("DelegationStat.png")
      img_label.setPixmap(
          pixmap.scaled(
              400,
              400,
              QtCore.Qt.KeepAspectRatio,
              QtCore.Qt.SmoothTransformation,
          )
      )
      self.outputLayout.addWidget(img_label, alignment=QtCore.Qt.AlignCenter)
      self.taskButton.show()

  @QtCore.Slot()
  def assignTaskButton(self):
    self.formContainer = QtWidgets.QWidget()
    self.formContainer.setStyleSheet("background-color: #f2f2f2; border-radius: 5px; padding: 10px;")
    formLayout = QtWidgets.QVBoxLayout(self.formContainer)
    formLayout.addWidget(QtWidgets.QLabel("Assign tasks for " + self.projectSearch.currentText()),alignment=QtCore.Qt.AlignCenter)

    empRowLayout = QtWidgets.QHBoxLayout()
    self.employeeNameLabel = QtWidgets.QLabel(("Employee Name:"))
    self.employeeName = QtWidgets.QLineEdit()
    self.employeeName.setPlaceholderText("Enter name here")
    self.employeeName.setStyleSheet("background-color: #ffffff; border: 1px solid #b0b0b0; border-radius: 4px; padding: 5px;")
    empRowLayout.addWidget(self.employeeNameLabel)
    empRowLayout.addWidget(self.employeeName, 1)
    formLayout.addLayout(empRowLayout)

    taskRowLayout = QtWidgets.QHBoxLayout()
    self.taskDescriptionLabel = QtWidgets.QLabel(("Task Description:"))
    self.taskDescription = QtWidgets.QLineEdit()
    self.taskDescription.setPlaceholderText("Enter description here")
    self.taskDescription.setStyleSheet("background-color: #ffffff; border: 1px solid #b0b0b0; border-radius: 4px; padding: 5px;")
    taskRowLayout.addWidget(self.taskDescriptionLabel)
    taskRowLayout.addWidget(self.taskDescription, 1)
    formLayout.addLayout(taskRowLayout)
    

    self.taskSubmit = QtWidgets.QPushButton("Submit Task")
    self.taskSubmit.setStyleSheet("background-color: #555555; color: #ffffff; padding: 6px; border-radius: 4px;")
    formLayout.addWidget(self.taskSubmit)
    self.outputLayout.addWidget(self.formContainer)

    self.taskSubmit.clicked.connect(self.saveTaskClicked)


  @QtCore.Slot()
  def saveTaskClicked(self):
    employeeFile = open("employee.txt","r")
    found = False
    for line in employeeFile:
        cleanline = line.strip()
        record = cleanline.split(",")
        if len(record) >=2  :
          if record [0] == self.employeeName.text():
            found = True
            break
    employeeFile.close()
    if found == False:
      self.outputLayout.addWidget(QtWidgets.QLabel("This employee hasn't been found"))
      self.employeeName.clear()

    if found == True:
      delegationFile = open("projectDelegation.txt","a")
      new_line = f"{self.projectSearch.currentText()},{self.employeeName.text()},{self.taskDescription.text()},{"In Progress"}\n"
      delegationFile.write(new_line)
      self.outputLayout.addWidget(QtWidgets.QLabel("The task was sucessfully added to the employees to-do list"))
      self.employeeName.clear()
      self.taskDescription.clear()
      delegationFile.close()
    
    


if __name__ == "__main__":
  app = QtWidgets.QApplication(sys.argv)
  widget = managersDashboard()
  widget.resize(800, 700)
  widget.show()
  sys.exit(app.exec())