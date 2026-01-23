from django.db import migrations

def create_initial_goal_data(apps, schema_editor):
    GoalType = apps.get_model('goals', 'GoalType')
    GoalResultType = apps.get_model('goals', 'GoalResultType')
    
    goal_types = ['Цель', 'Мечта', 'Хотелка']
    result_types = ['Реализовано', 'Реализовано частично', 'Не достигнута', 'Отложена', 'Отменена']
    
    for type_name in goal_types:
        GoalType.objects.get_or_create(type_name=type_name)
    print(f"✅ Создано {len(goal_types)} типов целей")
    
    for type_name in result_types:
        GoalResultType.objects.get_or_create(type_name=type_name)
    print(f"✅ Создано {len(result_types)} типов результатов целей")

def reverse_initial_goal_data(apps, schema_editor):
    GoalType = apps.get_model('goals', 'GoalType')
    GoalResultType = apps.get_model('goals', 'GoalResultType')
    
    GoalType.objects.filter(type_name__in=['Цель', 'Мечта', 'Хотелка']).delete()
    GoalResultType.objects.filter(type_name__in=['Реализовано', 'Реализовано частично', 'Не достигнута', 'Отложена', 'Отменена']).delete()
    print("❌ Удалены начальные типы целей и результатов")

class Migration(migrations.Migration):
    dependencies = [('goals', '0001_initial')]
    operations = [migrations.RunPython(create_initial_goal_data, reverse_initial_goal_data)]
