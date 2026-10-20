"""Seed exclusively through application APIs. Persist progress for safe normal reruns."""
from datetime import date, timedelta
import json
import os
from pathlib import Path
from client import API

state_file = Path('/runtime/seed-state.json')
state = json.loads(state_file.read_text()) if state_file.exists() else {'done': {}, 'catalog': {}}
state.setdefault('end_date', os.environ.get('SEED_END_DATE') or date.today().isoformat())
end = date.fromisoformat(state['end_date'])
def save():
    temp = state_file.with_suffix('.tmp')
    temp.write_text(json.dumps(state, indent=2))
    temp.replace(state_file)

api = API()
email, password = os.environ['DEMO_EMAIL'], os.environ['DEMO_PASSWORD']
try:
    api.request('/api/auth/sign-in/email', {'email': email, 'password': password})
except RuntimeError as error:
    if 'HTTP 401' not in str(error):
        raise
    api.request('/api/auth/sign-up/email', {'email': email, 'password': password, 'name': 'Harness Demo'})
    api.request('/api/auth/sign-in/email', {'email': email, 'password': password})
cred_file = Path('/runtime/credentials.json')
creds = json.loads(cred_file.read_text()) if cred_file.exists() else {}
if not creds.get('api_key'):
    key = api.request('/api/identity/user/generate-api-key', {'name': 'addon-harness', 'scope': 'full'})
    creds['api_key'] = key['apiKey']['key']
creds.update(email=email, password=password, end_date=str(end), start_date=str(end-timedelta(days=13)))
cred_file.write_text(json.dumps(creds, indent=2))
api.credentials = creds

foods = [('Harness Oatmeal', 160, 6, 27, 3, 'breakfast'),
         ('Harness Chicken Rice', 520, 42, 62, 12, 'lunch'),
         ('Harness Salmon Salad', 430, 38, 18, 24, 'dinner')]
for name, calories, protein, carbs, fat, meal in foods:
    if name not in state['catalog']:
        food = api.request('/api/foods', {'name': name, 'brand': 'Harness', 'is_custom': True,
            'serving_size': 1, 'serving_unit': 'serving', 'calories': calories,
            'protein': protein, 'carbs': carbs, 'fat': fat})
        state['catalog'][name] = {'id': food['id'], 'variant_id': food['default_variant']['id']}
        save()
if 'walking' not in state['catalog']:
    exercise = api.request('/api/exercises', {'exerciseData': json.dumps({'name': 'Harness Brisk Walk',
        'category': 'Cardio', 'calories_per_hour': 300, 'description': 'Synthetic walking activity',
        'source': 'custom', 'primary_muscles': [], 'secondary_muscles': [],
        'equipment': [], 'instructions': [], 'is_custom': True, 'shared_with_public': False})})
    state['catalog']['walking'] = exercise['id']
    save()

for index in range(14):
    day = str(end-timedelta(days=13-index))
    api.request('/api/measurements/check-in', {'entry_date': day,
        'weight': round(82-index*.07, 2), 'steps': 6500+index*210,
        'waist': round(88-index*.1, 1), 'height': 178})
    for name, calories, protein, carbs, fat, meal in foods:
        key = day + ':' + meal
        if key not in state['done']:
            food = state['catalog'][name]
            result = api.request('/api/food-entries', {'food_id': food['id'], 'variant_id': food['variant_id'],
                'entry_date': day, 'meal_type': meal, 'quantity': 1, 'unit': 'serving',
                'serving_size': 1, 'serving_unit': 'serving', 'calories': calories,
                'protein': protein, 'carbs': carbs, 'fat': fat})
            state['done'][key] = result['id']
            save()
    key = day + ':water'
    if key not in state['done']:
        api.request('/api/measurements/water-intake', {'entry_date': day, 'change_drinks': 8, 'container_id': None})
        state['done'][key] = True
        save()
    key = day + ':exercise'
    if index % 2 == 1 and key not in state['done']:
        result = api.request('/api/exercise-entries', {'exercise_id': state['catalog']['walking'],
            'exercise_name': 'Harness Brisk Walk', 'entry_date': day,
            'duration_minutes': 35, 'calories_burned': 175, 'notes': 'Harness sample workout'})
        state['done'][key] = result['id']
        save()
print('Seed complete: demo user, 14 check-ins, 42 meals, water history, 7 walks.')
