# Generated by Django 2.0 on 2017-12-30 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_auto_20171229_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='gameimage',
            field=models.ImageField(null=True, upload_to='gameimages'),
        ),
    ]
