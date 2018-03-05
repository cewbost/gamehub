from django.db import migrations

def forwards_func(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    db_alias = schema_editor.connection.alias
    group, created = Group.objects.using(db_alias).get_or_create(name='Developer')
    if created:
        group.save()
    group, created = Group.objects.using(db_alias).get_or_create(name='Player')
    if created:
        group.save()

def reverse_func(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    db_alias = schema_editor.connection.alias
    Group.objects.using(db_alias).filter(name='Developer').delete()
    Group.objects.using(db_alias).filter(name='Player').delete()
    

class Migration(migrations.Migration):
    
    dependencies = [
        ('accounts', '0006_auto_20180104_1540')
    ]
    
    operations = [
        migrations.RunPython(forwards_func, reverse_func)
    ]
