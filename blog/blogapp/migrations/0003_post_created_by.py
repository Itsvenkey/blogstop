# Generated by Django 5.0 on 2023-12-31 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0002_alter_category_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='created_by',
            field=models.CharField(default='Anonymous', max_length=225),
            preserve_default=False,
        ),
    ]