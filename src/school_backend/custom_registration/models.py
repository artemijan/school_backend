from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.core import validators
from django.utils import timezone

SEX_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female')
)


class AbstractExtendedUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """
    username = models.CharField(
        _('username'),
        max_length=30,
        unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$',
                _('Enter a valid username. This value may contain only '
                  'letters, numbers ' 'and @/./+/-/_ characters.')
            ),
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=True, unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
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

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


class ExtendedUser(AbstractExtendedUser):
    birthday = models.DateTimeField(null=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)


class Subject(models.Model):
    name = models.CharField(max_length=50)


class Teacher(ExtendedUser):
    class_room = models.IntegerField(
        validators=[
            MinValueValidator(0)
        ]
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    objects = UserManager()


class Student(ExtendedUser):
    level = models.IntegerField(
        validators=[
            MaxValueValidator(11),
            MinValueValidator(1)
        ],
        null=True
    )
    level_suffix = models.CharField(max_length=1)
    form_master = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    objects = UserManager()


class School(models.Model):
    name = models.CharField(max_length=30)
    location = models.CharField(max_length=255)
    current_students_count = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(5000),
            MinValueValidator(0)
        ]
    )
