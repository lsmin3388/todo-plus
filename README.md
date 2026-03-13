# Todo+

A smart todo management web application built with Flask and SQLite.

## Features

- **Todo List**: View, filter, and manage your todos with category and priority filters
- **CRUD Operations**: Create, read, update, and delete todos with title, description, category, priority, and due date
- **Statistics Dashboard**: Visual overview with completion rate, category distribution, and priority breakdown

## Tech Stack

- Python 3
- Flask
- SQLite
- Jinja2
- HTML/CSS

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/lsmin3388/todo-plus.git
cd todo-plus

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

## Project Structure

```
todo-plus/
├── app.py              # Flask routes and app config
├── models.py           # SQLite database model and queries
├── templates/
│   ├── base.html       # Base layout template
│   ├── index.html      # Todo list page
│   ├── form.html       # Create/edit form
│   └── stats.html      # Statistics dashboard
├── static/
│   └── style.css       # Stylesheet
├── requirements.txt
└── README.md
```

## Screenshots

### Todo List
Filter todos by category, priority, or completion status.

### Statistics Dashboard
Track your productivity with visual charts.

## License

This project is open source and available under the [MIT License](LICENSE).
