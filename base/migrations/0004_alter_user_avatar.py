# Generated by Django 4.1 on 2023-03-14 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0003_user_avatar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="avatar",
            field=models.ImageField(
                blank=True, default="avatars.svg", null=True, upload_to="avatars/"
            ),
        ),
    ]
