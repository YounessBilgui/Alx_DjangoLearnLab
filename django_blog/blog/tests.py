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

