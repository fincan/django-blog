# Generated by Django 3.1.7 on 2021-03-01 14:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='coment_content',
            new_name='comment_content',
        ),
    ]
