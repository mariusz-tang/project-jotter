from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """
        Creates and saves a user with the given username, email and
        password.
        """
        if not username:
            raise ValueError("Users must have a username")
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.full_clean()
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        """
        Creates and saves a staff superuser with the given username, email
        and password.
        """
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_verified = True
        user.save(using=self._db)
        return user
