# StudyDeck Forum

A discussion platform where students can create categories, ask questions, and share knowledge. Built with Django and deployed on PythonAnywhere.

## Live Demo
**View the live site here:** [https://tejalgoyal.pythonanywhere.com]

## Features
Category-based discussion forums
- Thread creation and replies
- Google OAuth authentication
- User-based posting and replies
- Category-based discussion forums

- **Categories**
  - Mathematics
  - Computer Programming
  - Exam Tips

- Each category allows users to:
  - Create discussion threads
  - View existing discussions
  - Post replies inside threads

This project uses **Google OAuth 2.0** for authentication via `django-allauth`.

### How it works:
- Users can log in using their Google account
- Authentication is handled securely via Google OAuth
- OAuth credentials are stored using environment variables (not hardcoded)

## Tech Stack
* **Backend:** Python, Django
* **Frontend:** HTML, CSS (Django Templates)
* **Database:** SQLite3
* **Deployment:** PythonAnywhere
* **Authentication:** Django Allauth + Google OAuth

