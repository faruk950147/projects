from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, phone, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("Username is required")
        if not phone:
            raise ValueError("Phone number is required")
        if email:
            email = self.normalize_email(email)
        user = self.model(username=username, phone=phone, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, phone, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(username=username, phone=phone, email=email, password=password, **extra_fields)


