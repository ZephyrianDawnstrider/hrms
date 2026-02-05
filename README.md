# HRMS Lite

A lightweight internal HR tool for managing employees and tracking attendance.

## Project Overview

HRMS Lite is a simple Django-based web application designed for a single HR administrator to:
- Manage employee records (add, edit, delete)
- Track daily attendance (mark and view records)

## Tech Stack

- **Backend:** Django (monolithic architecture)
- **Frontend:** Django Templates (HTML)
- **Database:** SQLite
- **Deployment:** Render (single web service)

## Project Structure

```
hrms-lite/
├── hrms/                 # Main Django project
│   ├── settings.py       # Project settings
│   ├── urls.py          # URL configuration
│   └── wsgi.py          # WSGI application
├── employees/           # Employee management app
│   ├── models.py        # Employee model
│   ├── forms.py         # Employee forms
│   ├── views.py         # Employee views
│   └── urls.py          # Employee URLs
├── attendance/          # Attendance management app
│   ├── models.py        # Attendance model
│   ├── forms.py         # Attendance forms
│   ├── views.py         # Attendance views
│   └── urls.py          # Attendance URLs
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   ├── employees/       # Employee templates
│   └── attendance/      # Attendance templates
├── requirements.txt     # Python dependencies
├── render.yaml         # Render deployment config
└── manage.py            # Django management script
```

## How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd hrms-lite
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

6. **Access the application:**
   Open your browser and go to `http://127.0.0.1:8000/`

## Features

### Employee Management
- **List Employees:** View all employees in a table format
- **Add Employee:** Create new employee records with ID, name, email, and department
- **Edit Employee:** Modify existing employee information
- **Delete Employee:** Remove employee records

### Attendance Management
- **Mark Attendance:** Record daily attendance (Present/Absent) for employees
- **View Attendance:** View attendance history for individual employees
- **Duplicate Prevention:** System prevents duplicate attendance entries for the same employee on the same day

## Database Schema

### Employee Table
| Field | Type | Description |
|-------|------|-------------|
| employee_id | CharField (unique) | Unique identifier for employee |
| full_name | CharField | Employee's full name |
| email | EmailField (unique) | Employee's email address |
| department | CharField | Employee's department |

### Attendance Table
| Field | Type | Description |
|-------|------|-------------|
| employee | ForeignKey | Reference to Employee |
| date | DateField | Attendance date |
| status | ChoiceField | Present or Absent |

**Constraint:** (employee, date) must be unique

## Assumptions & Limitations

This application is designed as a skills assessment with the following intentional constraints:

- **Single HR admin user:** No authentication or login system is implemented
- **No employee self-service:** Employees cannot log in or access the system
- **No messaging or notifications:** Communication features are not included
- **No roles or permissions:** Access control is not implemented
- **No onboarding workflows:** Employee onboarding processes are out of scope

These limitations are by design to keep the application simple and focused on core HR management functionality.

## Deployment

The application is configured for deployment on Render:

1. **Build Command:**
   ```bash
   pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
   ```

2. **Start Command:**
   ```bash
   gunicorn hrms.wsgi
   ```

3. **Environment Variables:**
   - `PYTHON_VERSION`: 3.11.0
   - `DJANGO_SETTINGS_MODULE`: hrms.settings

## URL Routes

| URL | Description |
|-----|-------------|
| `/` | Employee list (root) |
| `/employees/` | Employee list |
| `/employees/add/` | Add new employee |
| `/employees/edit/<id>/` | Edit employee |
| `/employees/delete/<id>/` | Delete employee |
| `/attendance/mark/` | Mark attendance |
| `/attendance/employee/<id>/` | View attendance for employee |

## License

This project is for educational and assessment purposes.
