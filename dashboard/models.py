from django.db import models
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField
from model_utils.fields import AutoCreatedField

# Create your models here.
GROUP_TYPES = (
    ('parlaposlanci', 'Parlaposlanci'),
    ('parlaskupine', 'Parlaskupine'),
    ('parlasearch', 'Parlasearch'),
    ('export', 'parladata export'),
    ('recache', 'Recache'),
    ('recache_cards', 'Recache cards'),
)
class Group(models.Model):
    name = models.CharField(_('name'),
                            max_length=128,
                            help_text=_('Name of gruop'))

    location = models.CharField(_('location'),
                            max_length=128,
                            help_text=_('Location of setter group'))

    group_type = models.CharField(_('type'),
                                  max_length=128,
                                  null=True,
                                  blank=True,
                                  help_text=_('Location of gruop'),
                                  choices=GROUP_TYPES
                                  )

    status = models.OneToOneField('Status',
                                  on_delete=models.CASCADE,
                                  related_name='g_status',
                                  )

    def __str__(self):
        return self.name


class Setter(models.Model):
    name = models.CharField(_('name'),
                            max_length=128,
                            help_text=_('Name of card'))

    group = models.ForeignKey('Group',
                              null=True,
                              blank=True,
                              related_name='setters')

    status = models.OneToOneField('Status',
                                  on_delete=models.CASCADE,
                                  related_name='s_status',
                                  )

    last_update = models.DateTimeField(_('last update time'),
                                       null=True,
                                       blank=True)

    setter_name = models.CharField(_('name'),
                                   max_length=128,
                                   help_text=_('Name of setter'))
    has_attr = models.BooleanField(default=False,
                                   help_text=_('Has setter input attribute?'))
    def __str__(self):
        return self.name

    def __str__(self):
        return self.name


class Status(models.Model):
    status_type = models.CharField(_('type'),
                                   max_length=128,
                                   help_text=_('Status type'),
                                   default='')

    status_note = models.CharField(_('note'),
                                   max_length=128,
                                   help_text=_('Status note'),
                                   default='')
    status_done = JSONField(_('done'),
                            null=True,
                            blank=True,
                            help_text=_('Status done'),
                            default=[])
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.status_type


class Cron(models.Model):
    note = models.CharField(_('note'),
                              max_length=128,
                              help_text=_('Cron note'),
                              default='')

    command = models.CharField(_('command'),
                               max_length=512,
                               help_text=_('Command'),
                               default='')

    hour = models.CharField(_('hour'),
                            max_length=32,
                            help_text=_('hours when cron runs'),
                            null=True,
                            blank=True)

    minute = models.CharField(_('minute'),
                            max_length=32,
                            help_text=_('minutes when cron runs'),
                            null=True,
                            blank=True)

    day = models.CharField(_('day'),
                            max_length=32,
                            help_text=_('days when cron runs '),
                            null=True,
                            blank=True)

    has_attr = models.BooleanField(default=True)


class ActiveCron(models.Model):
    cron = models.ForeignKey(Cron,
                             related_name='crons')

    command = models.CharField(_('command'),
                               max_length=512,
                               help_text=_('Command'),
                               default='')

    full_command = models.CharField(_('command'),
                                    max_length=512,
                                    help_text=_('Command'),
                                    default='')


