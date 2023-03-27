from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        # now = timezone.now()
        if not email:
            raise ValidationError('The given username must be set')
        email = self.normalize_email(email)
        try:
            user = self.model(email=email, is_active=True, is_staff=is_staff, is_superuser=is_superuser, **extra_fields)
            user.set_password(password)
            user.full_clean()
            user.save(using=self._db)
            return user
        except ValidationError as ve:
            raise ve

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)
