"""Hard-coded sample data (users, projects, tasks, topics, posts) shaped like database tables with ids. Replaced by the database in Part II."""

ROLES = ("Employee", "Manager")

USERS = [
    {
        "id": 1,
        "email": "J.Smith@make-it-all.co.uk",
        "password": "M4keItAll123?",
        "name": "John Smith",
        "role": "Employee",
        "teamIds": [1], 
    },
    {
        "id": 2,
        "email": "G.Smith@make-it-all.co.uk",
        "password": "M4keItAll321!",
        "name": "George Smith",
        "role": "Manager",
        "teamIds": [1, 2], 
    }
]

