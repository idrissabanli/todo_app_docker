# -*- coding: utf-8 -*-
try:
    from django.utils.timezone import now as datetime_now
except ImportError:
    from datetime import datetime
    datetime_now = datetime.now

# Create your models here.
from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import (
    PermissionsMixin, BaseUserManager, AbstractBaseUser
)
# from users.admin import Worker


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            ** extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_superuser = True
        user.is_active = True
        user.staff_status = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('First name'), max_length=30, blank=True)
    last_name = models.CharField(_('Last name'), max_length=30, blank=True)
    reg_date = models.DateTimeField(default=datetime_now)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    staff_status = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=False,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Un select this instead of deleting accounts.'))
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()
    REQUIRED_FIELDS = []

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        db_table = 'auth_user'

    def __str__(self):
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.staff_status

    # def save(self, *args, **kwargs):
    #     worker = Worker.objects.create(user=self.id)
    #     worker.save()
    #     return super(MyUser, self).save(*args, **kwargs)


class Person(models.Model):
    description=models.TextField(_(u'Description'))
    user = models.OneToOneField(MyUser, related_name='person_user', on_delete=models.CASCADE)
    group_type = models.CharField(_('Group Type'), choices=(('person', _('Person')), ('per_group', 'Person Group')),max_length=15)
    city = models.CharField(_('City'), max_length=100, null=True, blank=True)
    address = models.CharField(_('Address'), max_length=250, blank=False)
    phone = models.CharField(_('Phone'), max_length=40, null=True, blank=True)
    website = models.CharField(_('Web site'), max_length=60, null=True, blank=True)
    zipcode = models.CharField(_('Zip code'), max_length=40, blank=True, null=True)
    image = ThumbnailerImageField(_('Profile Picture'), upload_to='person/image', blank=True)
    work_internship = models.CharField(_('Work Internship'), max_length=255, null=True, blank=True)
    certificate = models.FileField(_('Certificate'), upload_to='person/certificate', null=True, blank=True)
    presentation = models.FileField(_('Presentation'), upload_to='person/presentation', null=True, blank=True)
    created = models.DateTimeField(editable=False, default=datetime_now)
    updated = models.DateTimeField(editable=False, auto_now=True)

    class Meta:
        verbose_name = _(u'Person')
        verbose_name_plural = _(u'Persons')

    def __unicode__(self):
        return self.user.email

    def __str__(self):
        return self.user.email