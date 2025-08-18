# Posts & Comments API Documentation

## Endpoints

### Posts
- GET /api/posts/ : List posts (paginated, search with ?search=term)
- POST /api/posts/ : Create post (fields: title, content)
- GET /api/posts/{id}/ : Retrieve post (includes nested comments)
- PUT/PATCH /api/posts/{id}/ : Update own post
- DELETE /api/posts/{id}/ : Delete own post

### Comments
- GET /api/comments/ : List comments (filter by post with ?post=POST_ID)
- POST /api/comments/ : Create comment (fields: post, content)
- GET /api/comments/{id}/ : Retrieve comment
- PUT/PATCH /api/comments/{id}/ : Update own comment
- DELETE /api/comments/{id}/ : Delete own comment

## Permissions
- Auth required for all endpoints.
- Only authors can modify or delete their posts/comments.

## Pagination
- Enabled globally (page size 10). Use ?page=N.

## Search
- Posts support search by title and content via ?search=term.

## Sample Requests
```
POST /api/posts/
{
  "title": "First Post",
  "content": "Hello world"
}

POST /api/comments/
{
  "post": 1,
  "content": "Nice post!"
}
```
