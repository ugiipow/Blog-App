# Generated by Django 4.2.3 on 2023-08-05 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0004_alter_post_id_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
