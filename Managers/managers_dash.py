import sys
import matplotlib.pyplot as plt
from PySide6 import QtCore, QtGui, QtWidgets

"""
the main dashboard class with functions inside which are called when buttons are pressed
"""
class managersDashboard(QtWidgets.QWidget):

  """
  this function has all the initial layout of the page when you first selct a project
  """
  def __init__(self):
    super().__init__()

    #title label 
    #Zoe is an example, Managers name will be replaced with what manager is logged into the system when it is hard coded
    self.title = QtWidgets.QLabel(
        "Zoe, choose one of your projects to manage. \nYou can view task delegation, progession, assign tasks and appoint Team Leaders, or create a new Project.",
        alignment=QtCore.Qt.AlignCenter,
    )
    
    #drop down option or type in text box to choose the project
    self.projectSearch = QtWidgets.QComboBox()
    self.projectSearch.setPlaceholderText("Project:")
    #opens the project files used for seeing what project this manager manages  
    try:
      managerFile = open("projectManager.txt", "r").readlines()
    except FileNotFoundError:
      self.outputLayout.addWidget(
          QtWidgets.QLabel("Error: projectManager.txt not found.")
      )
      return
    #if there is a project that the manager manages then it will be added to an array which will be then displayed in the dropdown list  
    projectList = [] 
    for line in managerFile[1:]:
        cleanline = line.strip()
        managerRecord = cleanline.split(",")
        if len(managerRecord) > 3:
          if managerRecord[1] == "Zoe":
            projectList.append(managerRecord[0]) 
    #adds the array to the drop down and now the widget can be displayed correctly 
    self.projectSearch.addItems(projectList)
    self.projectSearch.setEditable(True)
    self.projectSearch.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

    #submit button
    self.submitProject = QtWidgets.QPushButton("Submit")
    self.submitProject.setStyleSheet("background-color: #f5a623; color: #1e1e1e; border-radius: 6px; padding: 6px 12px")
    
    #create a new project button
    self.createProject = QtWidgets.QPushButton("Create Project")
    self.createProject.setStyleSheet("background-color: #e5e5e5; color: #1e1e1e; border-radius: 6px; padding: 6px 12px")

    #assign task button but it appears later when the submit button is pressed 
    self.assignTask = QtWidgets.QPushButton("Assign Tasks")
    self.assignTask.setStyleSheet("background-color: #A1A1A1; color: #1e1e1e; border-radius: 6px; padding: 6px 12px")
    self.assignTask.hide()

    #manage project button it appears later when the submit button is pressed 
    self.manageProject = QtWidgets.QPushButton("Manage this project")
    self.manageProject.setStyleSheet("background-color: #e5e5e5; color: #1e1e1e; border-radius: 6px; padding: 6px 12px")
    self.manageProject.hide()
    
    #a box for the pie chart to go into
    self.outputTaskDelegation = QtWidgets.QWidget()
    self.outputLayout = QtWidgets.QVBoxLayout(self.outputTaskDelegation)

    #setting the main layout
    self.mainLayout = QtWidgets.QVBoxLayout(self)
    self.mainLayout.setAlignment(QtCore.Qt.AlignTop)
    self.mainLayout.setSpacing(10)

    #the text next to the dropdown box to give it context
    self.searchRowLayout = QtWidgets.QHBoxLayout()
    self.searchRowLayout.addWidget(QtWidgets.QLabel("Project:"))
    self.searchRowLayout.addWidget(self.projectSearch, 1)
    
    #layout all the widgets in the right place on the page 
    self.mainLayout.addWidget(self.title)
    self.mainLayout.addLayout(self.searchRowLayout)
    self.mainLayout.addWidget(self.submitProject)
    self.mainLayout.addWidget(self.createProject)
    self.mainLayout.addWidget(self.outputTaskDelegation) 
    self.mainLayout.addWidget(self.assignTask)   
    self.mainLayout.addWidget(self.manageProject)

    #calling the functions when the specific button is pressed 
    self.submitProject.clicked.connect(self.submitClicked)
    self.createProject.clicked.connect(self.createClicked)
    self.assignTask.clicked.connect(self.assignClicked)
    self.manageProject.clicked.connect(self.manageClicked)


  """
  function which clears the outputs wehn you re press the submit button 
  """
  def clearOutput(self):
    while self.outputLayout.count():
      child = self.outputLayout.takeAt(0)
      if child.widget():
        child.widget().deleteLater()


  """
  Function which is called when you press the submit button after choosing the project 
  it creates the pie chart with the info in the text file
  """
  @QtCore.Slot()
  def submitClicked(self):
    #clears any other pie chart which is already there 
    self.clearOutput()

    #opens the project files used for the pie chart 
    try:
      delegationFile = open("projectDelegation.txt", "r").readlines()
    except FileNotFoundError:
      self.outputLayout.addWidget(
          QtWidgets.QLabel("Error: projectDelegation.txt not found.")
      )
      return

    #running variables to update how big the pie chart slices need to be
    #in the hardcoded verion this will not be the case as we dont know how many employees there will be from signing up so it will need to be an array
    statEmployee1 = 0
    statEmployee2 = 0
    statEmployee3 = 0
    statEmployee4 = 0
    statEmployee5 = 0
    positiveProgress = 0
    overallProgress = 0
    #gets the project which has been inputted 
    searchVal = self.projectSearch.currentText()

    #ensures there is a something in the project search bar 
    if searchVal == "":
      self.outputLayout.addWidget(QtWidgets.QLabel("Please enter a search"))
    
    #if there is a project then it can split up the file and every time it reads the employees it can add a task to their running total
    #for that project as well it will check its completion status and add it to a running total
    else:
      for line in delegationFile[1:]:
        cleanline = line.strip()
        delegationRecord = cleanline.split(",")
        if len(delegationRecord) > 3:
          if delegationRecord[0] == searchVal:
            employee = delegationRecord[1]
            status = delegationRecord [3]
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
            if status == ("Complete"):
              positiveProgress += 1
              overallProgress +=1
            elif status == ("In Progress"):
              overallProgress +=1

      #creates counts of how many tasks employees have by getting the employee variables 
      employee = ["Alice", "Bert", "Clara", "Dilip","Emma"]
      counts = [statEmployee1, statEmployee2, statEmployee3, statEmployee4, statEmployee5]
      

      #if there are no tasks assigned to anyone then there will be no pie charts just this message 
      if sum(counts) == 0:
        self.outputLayout.addWidget(QtWidgets.QLabel(f"No employee tasks found for {searchVal}."))
        self.assignTask.show()
        self.manageProject.show()
        return
      

      #creating a pie chart with the data from count and using a specific colour scheme and a title
      #then it saves it as a file which can be accessed later 
      plt.figure(figsize=(5, 4))
      colours = ['#f5a623', "#e5e5e5", "#ffb84d", "#A1A1A1","#555555"]
      plt.pie(counts, labels=employee, autopct="%1.1f%%", colors=colours)
      plt.title(f"Task Delegation for {searchVal}")
      plt.savefig("DelegationStat.png")
      plt.close()

      #puts the pie chart file into a box so that it can be dislplayed as the file that was created earlier
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
      
      #creates the percentage to show in the progress bar if there are tasks assigned to that project 
      if overallProgress > 0:
        progressPercentage = int ((positiveProgress / overallProgress)*100)
      else:
        progressPercentage = 0

      #creating the progress bar with the information from the variables 
      progressBar = QtWidgets.QProgressBar()
      progressBar.setRange(0, 100)
      progressBar.setValue(progressPercentage)
      

      #adding the widgets to the layout and also showing the assign button after it was hidden 
      self.outputLayout.addWidget(img_label, alignment=QtCore.Qt.AlignCenter)
      self.outputLayout.addWidget(QtWidgets.QLabel(f"Project Progress ({positiveProgress}/{overallProgress} tasks completed):"))
      self.outputLayout.addWidget(progressBar)
      self.assignTask.show()
      self.manageProject.show()

  """
  this function is called when a manager clicks on the assign task button 
  it gives you all the boxes to fill in to put a task on the file 
  """
  @QtCore.Slot()
  def assignClicked(self):
    #clears any other pie chart which is already there 
    self.clearOutput()
    #this creates a grey box for the assign task boxes to go into
    self.formContainer = QtWidgets.QWidget()
    self.formContainer.setStyleSheet("background-color: #f2f2f2; border-radius: 5px; padding: 10px;")
    formLayout = QtWidgets.QVBoxLayout(self.formContainer)
    #text to ensure that he user knows the assigning tasks ar for the project they selected 
    formLayout.addWidget(QtWidgets.QLabel("Assign tasks for " + self.projectSearch.currentText()+"\nAll entrys with a * need to contain values "),alignment=QtCore.Qt.AlignCenter)

    #employee info filling in data area
    empRowLayout = QtWidgets.QHBoxLayout()
    self.employeeNameLabel = QtWidgets.QLabel(("*Employee Name:"))
    self.employeeName = QtWidgets.QLineEdit()
    self.employeeName.setPlaceholderText("Enter name here")
    self.employeeName.setStyleSheet("background-color: #ffffff; border: 1px solid #b0b0b0; border-radius: 4px; padding: 5px;")
    empRowLayout.addWidget(self.employeeNameLabel)
    empRowLayout.addWidget(self.employeeName, 1)
    formLayout.addLayout(empRowLayout)

    #task description filling in data area
    taskRowLayout = QtWidgets.QHBoxLayout()
    self.taskDescriptionLabel = QtWidgets.QLabel(("*Task Description:"))
    self.taskDescription = QtWidgets.QLineEdit()
    self.taskDescription.setPlaceholderText("Enter description here")
    self.taskDescription.setStyleSheet("background-color: #ffffff; border: 1px solid #b0b0b0; border-radius: 4px; padding: 5px;")
    taskRowLayout.addWidget(self.taskDescriptionLabel)
    taskRowLayout.addWidget(self.taskDescription, 1)
    formLayout.addLayout(taskRowLayout)
    
    #submit button so the task can update on the file
    self.taskSubmit = QtWidgets.QPushButton("Submit Task")
    self.taskSubmit.setStyleSheet("background-color: #555555; color: #ffffff; padding: 6px; border-radius: 4px;")
    formLayout.addWidget(self.taskSubmit)
    self.outputLayout.addWidget(self.formContainer)

    #when the submit button is clicked it calls this function 
    self.taskSubmit.clicked.connect(self.taskSubmitClicked)


  """
  This function lets the task that the manager inputs be saved on a file so employees to do lists will be updated 
  it opens the file and updates it while making sure essential values are filled in 
  """
  @QtCore.Slot()
  def taskSubmitClicked(self):
    #checks values have not been left blank
    if self.employeeName.text().strip()=="":
      self.outputLayout.addWidget(QtWidgets.QLabel("Please enter an employee"))
      self.employeeName.clear()
      return
    if self.taskDescription.text().strip()=="":
      self.outputLayout.addWidget(QtWidgets.QLabel("Please enter a description"))
      self.taskDescription.clear()
      return
    
    #opens the file and sets a varaible for if the employee exists 
    managerFile = open("projectManager.txt","r")
    found = False
    #finds the inputted employee and checks if they are in the project
    for line in managerFile:
        cleanline = line.strip()
        record = cleanline.split(",")
        if len(record) >=4  :
          projectEmployees = record[3].split(":")
          if self.employeeName.text() in projectEmployees:
            found = True
            break
    managerFile.close()
    
    #if the employee hasnt been found then the text box is cleared and a message is given 
    if found == False:
      self.outputLayout.addWidget(QtWidgets.QLabel("This employee isnt assigned to this project"))
      self.employeeName.clear()
    
    #if the name has been found, then the task can be added to the delegation file safely 
    if found == True:
      delegationFile = open("projectDelegation.txt","a")
      #inputs a new line of data onto the file which takes the data from the text boxes the user has submitted 
      new_line = f"{self.projectSearch.currentText()},{self.employeeName.text()},{self.taskDescription.text()},{"In Progress"}\n"
      delegationFile.write(new_line)
      self.outputLayout.addWidget(QtWidgets.QLabel("The task was sucessfully added to the employees to-do list"))
      #clears the boxes ready for a new task 
      self.employeeName.clear()
      self.taskDescription.clear() 
      delegationFile.close()


  """
  this function is lets the manager manage the teams and the project  
  it gives you all the boxes to fill in so you can assign team leaders and remove and add employees to projects 
  """
  @QtCore.Slot()
  def manageClicked(self):
    #clears any task input which is already there 
    self.clearOutput()
    #this creates a grey box for the assign task boxes to go into
    self.formContainer = QtWidgets.QWidget()
    self.formContainer.setStyleSheet("background-color: #f2f2f2; border-radius: 5px; padding: 10px;")
    formLayout = QtWidgets.QVBoxLayout(self.formContainer)

    #finding the team leader and mebers so the manager can see the current project info before chnaging the team leader 
    managerFile = open("projectManager.txt","r")
    teamLeader = "None"
    employeeList = []
    #finds the project then finds the relevant employees
    for line in managerFile:
        cleanline = line.strip()
        record = cleanline.split(",")
        if len(record) >=4  :
          if record[0]== self.projectSearch.currentText().strip():
            teamLeader = record[2]
            employeeList = record[3].split(":")
            break

    #putting the List into a tring so then it can be outputted later 
    teamMembers = ", ".join(employeeList) if employeeList else "None" 
    managerFile.close()
    #text to ensure that the user knows which project they are managing and the current info about it  
    formLayout.addWidget(QtWidgets.QLabel("<b>Managing project " + self.projectSearch.currentText()+"</b>"),alignment=QtCore.Qt.AlignCenter)
    formLayout.addWidget(QtWidgets.QLabel("Current Team Leader: "+teamLeader+ " \nCurrent Team Members: "+teamMembers),alignment=QtCore.Qt.AlignCenter)

    #team leader filling in data area
    empRowLayout = QtWidgets.QHBoxLayout()
    self.teamLeaderLabel = QtWidgets.QLabel(("Assign a team leader:"))
    self.teamLeader = QtWidgets.QLineEdit()
    self.teamLeader.setPlaceholderText("Enter name here")
    self.teamLeader.setStyleSheet("background-color: #ffffff; border: 1px solid #b0b0b0; border-radius: 4px; padding: 5px;")
    

    #submit button so the task can update on the file
    self.teamLeaderSubmit = QtWidgets.QPushButton("Submit")
    self.teamLeaderSubmit.setStyleSheet("background-color: #555555; color: #ffffff; padding: 6px; border-radius: 4px;")
    

    empRowLayout.addWidget(self.teamLeaderLabel)
    empRowLayout.addWidget(self.teamLeader, 1)
    empRowLayout.addWidget(self.teamLeaderSubmit)
    formLayout.addLayout(empRowLayout)
    #when the submit button is clicked it calls this function 
    self.teamLeaderSubmit.clicked.connect(self.teamLeaderClicked)

    #add employees to this team 
    taskRowLayout = QtWidgets.QHBoxLayout()
    self.addEmployeeLabel = QtWidgets.QLabel(("Add an employee to this project:"))
    self.addEmployee = QtWidgets.QLineEdit()
    self.addEmployee.setPlaceholderText("Enter name here")
    self.addEmployee.setStyleSheet("background-color: #ffffff; border: 1px solid #b0b0b0; border-radius: 4px; padding: 5px;")
    

    #submit button so the task can update on the file
    self.addSubmit = QtWidgets.QPushButton("Submit")
    self.addSubmit.setStyleSheet("background-color: #555555; color: #ffffff; padding: 6px; border-radius: 4px;")
    
    
    taskRowLayout.addWidget(self.addEmployeeLabel)
    taskRowLayout.addWidget(self.addEmployee, 1)
    taskRowLayout.addWidget(self.addSubmit)
    formLayout.addLayout(taskRowLayout)
    #when the submit button is clicked it calls this function
    self.addSubmit.clicked.connect(self.addClicked)

    #remove employees from this team 
    taskRowLayout = QtWidgets.QHBoxLayout()
    self.removeEmployeeLabel = QtWidgets.QLabel(("Remove an employee from this project:"))
    self.removeEmployee = QtWidgets.QLineEdit()
    self.removeEmployee.setPlaceholderText("Enter name here")
    self.removeEmployee.setStyleSheet("background-color: #ffffff; border: 1px solid #b0b0b0; border-radius: 4px; padding: 5px;")
    
    
    #submit button so the task can update on the file
    self.removeSubmit = QtWidgets.QPushButton("Submit")
    self.removeSubmit.setStyleSheet("background-color: #555555; color: #ffffff; padding: 6px; border-radius: 4px;")

    #when the submit button is clicked it calls this function 
    taskRowLayout.addWidget(self.removeEmployeeLabel)
    taskRowLayout.addWidget(self.removeEmployee, 1)
    taskRowLayout.addWidget(self.removeSubmit)
    formLayout.addLayout(taskRowLayout)
    self.removeSubmit.clicked.connect(self.removeClicked)

    self.outputLayout.addWidget(self.formContainer)

  """
  this function allows a team leader to be assigned 
  it checks they are in the team first then writes it onto the file
  """
  @QtCore.Slot()
  def teamLeaderClicked(self):
    #opens the file and sets a varaible for if the employee exists in the team
    managerFile = open("projectManager.txt","r")
    found = False
    #finds the inputted employee
    for line in managerFile:
        cleanline = line.strip()
        record = cleanline.split(",")
        if len(record) >=4  :
          projectEmployees = record[3].split(":")
          if self.teamLeader.text() in projectEmployees:
            found = True
            break
    managerFile.close()
    #if the employee hasnt been found then the text box is cleared and a message is given
    if found == False:
      self.outputLayout.addWidget(QtWidgets.QLabel("This employee cannot be the team leader beacuse they are not a part of this project"))
      self.teamLeader.clear()
      return
    
    #if the employee has been found they can be made team leader
    #the file is rewritten with the right values
    elif found == True:
      managerFile = open("projectManager.txt","r")
      updatedFile=[]
      for line in managerFile:
          cleanline = line.strip()
          record = cleanline.split(",")
          if len(record) >=4  :
            if record[0]== self.projectSearch.currentText():
              record[2]=self.teamLeader.text()
              updatedFile.append(",".join(record) + "\n")
            else: 
              updatedFile.append(line)
      managerFile.close()

      managerFile = open("projectManager.txt","w")
      #inputs a new data onto the file
      managerFile.writelines(updatedFile)
      self.outputLayout.addWidget(QtWidgets.QLabel("The Team Leader was sucessfully assigned to their new role"))
      #clears the boxes ready for a team Leader 
      self.teamLeader.clear()
      managerFile.close()



  """
  this function allows managers to add employees to porjects
  it checks they are an employee on the employee file and then saves the new employee on the project manager file
  """
  @QtCore.Slot()
  def addClicked(self):
    updatedFile = []
    #opens the file and sets a varaible for if the employee exists 
    employeeFile = open("employee.txt","r")
    found = False
    #finds the inputted employee
    for line in employeeFile:
        cleanline = line.strip()
        record = cleanline.split(",")
        if len(record) >=2  :
          if record[0]== self.addEmployee.text():
            found=True
            break
    employeeFile.close()
    #if the employee hasnt been found then the text box is cleared and a message is given
    if found == False:
      self.outputLayout.addWidget(QtWidgets.QLabel("This employee cannot be found"))
      self.addEmployee.clear()
      return
    
    #if the employee has been found they can checked to see if they already in there and added if not
    #the file is rewritten with the right values
    elif found == True:
      managerFile = open("projectManager.txt","r")
      lines = managerFile.readlines()
      managerFile.close()
      updatedFile.append(lines[0]) 
      for line in lines[1:]:
          cleanline = line.strip()
          record = cleanline.split(",")
          if len(record) >=4  :
            if record[0]== self.projectSearch.currentText():
              projectEmployees = record[3].split(":")
              if self.addEmployee.text() in projectEmployees:
                self.outputLayout.addWidget(QtWidgets.QLabel("The employee is already assigned to this project"))
                self.addEmployee.clear()
                return
              else:
                record[3]=record[3]+":"+self.addEmployee.text()
                updatedFile.append(",".join(record) + "\n")
            else: 
              updatedFile.append(line)
      managerFile.close()

      managerFile = open("projectManager.txt","w")
      #inputs a new data onto the file
      managerFile.writelines(updatedFile)
      self.outputLayout.addWidget(QtWidgets.QLabel("The employee was sucessfully assigned to this project"))
      #clears the boxes ready for another adding employee
      self.addEmployee.clear()
      managerFile.close()


  """
  this function allows managers to remove an employee from a project 
  for this to happen the employee needs to have completed all their tasks that have been assigned to them 
  it checks that the employee is assigned to the project and then it checks that all their tasks are complted related to that projecty before removing them  
  """
  @QtCore.Slot()
  def removeClicked(self):
    updatedFile=[]
    #opens the file and sets a varaible for if the employee exists in the team
    managerFile = open("projectManager.txt","r")
    lines = managerFile.readlines()
    managerFile.close()
    found = False
    #finds the inputted employee
    for line in lines[1:]:
        cleanline = line.strip()
        record = cleanline.split(",")
        if len(record) >=4  :
          projectEmployees = record[3].split(":")
          if self.removeEmployee.text() in projectEmployees:
            found = True
            break
    
    #if the employee hasnt been found then the text box is cleared and a message is given
    if found == False:
      self.outputLayout.addWidget(QtWidgets.QLabel("This employee cannot be removed beacuse they are not a part of this project"))
      self.removeEmployee.clear()
      return
    
    #if the employee has been found they can be removed 
    #first they need to have all their tasks complete so this checked
    elif found == True:
      projectDelegation = open("projectDelegation.txt","r")
      for line in projectDelegation:
        cleanline = line.strip()
        record = cleanline.split(",")
        if len(record) >=4:
          if record[0].strip()== self.projectSearch.currentText().strip() and record[1]==self.removeEmployee.text():
            if record[3]=="In Progress":
              self.outputLayout.addWidget(QtWidgets.QLabel("This employee cannot be removed beacuse havn't completed all their tasks for this project"))
              self.removeEmployee.clear()
              projectDelegation.close()
              return
      projectDelegation.close()
      #now a file can be written without their name
      updatedFile.append(lines[0])
      for line in lines[1:]:
          cleanline = line.strip()
          record = cleanline.split(",")
          if len(record) >=4  :
            if record[0]== self.projectSearch.currentText():
              projectEmployees = record[3].split(":")
              if self.removeEmployee.text().strip() in projectEmployees:
                projectEmployees.remove(self.removeEmployee.text().strip())
              record[3]=":".join(projectEmployees)
              updatedFile.append(",".join(record) + "\n")
            else: 
              updatedFile.append(line)
      
    managerFile = open("projectManager.txt","w")
    #inputs a new data onto the file
    managerFile.writelines(updatedFile)
    managerFile.close()
    self.outputLayout.addWidget(QtWidgets.QLabel("The employee was sucessfully removed from this project"))
    #clears the boxes ready for another employee
    self.removeEmployee.clear()



  @QtCore.Slot()
  def createClicked(self):
    #clears any widget there before 
    self.clearOutput()
    #this creates a grey box for the assign task input boxes to go into
    self.formContainer = QtWidgets.QWidget()
    self.formContainer.setStyleSheet("background-color: #f2f2f2; border-radius: 5px; padding: 10px;")
    formLayout = QtWidgets.QVBoxLayout(self.formContainer)
    #text to ensure that he user knows that they will be managing that project 
    #in the hard coded version this will have the managers name who is signed in as Zoe is just an example
    formLayout.addWidget(QtWidgets.QLabel("Create a project that is under Zoe's management \nAll entrys with a * need to contain values"),alignment=QtCore.Qt.AlignCenter)

    #new name filling in data area
    empRowLayout = QtWidgets.QHBoxLayout()
    self.projectNameLabel = QtWidgets.QLabel(("*Project Name:"))
    self.projectName = QtWidgets.QLineEdit()
    self.projectName.setPlaceholderText("Enter name here")
    self.projectName.setStyleSheet("background-color: #ffffff; border: 1px solid #b0b0b0; border-radius: 4px; padding: 5px;")
    empRowLayout.addWidget(self.projectNameLabel)
    empRowLayout.addWidget(self.projectName, 1)
    formLayout.addLayout(empRowLayout)
    
    #submit button so the task can update on the file
    self.projectSubmit = QtWidgets.QPushButton("Submit Project")
    self.projectSubmit.setStyleSheet("background-color: #555555; color: #ffffff; padding: 6px; border-radius: 4px;")
    formLayout.addWidget(self.projectSubmit)
    self.outputLayout.addWidget(self.formContainer)

    #when the submit button is clicked it calls this function 
    self.projectSubmit.clicked.connect(self.projectSubmitClicked)

  """
  This function adds a new project onto the project manager file 
  it checks that there in an input and updates the dropdown list 
  """
  @QtCore.Slot()
  def projectSubmitClicked(self):
    #checks values have not been left blank
    if self.projectName.text().strip()=="":
      self.outputLayout.addWidget(QtWidgets.QLabel("Please enter a project name"))
      self.projectName.clear()
      return
     
    managerFile = open("projectManager.txt","a")
    #inputs a new line of data onto the file which takes the data from the text boxes the user has submitted 
    #it puts in the manager zoe but in the hard coded version this will be the manager logged in
    new_line = f"{self.projectName.text()},{"Zoe"},{"None"},{""},\n"
    managerFile.write(new_line)
    #updates the search box and outputs user to let them know
    self.projectSearch.addItem(self.projectName.text())
    self.outputLayout.addWidget(QtWidgets.QLabel("The project was sucessfully added"))
    self.outputLayout.addWidget(QtWidgets.QLabel("<b>Please select this project from the dropdown menu and click manage project to assign employees and Team Leaders</b>"))
    #clears the boxes ready for a new task 
    self.projectName.clear()
    managerFile.close()
    

    
"""
calls the managers dashbaord widget in a window
"""
if __name__ == "__main__":
  app = QtWidgets.QApplication(sys.argv)
  widget = managersDashboard()
  widget.resize(800, 700)
  widget.show()
  sys.exit(app.exec())