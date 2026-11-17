import sys

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QFrame,
    QScrollArea,
    )
from pathlib import Path

# The three columns in display order: (status stored on each task, heading shown)
STATUSES = [
    ("assigned", "Assigned"),
    ("in_progress", "In progress"),
    ("complete", "Complete"),
]

# What each card's button says, and where it moves the task
NEXT_STEP = {
    "assigned": ("Start", "in_progress"),
    "in_progress": ("Done", "complete"),
}


class TaskCard(QFrame):
    """One task. Emits the task's id when its action button is clicked."""
    actionClicked = Signal(int)

    def __init__(self, task, parent=None):
        super().__init__(parent)
        self.setObjectName("taskCard")

        layout = QVBoxLayout(self)                     
        layout.setContentsMargins(12, 10, 12, 10)

        title = QLabel(task["title"])
        title.setObjectName("taskTitle")
        title.setWordWrap(True)
        layout.addWidget(title)

        # Completed tasks have no next step, so no button
        if task["status"] in NEXT_STEP:
            buttonText, _ = NEXT_STEP[task["status"]]
            button = QPushButton(buttonText)
            button.setObjectName("taskActionButton")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(lambda: self.actionClicked.emit(task["id"]))
            layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignRight)


class BoardColumn(QFrame):
    """A column with a heading and a scrollable list of task cards."""
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setObjectName("boardColumn")
        self.title = title

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)   
        outer.setSpacing(0)  

        self.header = QLabel(title)
        self.header.setObjectName("columnHeader")
        outer.addWidget(self.header)

        # Scroll area so a long column scrolls instead of stretching the window
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)                 # cards fill the column's width
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        container = QWidget()
        container.setObjectName("cardsContainer")
        self.cardsLayout = QVBoxLayout(container)
        self.cardsLayout.setContentsMargins(12, 12, 12, 12)
        self.cardsLayout.setSpacing(8)
        self.cardsLayout.addStretch(1)                  # keeps cards pinned to the top
        scroll.setWidget(container)
        outer.addWidget(scroll)

    def setCards(self, cards):
        """Replace the column's cards and update the count in the heading."""
        while self.cardsLayout.count() > 1:             # remove old cards, keep the stretch
            item = self.cardsLayout.takeAt(0)
            item.widget().deleteLater()                 # deferred delete: safe even mid-click
        for card in cards:
            self.cardsLayout.insertWidget(self.cardsLayout.count() - 1, card)   # above the stretch
        self.header.setText(f"{self.title} ({len(cards)})")


class ToDoList(QWidget):
    def __init__(self):
        super().__init__()
        
        self.tasks = []
        self.nextId = 1

        self.setWindowTitle("To-Do List")
        self.resize(500, 450)

        self.setObjectName("todoScreen")
        self.setAttribute(Qt.WA_StyledBackground, True)

        # Heading
        heading = QLabel("To-Do List")
        heading.setObjectName("heading")

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        #Text input for typing new tasks
        self.taskInput = QLineEdit()
        self.taskInput.setPlaceholderText("Type a new task here...")

        #Adding button
        self.addButton = QPushButton("Add Task")
        self.addButton.setObjectName("addTaskButton")

        #Place input field and button side-by-side using a horizontal layout
        inputLayout = QHBoxLayout()
        inputLayout.addWidget(self.taskInput)
        inputLayout.addWidget(self.addButton)

        boardLayout = QHBoxLayout()
        boardLayout.setSpacing(16)
        self.columns = {}
        for status, title in STATUSES:
            column = BoardColumn(title)
            self.columns[status] = column
            boardLayout.addWidget(column)

        #Add everything to main vertical layout
        layout.addWidget(heading)
        layout.addLayout(inputLayout)
        layout.addLayout(boardLayout, 1) 

        self.setLayout(layout)

        #Connecting the buttons
        self.addButton.clicked.connect(self.addTask)
        self.taskInput.returnPressed.connect(self.addTask)

        self.refresh()    

    def addTask(self):
        text = self.taskInput.text().strip()
        if not text:
            return

        self.tasks.append({"id": self.nextId, "title": text, "status": "assigned"})
        self.nextId += 1
        self.taskInput.clear()
        self.refresh()

    def advanceTask(self, taskId):
        """Move a task to the next column, then redraw."""
        for task in self.tasks:
            if task["id"] == taskId and task["status"] in NEXT_STEP:
                _, nextStatus = NEXT_STEP[task["status"]]
                task["status"] = nextStatus
        self.refresh()

    def refresh(self):
        """Rebuild every column from the task data."""
        for status, column in self.columns.items():
            cards = []
            for task in self.tasks:
                if task["status"] == status:
                    card = TaskCard(task)
                    card.actionClicked.connect(self.advanceTask)
                    cards.append(card)
            column.setCards(cards)


# changed as it made 2 qApplication instances which leads to an error.
# Run this file on its own with: python -m app.screens.todo
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    stylesPath = Path(__file__).resolve().parent.parent / "styles.qss"
    app.setStyleSheet(stylesPath.read_text(encoding="utf-8"))
    window = ToDoList()
    window.show()

    sys.exit(app.exec())


