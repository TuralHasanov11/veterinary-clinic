from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group, PermissionsMixin
from django.db.models.signals import post_save



class AuthManager(BaseUserManager):
    
    def create_user(self, username, password=None):
        
        if not username:
            raise ValueError("Username is required")

        user = self.model(
            username = username,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, username, password):
        user = self.create_user(
            username = username,
            password = password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser= True
        user.save(using=self._db)
        return user
       


class Account(AbstractBaseUser, PermissionsMixin):
    
    username= models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    first_name= models.CharField(max_length=255, blank=True, null=True)
    last_name= models.CharField(max_length=255, blank=True, null=True)

    objects = AuthManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    GROUPS = {'admin':'Admin','staff':'İşçi'}

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def getRoleName(self):
        if self.groups.all():
            return Account.GROUPS[self.groups.all()[0].name]
        return None


def postSaveAccountReceiver(sender, instance, **kwargs):
    adminGroup = Group.objects.filter(name='admin').first()
    if adminGroup is not None:
        if not instance.is_admin:
            instance.groups.set([adminGroup])
        else:
            instance.groups.remove(adminGroup)

post_save.connect(postSaveAccountReceiver, sender=Account)
