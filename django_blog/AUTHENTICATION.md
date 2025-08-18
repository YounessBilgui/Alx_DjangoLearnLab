# Authentication System Documentation

## Overview
This document describes the user authentication system implemented in the Django Blog project. It provides registration, login, logout, and profile management features.

## Components
- `Profile` model: Extends user information with a bio field (and future extensible fields like avatar).
- Forms:
  - `RegistrationForm`: Extends `UserCreationForm` to add email.
  - `ProfileForm`: Allows editing the `bio` field of the profile.
- Views:
  - `register`: Handles new user sign-up and logs the user in upon success.
  - `LoginView` / `LogoutView`: Built-in Django class-based views for authentication.
  - `profile`: Allows authenticated users to view and edit their profile.
- Templates (in `templates/registration/`): `login.html`, `register.html`, `profile.html`.
- URLs: Added routes for `/register/`, `/login/`, `/logout/`, `/profile/`.

## Data Flow
1. Registration: User submits username, email, password. On success, user is created, profile auto-created via signals, user is logged in and redirected to post list.
2. Login: Standard auth view verifies credentials, sets session.
3. Profile View/Edit: Authenticated user loads form (prefilled). POST saves changes.
4. Logout: Ends session and redirects to post list.

## Security Considerations
- CSRF protection enabled on all POST forms via `{% csrf_token %}`.
- Passwords hashed using Django's configured password hashers.
- Profile editing restricted to authenticated users (decorator `@login_required`).
- Registration form validates password strength via default validators.

## How to Test
Run tests:
```
python manage.py test blog
```
The test suite covers registration, automatic login, profile update, login/logout flow, and authenticated access enforcement.

Manual test steps:
1. Go to `/register/`, create account.
2. Confirm redirect to home and navigation shows Profile/Logout.
3. Visit `/profile/`, edit bio, save, ensure persistence.
4. Logout via `/logout/`, ensure nav changes to Login/Register.
5. Attempt to access `/profile/` when logged out -> redirected to `/login/?next=/profile/`.

## Extensibility
- Add fields to `Profile` (e.g., avatar) and include them in `ProfileForm`.
- Replace auth templates with custom styling.
- Add email verification by sending confirmation emails on registration.

## Files Reference
- `blog/models.py`: Contains `Profile` model and signals.
- `blog/forms.py`: Defines auth-related forms.
- `blog/views.py`: Implements registration and profile logic.
- `blog/urls.py`: Routing for auth endpoints.
- `templates/registration/*.html`: UI templates.
- `blog/tests.py`: Automated tests for auth flows.
