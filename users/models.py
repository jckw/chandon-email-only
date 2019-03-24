from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Email field is required')

        email = self.normalize_email(email)

        if self.model.objects.filter(email__iexact=email).exists():
            raise ValueError('This email is already connected to an account')

        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email):
        case_insensitive_email_field = '{}__iexact'.format(
            self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_email_field: email})


class AbstractCustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        null=True,
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.get_full_name()

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return self.email


class CustomUser(AbstractCustomUser):
    """
    Users within the Django authentication system are represented by this
    model.

    Password and email are required. Other fields are optional.
    """
    class Meta(AbstractCustomUser.Meta):
        swappable = 'AUTH_USER_MODEL'
