# Tagging & Search Features

## Overview
The blog supports tagging posts and searching across titles, content, and tag names to help users discover related content quickly.

## Tagging
- Implemented via `django-taggit`'s `TaggableManager` on the `Post` model.
- Users add tags in the post create/update form using a comma-separated input.
- New tags are created automatically when a post is saved.
- Tags are displayed on post list, detail pages, and link to a filtered tag view.

### Adding Tags
1. Navigate to Create or Edit Post.
2. Enter tags separated by commas in the tags field (e.g., `django, api, testing`).
3. Submit the form; tags appear under the post.

## Viewing Posts by Tag
- Each tag link leads to `/tags/<slug>/` which lists all posts having that tag.
- Template: `posts_by_tag.html`.

## Search
- Search URL: `/search/?q=keyword`.
- Matches are found if `keyword` appears in the title, content, or any associated tag name.
- View: `PostSearchView` using `Q` objects for case-insensitive partial matching.
- Template: `search_results.html`.

### Using the Search Bar
1. Enter a keyword in the navbar search input.
2. Results list all matching posts (title, snippet).
3. If no matches, a graceful message appears.

## Implementation Details
- `PostSearchView.get_queryset()` filters with:
  - `title__icontains`
  - `content__icontains`
  - `tags__name__icontains`
- `distinct()` ensures no duplicate posts when multiple tags match.

## Extensibility
- Add pagination by subclassing ListView and setting `paginate_by = 10`.
- Integrate advanced search (e.g. Postgres full-text) later.
- Provide tag clouds or related posts by overlapping tags.

## Testing Suggestions
- Create posts with overlapping tags; verify search includes all correct posts.
- Search for an existing tag name; posts using that tag must appear.
- Search for nonsense term returns empty results.
- Add/edit post to change tags then re-search to confirm updates.

## Files Involved
- `blog/models.py`: `Post` with `TaggableManager`.
- `blog/forms.py`: `PostForm` with tag field + help text.
- `blog/views.py`: `PostSearchView`, `TagPostListView`.
- `templates/post_detail.html`, `templates/post_list.html`: Display tags.
- `templates/posts_by_tag.html`: Tag-filtered posts.
- `templates/search_results.html`: Search results output.

## Dependencies
- `django-taggit` already installed and in `INSTALLED_APPS`.

## Quick Manual Test
1. Create Post A with tags: `django, web`.
2. Create Post B with tags: `api, django`.
3. Visit `/tags/django/` → Both posts show.
4. Visit `/search/?q=web` → Only Post A.
5. Visit `/search/?q=django` → Both posts.

This completes tagging & search integration.
