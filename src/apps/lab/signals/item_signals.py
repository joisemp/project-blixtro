# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.lab.models import Item

@receiver(post_save, sender=Item)
def set_org_from_lab(sender, instance, created, **kwargs):
    if created:  # Only perform this action if the instance was newly created
        if instance.lab and not instance.org:
            try:
                instance.org = instance.lab.org
                instance.save(update_fields=['org'])  # Save only the 'org' field to avoid recursion
            except Exception as e:
                # Handle the case where `lab.org` is not set or other issues
                print(f"Error setting org for Item {instance.id}: {e}")
