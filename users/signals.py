from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=get_user_model())
def assign_user_to_group(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='employee')
        instance.groups.add(group)
