# Sample data

## Workout data

Log in with the demo email and open the exercise diary. **Six strength training
days** each contain **Harness Barbell Squat**, **Harness Bench Press**, and
**Harness Bent-over Row**, with three sets of ten reps per exercise: **18 exercise
entries and 54 logged strength sets**. Weights increase by 2.5 kg per session, and
sets include completion times, rest intervals, and effort ratings. Seven walking
workouts are also included.

Strength workout dates are 12, 10, 8, 5, 3 and 0 days before the fixture's end date,
recorded in `runtime/credentials.json`. Select that end date in the diary to see
the latest three strength exercises and a walk. Run `python harness.py seed` to
add the strength fixtures to an existing harness without resetting its database.

A demo user, six strength training days with 54 sets, seven walking workouts, 14 daily weight/waist/step check-ins, three custom foods, 42 breakfast/lunch/dinner diary entries, and 14 days of water intake. The demo email is configured as the local administrator.

The history ends on the first seed date and remains anchored on normal reruns.
For a fixed date, set `SEED_END_DATE=2026-10-20` before the first `up`.
Use reset to move an existing fixture to another date or start a clean scenario.
SparkyFitness is seeded through its APIs and keeps a progress journal in runtime/. Retain runtime together with database volumes. An interruption between an API commit and journal write can leave a duplicate; reset gives a clean baseline.

## Inspect the fixture

```sh
python harness.py seed
python harness.py test
```

Use the fixture end date from the ignored credentials file to choose diary/history dates. Normal reseeding stays anchored; moving to a different date requires a deliberate clean scenario. Test round-trips use `2001-01-01` to avoid changing the visible demo history.
