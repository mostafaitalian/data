# Generated by Django 2.1.4 on 2019-02-16 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='newslink',
            name='slug',
            field=models.SlugField(default=models.CharField(max_length=63)),
        ),
        migrations.AlterUniqueTogether(
            name='newslink',
            unique_together={('slug', 'startup')},
        ),
    ]
