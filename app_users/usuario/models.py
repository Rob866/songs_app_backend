from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from PIL import  Image


class UsuarioManager(BaseUserManager):

    def create_user(self,username,email,nombre,password=None):
        if not username:
            raise ValueError("Debes de tener un usarname")
        if not email:
            raise ValueError("Debes de tener un email")
        if not nombre:
            raise ValueError("Debes de tener un nombre")

        user = self.model(
          username = username,
          email = email.normalize_email(email),
          nombre= nombre
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username,email,nombre,password):
        user = self.create_user(
        username =username,
        nombre =nombre,
        email= email.normalize_email(email),
        password = password
        )
        user.is_admin= True
        user.is_staff= True
        user.is_superuser=True
        user.save(using=self._db)
        return user

class Usuario(AbstractBaseUser,PermissionsMixin):

    username= models.CharField(max_length=100,unique=True)
    email = models.EmailField(max_length=100,unique=True)
    nombre = models.CharField(max_length=100)
    apellido= models.CharField(max_length=100,null=True,blank=True)
    imagen = model.ImageField(default="default.jpg",upload_to='profile_pics')

    date_joined  =  models.DateTimeField(verbose_name="Fecha de ingreso",auto_now_add=True)
    last_login   =  models.DateTimeField(verbose_name="Ultima fecha de Sesión",auto_now=True)
    is_admin     =  models.BooleanField(verbose_name="¿Es Administrador?",default=False)
    is_active    =  models.BooleanField(verbose_name="¿Esta Acivo?",default=True)
    is_staff     =  models.BooleanField(verbose_name="¿Es parte del Staff?",default=False)
    is_superuser =  models.BooleanField(verbose_name="¿Es Super Usuario?",default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS= ['username','nombre']


    def __str__(self):
        return f'{self.nombre} {self.apellido}'

    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True
