# Local validation — 2026-10-20

Validated on Docker Desktop 4.72.0, Linux containers, Compose 5.1.3 and Windows.

- Started from new PostgreSQL/uploads/backup volumes with `python harness.py up`.
- Repeated seeding retained exactly 14 check-ins, 42 food entries, 14 water
  entries, seven walks and 18 strength exercise entries with 54 logged sets;
  verified counts directly in PostgreSQL.
- `python harness.py test`: all five integration tests passed; results in
  the ignored `reports/junit.xml` file.
- Confirmed the HTTP frontend and its JavaScript assets return 200.
- The seeder authenticated through Better Auth's sign-in API and generated a
  real API key, used by the addon and tests.
- Validated the example Compose addon override using `docker compose config`.
- Ran `python harness.py reset --yes`, then `python harness.py test` from the
  resulting empty volumes; all four baseline tests passed before the strength
  fixtures were added.
- Ran concurrently with the wger harness on separate ports, networks and volumes.
- Added strength fixtures to the existing harness without resetting. Repeated
  seeding kept 54 strength sets across six training dates; the API test verifies
  reps, completed sets and increasing weights for squat, bench press and row.

The image is upstream's pinned v1.8.0 release. External providers, paid AI
integrations, and visual browser automation are not covered.
