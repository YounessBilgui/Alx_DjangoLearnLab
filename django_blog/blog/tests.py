from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthFlowTests(TestCase):
	def test_registration_login_profile(self):
		# Register
		response = self.client.post(reverse('blog:register'), {
			'username': 'tester',
			'email': 'tester@example.com',
			'password1': 'StrongPass12345',
			'password2': 'StrongPass12345'
		})
		self.assertEqual(response.status_code, 302)
		self.assertTrue(User.objects.filter(username='tester').exists())

		# Logged in redirect to list
		response = self.client.get(reverse('blog:profile'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Your Profile')

		# Update profile
		response = self.client.post(reverse('blog:profile'), {'bio': 'Hello world'})
		self.assertEqual(response.status_code, 302)
		user = User.objects.get(username='tester')
		self.assertEqual(user.profile.bio, 'Hello world')

	def test_login_logout(self):
		user = User.objects.create_user(username='abc', email='a@b.com', password='Abcpass12345')
		# Login
		response = self.client.post(reverse('blog:login'), {'username': 'abc', 'password': 'Abcpass12345'})
		self.assertEqual(response.status_code, 302)
		# Logout
		response = self.client.get(reverse('blog:logout'))
		self.assertEqual(response.status_code, 302)
		# Access profile should redirect
		response = self.client.get(reverse('blog:profile'))
		self.assertEqual(response.status_code, 302)


class PostCrudTests(TestCase):
	def setUp(self):
		from django.contrib.auth import get_user_model
		self.User = get_user_model()
		self.author = self.User.objects.create_user(username='author', password='StrongPass12345')
		self.other = self.User.objects.create_user(username='other', password='StrongPass12345')

	def test_create_post(self):
		self.client.login(username='author', password='StrongPass12345')
		response = self.client.post('/posts/new/', {
			'title': 'My Post',
			'content': 'Body',
			'tags': ''
		})
		self.assertEqual(response.status_code, 302)
		from .models import Post
		self.assertTrue(Post.objects.filter(title='My Post').exists())

	def test_update_permission(self):
		from .models import Post
		post = Post.objects.create(title='X', content='Y', author=self.author)
		# other user cannot edit
		self.client.login(username='other', password='StrongPass12345')
		resp = self.client.get(f'/posts/{post.id}/edit/')
		self.assertEqual(resp.status_code, 403)
		# author can edit
		self.client.logout()
		self.client.login(username='author', password='StrongPass12345')
		resp = self.client.post(f'/posts/{post.id}/edit/', {'title': 'X2', 'content': 'Y2', 'tags': ''})
		self.assertEqual(resp.status_code, 302)
		post.refresh_from_db()
		self.assertEqual(post.title, 'X2')

	def test_delete_permission(self):
		from .models import Post
		post = Post.objects.create(title='Del', content='Y', author=self.author)
		# other user attempt
		self.client.login(username='other', password='StrongPass12345')
		resp = self.client.post(f'/posts/{post.id}/delete/')
		self.assertEqual(resp.status_code, 403)
		self.client.logout()
		# author deletes
		self.client.login(username='author', password='StrongPass12345')
		resp = self.client.post(f'/posts/{post.id}/delete/')
		self.assertEqual(resp.status_code, 302)
		self.assertFalse(Post.objects.filter(id=post.id).exists())


class SearchTagTests(TestCase):
	def setUp(self):
		from django.contrib.auth import get_user_model
		from .models import Post
		self.User = get_user_model()
		self.user = self.User.objects.create_user(username='u', password='StrongPass12345')
		p1 = Post.objects.create(title='Django Testing', content='Learn to test Django apps', author=self.user)
		p2 = Post.objects.create(title='REST Framework', content='Building APIs', author=self.user)
		p1.tags.add('django')
		p2.tags.add('api')

	def test_search(self):
		resp = self.client.get('/search/?q=django')
		self.assertContains(resp, 'Django Testing')
		self.assertNotContains(resp, 'REST Framework')

	def test_tag_filter(self):
		resp = self.client.get('/tags/django/')
		self.assertContains(resp, 'Django Testing')
		self.assertNotContains(resp, 'REST Framework')


class CommentCrudTests(TestCase):
	def setUp(self):
		from django.contrib.auth import get_user_model
		from .models import Post
		self.User = get_user_model()
		self.author = self.User.objects.create_user(username='author', password='StrongPass12345')
		self.other = self.User.objects.create_user(username='other', password='StrongPass12345')
		self.post = Post.objects.create(title='P', content='C', author=self.author)

	def test_add_comment(self):
		self.client.login(username='author', password='StrongPass12345')
		resp = self.client.post(f'/posts/{self.post.id}/comments/new/', {'content': 'Nice post'})
		self.assertEqual(resp.status_code, 302)
		from .models import Comment
		self.assertTrue(Comment.objects.filter(post=self.post, content='Nice post').exists())

	def test_add_comment_whitespace_rejected(self):
		self.client.login(username='author', password='StrongPass12345')
		resp = self.client.post(f'/posts/{self.post.id}/comments/new/', {'content': '   '})
		# Should redirect back without creating comment
		from .models import Comment
		self.assertFalse(Comment.objects.filter(post=self.post, content='   ').exists())

	def test_comment_url_pattern(self):
		# Ensure intuitive URL structure exists
		path = f'/posts/{self.post.id}/comments/new/'
		resp = self.client.get(path)
		# GET currently redirects (not allowed method) but URL resolves; accept 302 or 301
		self.assertIn(resp.status_code, (302, 301, 405))

	def test_edit_comment_permission(self):
		from .models import Comment
		c = Comment.objects.create(post=self.post, author=self.author, content='Orig')
		# other cannot edit
		self.client.login(username='other', password='StrongPass12345')
		resp = self.client.get(f'/comments/{c.id}/edit/')
		self.assertEqual(resp.status_code, 403)
		self.client.logout()
		# owner edits
		self.client.login(username='author', password='StrongPass12345')
		resp = self.client.post(f'/comments/{c.id}/edit/', {'content': 'Changed'})
		self.assertEqual(resp.status_code, 302)
		c.refresh_from_db()
		self.assertEqual(c.content, 'Changed')

	def test_delete_comment_permission(self):
		from .models import Comment
		c = Comment.objects.create(post=self.post, author=self.author, content='Delete me')
		self.client.login(username='other', password='StrongPass12345')
		resp = self.client.post(f'/comments/{c.id}/delete/')
		self.assertEqual(resp.status_code, 403)
		self.client.logout()
		self.client.login(username='author', password='StrongPass12345')
		resp = self.client.post(f'/comments/{c.id}/delete/')
		self.assertEqual(resp.status_code, 302)
		self.assertFalse(Comment.objects.filter(id=c.id).exists())


