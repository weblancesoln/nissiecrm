# Nissie Ideal Shelters CRM

A professional lead management CRM for Nissie Ideal Shelters Real Estate. Built with Django, designed for simplicity and efficiency—similar to Zoho CRM but focused exclusively on lead management.

## Features

- **Lead Management**: Add, edit, view, and delete leads
- **Lead Fields**: Prospect name, phone, email, point of contact, prospect response, remarks, status, source
- **Color Coding**: Visual lead classification (Hot, Warm, New, Cold, Urgent, Follow Up, etc.)
- **Bulk Upload**: Import leads from CSV or Excel files
- **Export**: Download leads as CSV or Excel
- **Search & Filter**: By name, phone, status, or color
- **Dashboard**: Lead statistics at a glance
- **User Authentication**: Register, login, and secure access

## Quick Start

### 1. Create virtual environment and install dependencies

```bash
cd "AI Website Builder /Nissie CRM"
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run migrations

```bash
python manage.py migrate
```

### 3. Create superuser (optional, for admin access)

```bash
python manage.py createsuperuser
```

### 4. Run the development server

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/

## Upload Format

For bulk upload, use CSV or Excel with columns (names are flexible):

| Column         | Alternatives     | Required |
|----------------|------------------|----------|
| first_name     | firstname        | Yes      |
| last_name      | lastname         | No       |
| prospect_name  | name (legacy)    | Alt      |
| phone_number   | phone, mobile    | No       |
| email          | mail             | No       |
| point_of_contact | poc, referral  | No       |
| prospect_response | response      | No       |
| remarks        | notes, comments  | No       |
| status         | -                | No       |
| source         | lead_source      | No       |
| assigned_to    | staff (username) | No       |

Download a sample template from **Upload** → **Download sample CSV template**.

## Color Codes

- **Green** - Hot Lead
- **Yellow** - Warm Lead  
- **Blue** - New
- **Gray** - Cold
- **Red** - Urgent
- **Pink** - Follow Up
- **Orange** - Interested
- **Teal** - Qualified
