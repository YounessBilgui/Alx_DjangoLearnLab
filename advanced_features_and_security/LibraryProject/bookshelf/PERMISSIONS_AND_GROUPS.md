# Permissions and Groups Setup for Bookshelf App

## Custom Permissions
The `Book` model in `bookshelf/models.py` defines the following custom permissions:
- `can_view`: Can view book
- `can_create`: Can create book
- `can_edit`: Can edit book
- `can_delete`: Can delete book

These are set in the `Meta` class of the `Book` model.

## Groups
Recommended groups to create in the Django admin:
- **Viewers**: Assign `can_view` permission.
- **Editors**: Assign `can_view`, `can_create`, and `can_edit` permissions.
- **Admins**: Assign all permissions (`can_view`, `can_create`, `can_edit`, `can_delete`).

## Assigning Permissions
1. Go to the Django admin site.
2. Create the groups above.
3. Assign the appropriate permissions to each group using the checkboxes for the `Book` model.
4. Add users to the relevant groups.

## Enforcing Permissions in Views
- The views for adding, editing, and deleting books use the `@permission_required` decorator with the custom permissions:
  - `@permission_required('bookshelf.can_create', raise_exception=True)` for adding books
  - `@permission_required('bookshelf.can_edit', raise_exception=True)` for editing books
  - `@permission_required('bookshelf.can_delete', raise_exception=True)` for deleting books

## Testing
- Assign users to different groups and verify that only users with the correct permissions can access the protected views.
- Attempt to access restricted views as a user without the required permission to confirm access is denied.
