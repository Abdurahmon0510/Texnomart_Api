from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Category, Product
import json


@receiver(post_save, sender=Category)
def send_category_created_email(sender, instance, created, **kwargs):
    if created:
        admins = User.objects.filter(is_staff=True)
        admin_emails = [admin.email for admin in admins if admin.email]
        if admin_emails:
            try:
                send_mail(
                    'New category created',
                    f'New Category created: {instance.name}',
                    'abdurahmon942120510@gmail.com',
                    admin_emails,
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Error send email: {e}")


@receiver(post_save, sender=Product)
def send_product_created_email(sender, instance, created, **kwargs):
    if created:
        admins = User.objects.filter(is_staff=True)
        admin_emails = [admin.email for admin in admins if admin.email]
        if admin_emails:
            try:
                send_mail(
                    'New product created',
                    f'New product created: {instance.name}',
                    'abdurahmon942120510@gmail.com',
                    admin_emails,
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Error send email: {e}")


@receiver(pre_delete, sender=Category)
def save_deleted_category(sender, instance, **kwargs):
    with open('deleted_categories.json', 'a') as f:
        json.dump({'id': instance.id, 'name': instance.name}, f)
        f.write('\n')


@receiver(pre_delete, sender=Product)
def save_deleted_product(sender, instance, **kwargs):
    with open('deleted_products.json', 'a') as f:
        json.dump({'id': instance.id, 'name': instance.name}, f)
        f.write('\n')
