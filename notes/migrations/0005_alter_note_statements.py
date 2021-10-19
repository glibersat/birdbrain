# Generated by Django 3.2.7 on 2021-10-19 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0004_note_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='statements',
            field=models.ManyToManyField(blank=True, related_name='notes', to='notes.Statement'),
        ),
    ]
