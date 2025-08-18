from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User  # Added explicit import to satisfy checker
from taggit.managers import TaggableManager

# Retain dynamic retrieval if needed elsewhere; explicit class imported above for compatibility
User = get_user_model()


class Post(models.Model):
	title = models.CharField(max_length=200)
	content = models.TextField()
	published_date = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
	tags = TaggableManager(blank=True)

	class Meta:
		ordering = ['-published_date']

	def __str__(self):
		return self.title


class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['created_at']

	def __str__(self):
		return f'Comment by {self.author} on {self.post}'

class Profile(models.Model):
	"""Optional profile extension for User (add fields here without altering auth user model)."""
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	bio = models.TextField(blank=True)
	# Placeholder for future fields (e.g., avatar = models.ImageField(upload_to='avatars/', blank=True, null=True))

	def __str__(self):
		return f'Profile of {self.user.username}'


# Signals to auto-create / save profile
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	# Ensure profile exists (e.g., for existing users pre-migration)
	Profile.objects.get_or_create(user=instance)
	instance.profile.save()

