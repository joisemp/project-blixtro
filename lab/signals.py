from django.db.models.signals import post_delete
from django.dispatch import receiver

from . models import Lab, Category, Item, ItemGroup

@receiver(post_delete, sender=Lab)
def delete_lab_related(sender, instance, **kwargs):
    Category.objects.filter(lab=instance).delete()
    Item.objects.filter(lab=instance).delete()
    ItemGroup.objects.filter(lab=instance).delete()


