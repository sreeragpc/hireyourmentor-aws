from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


my_choices=(
    ("student", "student"),
    ("mentor", "mentor"),
)


# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, phone_number, username, email, password=None, city=None):
        if not email:
            raise ValueError('User must have an email address ')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            city=city,

        )
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password, phone_number):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,

        )
        user.user_role = "admin"
        user.is_admin = True
        user.is_active = True
        user.is_staff = True

        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    user_role = models.CharField(max_length = 30,choices = my_choices,null=True)
    first_name = models.CharField(max_length=50,null=True)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(
        ('mobile number'), max_length=10, unique=True)

    city = models.CharField(max_length=50, null=True)
    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'phone_number']

    objects = MyUserManager()

    def _str_(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_labels):
        return True
    
    



