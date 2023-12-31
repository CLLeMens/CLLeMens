# Generated by Django 4.2.6 on 2023-10-07 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=255)),
                ('file_type', models.CharField(max_length=50)),
                ('md5_hash', models.CharField(blank=True, editable=False, max_length=32)),
                ('file', models.FileField(upload_to='uploads/')),
            ],
        ),
    ]
