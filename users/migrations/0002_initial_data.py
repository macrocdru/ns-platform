from django.db import migrations

def create_initial_roles(apps, schema_editor):
    NSRole = apps.get_model('users', 'NSRole')
    roles = ['Администратор', 'Модератор', 'Участник', 'Наблюдатель']
    for role_name in roles:
        NSRole.objects.get_or_create(rolename=role_name)
    print(f"✅ Создано {len(roles)} ролей системы")

def reverse_initial_roles(apps, schema_editor):
    NSRole = apps.get_model('users', 'NSRole')
    NSRole.objects.filter(rolename__in=['Администратор', 'Модератор', 'Участник', 'Наблюдатель']).delete()
    print("❌ Удалены начальные роли системы")

class Migration(migrations.Migration):
    dependencies = [('users', '0001_initial')]
    operations = [migrations.RunPython(create_initial_roles, reverse_initial_roles)]
