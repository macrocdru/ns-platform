from django.db import migrations

def create_initial_session_data(apps, schema_editor):
    SessionType = apps.get_model('goal_sessions', 'SessionType')
    SessionStatus = apps.get_model('goal_sessions', 'SessionStatus')
    
    session_types = ['Установочная', 'Регулярная', 'Завершающая']
    session_statuses = ['Планирование', 'В процессе', 'Завершена', 'Отменена']
    
    for type_name in session_types:
        SessionType.objects.get_or_create(type_name=type_name)
    print(f"✅ Создано {len(session_types)} типов сессий")
    
    for type_name in session_statuses:
        SessionStatus.objects.get_or_create(type_name=type_name)
    print(f"✅ Создано {len(session_statuses)} статусов сессий")

def reverse_initial_session_data(apps, schema_editor):
    SessionType = apps.get_model('goal_sessions', 'SessionType')
    SessionStatus = apps.get_model('goal_sessions', 'SessionStatus')
    
    SessionType.objects.filter(type_name__in=['Установочная', 'Регулярная', 'Завершающая']).delete()
    SessionStatus.objects.filter(type_name__in=['Планирование', 'В процессе', 'Завершена', 'Отменена']).delete()
    print("❌ Удалены начальные типы и статусы сессий")

class Migration(migrations.Migration):
    dependencies = [('goal_sessions', '0001_initial')]
    operations = [migrations.RunPython(create_initial_session_data, reverse_initial_session_data)]
