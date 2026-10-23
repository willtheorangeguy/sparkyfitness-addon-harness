from datetime import date, timedelta
import unittest
from client import credentials, rows
from contract import api


class SparkyExtendedTests(unittest.TestCase):
    def test_checkin_values_progress_over_fourteen_dates(self):
        creds = credentials()
        values = rows(api().request('/api/measurements/check-in-measurements-range/'
                                    + creds['start_date'] + '/' + creds['end_date']))
        values.sort(key=lambda x: x['entry_date'])
        self.assertEqual(len(values), 14)
        for index, item in enumerate(values):
            self.assertAlmostEqual(float(item['weight']), round(82 - index * .07, 2), places=2)
            self.assertEqual(int(item['steps']), 6500 + index * 210)

    def test_daily_meals_and_macros(self):
        client = api()
        end = date.fromisoformat(credentials()['end_date'])
        for offset in range(14):
            day = str(end - timedelta(days=offset))
            values = rows(client.request('/api/food-entries/by-date/' + day))
            with self.subTest(day=day):
                self.assertEqual(len(values), 3)
                self.assertEqual({x['meal_type'] for x in values}, {'breakfast', 'lunch', 'dinner'})
                self.assertAlmostEqual(sum(float(x['calories']) for x in values), 1110)
                self.assertAlmostEqual(sum(float(x['protein']) for x in values), 86)
                self.assertTrue(all(x['entry_date'][:10] == day for x in values))

    def test_completed_sets_include_effort_and_rest_values(self):
        client = api()
        end = date.fromisoformat(credentials()['end_date'])
        for offset in (12, 10, 8, 5, 3, 0):
            values = rows(client.request('/api/exercise-entries/by-date?selectedDate=' + str(end - timedelta(days=offset))))
            strength = [entry for entry in values if entry['name'] in {
                'Harness Barbell Squat', 'Harness Bench Press', 'Harness Bent-over Row'}]
            self.assertEqual(len(strength), 3)
            for entry in strength:
                self.assertEqual(len(entry['sets']), 3)
                for number, logged in enumerate(entry['sets']):
                    self.assertEqual(float(logged['rpe']), 7 + number * .5)
                    self.assertEqual(float(logged['rir']), 3 - number * .5)
                    self.assertEqual(int(logged['rest_time']), 90)
                    self.assertTrue(logged['completed_at'])

    def test_checkin_create_read_update_delete(self):
        client = api()
        path = '/api/measurements/check-in'
        created = client.request(path, {'entry_date': '2002-01-01', 'weight': 79.5, 'steps': 1234})
        try:
            self.assertAlmostEqual(float(client.request(path + '/2002-01-01')['weight']), 79.5)
            updated = client.request(path, {'entry_date': '2002-01-01', 'weight': 80.25, 'steps': 1500})
            self.assertEqual(updated['id'], created['id'])
            actual = client.request(path + '/2002-01-01')
            self.assertAlmostEqual(float(actual['weight']), 80.25)
            self.assertEqual(int(actual['steps']), 1500)
        finally:
            client.request(path + '/' + str(created['id']), method='DELETE')
        self.assertFalse(client.request(path + '/2002-01-01'))

    def test_unseeded_day_has_no_food_entries(self):
        self.assertEqual(rows(api().request('/api/food-entries/by-date/2002-01-01')), [])
