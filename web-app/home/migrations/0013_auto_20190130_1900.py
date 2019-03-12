# Generated by Django 2.1.5 on 2019-01-30 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_auto_20190130_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('r', 'Request'), ('c', 'Confirmed'), ('f', 'Finished')], default='f', help_text='order', max_length=1),
        ),
    ]
