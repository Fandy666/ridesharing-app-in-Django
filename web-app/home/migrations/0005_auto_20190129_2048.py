# Generated by Django 2.1.5 on 2019-01-29 20:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('home', '0004_auto_20190129_0407'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='user',
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['time'], 'permissions': (('confirm_order', 'Can change order status'), ('change_order_info', 'Can change order information'))},
        ),
        migrations.DeleteModel(
            name='UserInfo',
        ),
    ]
