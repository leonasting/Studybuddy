# Generated by Django 4.1 on 2023-03-14 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0002_user_bio_user_name_alter_user_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="avatar",
            field=models.ImageField(blank=True, null=True, upload_to="avatars/"),
        ),
    ]
