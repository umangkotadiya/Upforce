from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom user manager
# class MyUserManager(BaseUserManager):
#     def create_user(self, email, name, password=None):
#         if not email:
#             raise ValueError("Users must have an email address")
#         user = self.model(email=self.normalize_email(email), name=name)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, name, password=None):
#         user = self.create_user(email, name, password)
#         user.is_admin = True
#         user.save(using=self._db)
#         return user

# Custom user model
class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    other_details = models.TextField()

    def __str__(self):
        return self.email

class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    other_details = models.TextField()

    def __str__(self):
        return self.title

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    other_details = models.TextField()

    def __str__(self):
        return f"{self.user.name} likes {self.post.title}"
