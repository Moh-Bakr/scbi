# Generated by Django 4.1.2 on 2022-10-13 13:54

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('CustomAuth', '0005_alter_customuser_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
