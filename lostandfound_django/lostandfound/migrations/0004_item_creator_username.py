# Generated by Django 5.0.5 on 2024-05-09 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lostandfound', '0003_rename_user_usr_item_contact_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='creator_username',
            field=models.CharField(default=12, max_length=150),
            preserve_default=False,
        ),
    ]