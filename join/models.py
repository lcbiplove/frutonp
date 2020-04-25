from django.db import models
from django.forms import ModelForm
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from frutonp.utils import randomToken, file_size, image_crop
from django.core.validators import FileExtensionValidator
from home.models import NotifClick

class MyUserManager(BaseUserManager):
    def create_user(self, email, name, phone1, password=None, signed_up=timezone.localtime(), token=randomToken(),):
        """
        Creates and saves a User with the given email, name
        and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone1=phone1,
            signed_up=signed_up,
            token=token,
        )

        user.set_password(password)
        user.save(using=self._db)
        MyUserProfile.objects.create(myuser=user) 
        NotifClick.objects.create(myuser=user) 

        return user

    def create_superuser(self, email, name, phone1, password=None, signed_up=timezone.localtime(), token=randomToken(),):
        """
        Creates and saves a superuser with the given email, name and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            phone1=phone1,
            signed_up=signed_up,
            token=token,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=48)
    phone1 = models.BigIntegerField()
    token = models.CharField(max_length=65, null=True)
    is_activated = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    signed_up = models.DateTimeField(null=True, verbose_name='Signed_Up')
    name_updated = models.DateTimeField(null=True, verbose_name='Name updated')
    phone_updated = models.DateTimeField(null=True, verbose_name='Phone updated')
    password_updated = models.DateTimeField(null=True, verbose_name='Password updated')

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone1']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def short_name(self):
        if len(self.name)>22:
            return self.name[:23]+"..."
        return self.name

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class MyUserProfile(models.Model):
    myuser = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    location = models.CharField(max_length=255, null=True, default="")
    desc = models.TextField(null=True, default="")
    phone2 = models.CharField(max_length=10, null=True, default="")
    pp = models.ImageField(null=True, default='pp/no_pp.png', upload_to='pp/', validators=[file_size, FileExtensionValidator(['jpg', 'jpeg', 'png',])],)
    modified_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.modified_at = timezone.now()
        super(MyUserProfile, self).save(*args, **kwargs)
        return image_crop(self)

    def get_image(self):
        return self.pp.path

    def __str__(self):
        return self.myuser.name

class ProfilePicForm(ModelForm):
    class Meta:
        model = MyUserProfile
        fields = ('pp',)