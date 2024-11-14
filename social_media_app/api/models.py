from django.db import models
from django.db import models
from django.contrib.auth.models import BaseUserManager , AbstractBaseUser , PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save


class UserManager(BaseUserManager):

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            email = self.normalize_email(email)
        username = username
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    
    username   = models.CharField(max_length=255 , unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name  = models.CharField(max_length=150, blank=True)
    email      = models.EmailField(blank=True)
    is_staff   = models.BooleanField(default=False)
    is_active  = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username

#function to account object each time user created
 
def create_user_account(sender , instance , created , **kwargs) :
       if created :
              account = Account.objects.create(user=instance)
              account.save()

post_save.connect(create_user_account , sender=User)
class Account(models.Model) :
    user = models.OneToOneField(User , on_delete=models.CASCADE , related_name="accounts")
    profile_image = models.ImageField(upload_to="profile-images" , null=True)
    bio = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return f"account of : {self.user.username} created at {self.created}"

class Post(models.Model) :
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="posts" , null=True)
    descriptions = models.TextField()
    created_at   = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account , on_delete=models.CASCADE , related_name="posts" , null=True)
    private = models.ForeignKey("PrivateG" , on_delete=models.CASCADE , related_name="posts" , null=True,blank=True)
    def __str__(self) :
        return self.title

class PostLike(models.Model):
    post = models.ForeignKey(Post , on_delete=models.CASCADE , related_name="likes")
    account = models.ForeignKey(Account , on_delete=models.CASCADE , related_name="likes")
    

    def __str__(self):
        return f"{self.post}"

class Comment(models.Model) :
    post = models.ForeignKey(Post , on_delete=models.CASCADE , related_name="comments")
    account = models.ForeignKey(Account , on_delete=models.CASCADE , related_name="comments")
    
    content = models.TextField()

    def __str__(self) :
        return f"{self.post}"

class MarketPlace(models.Model) :
    seller = models.ForeignKey(Account , on_delete=models.CASCADE , related_name="rates")
    product_name = models.CharField(max_length=255)
    product_image = models.ImageField()
    product_price = models.DecimalField(max_digits=8,decimal_places=2)
    product_informations = models.TextField()

    def __str__(self) :
        return f"{self.seller}"

class PrivateG(models.Model) :
    owner = models.ForeignKey(Account , on_delete=models.PROTECT , related_name="private_group")
    members = models.ManyToManyField(Account , related_name="private_members" , blank=True)
    code = models.CharField(max_length=8)
    created_at   = models.DateTimeField(auto_now_add=True , null=True)


    def __str__(self) :
        return f"{self.owner}"

class Public(models.Model) :
    owner = models.OneToOneField(Account , on_delete=models.PROTECT , related_name="public_group")
    members = models.ManyToManyField(Account , related_name="public_members" , blank=True)
    created_at   = models.DateTimeField(auto_now_add=True , null=True)

    def __str__(self) :
        return f"{self.owner}"
