# Configuration

## Precedence

Compose interpolation uses the host environment before `.env` values. The controller creates `.env` from `.env.example` only when `.env` does not exist. It substitutes four secret placeholders with random 32-byte hex strings during that creation. It never merges edits into an existing `.env`.

The controller explicitly loads `compose.yaml`, then `compose.override.yaml` when present. Service environment entries in those files configure containers. A saved seed end date wins over `SEED_END_DATE`; without either, the first seed uses its current date.

## Host and Compose settings

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `COMPOSE_PROJECT_NAME` | string | `sparkyfitness-addon-harness` | Compose resource namespace; example `sparkyfitness-addon-harness-trial`. Never share it with production. |
| `APP_PORT` | integer | `8102` | Loopback frontend host port; example `8102`. Change PUBLIC_URL to match. |
| `ADDON_PORT` | integer | `9102` | Loopback addon host port; example `9102`. |
| `PUBLIC_URL` | URL | `http://localhost:8102` | Browser origin; example `http://localhost:8102`. Used for application origin checks. |
| `DB_PASSWORD` | string | `generated on first init` | Database owner password; example placeholder `GENERATE_DB_PASSWORD` is replaced only when the controller creates .env. |
| `APP_DB_PASSWORD` | string | `generated on first init` | SparkyFitness app database password; example placeholder `GENERATE_APP_DB_PASSWORD`. |
| `SECRET_KEY` | string | `generated on first init` | Application auth/Django secret; example placeholder `GENERATE_SECRET_KEY`. |
| `ENCRYPTION_KEY` | string | `generated on first init` | SparkyFitness API encryption key; example placeholder `GENERATE_ENCRYPTION_KEY`. |
| `DEMO_USERNAME` | string | `demo` | Template field not used for SparkyFitness email login; example `demo`. |
| `DEMO_EMAIL` | string | `demo@example.test` | Seeded login/admin email; example `demo@example.test`. |
| `DEMO_PASSWORD` | string | `HarnessDemo123!` | Known disposable demo password; example `HarnessDemo123!`. Change before first seed for another value. |
| `SEED_END_DATE` | date | `empty` | First fixture end date; example `2026-10-20`. Existing saved end date wins on reruns. |

Compose rejects invalid configuration/port values. `SEED_END_DATE` must parse as an ISO date when first used. Supplying an existing `.env` with unchanged secret placeholders bypasses generation, so let the controller initialize the file or replace those values yourself.

## Addon environment

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `APP_URL` | URL | `http://server:3010` | Application origin inside the Compose network; example `http://server:3010`. |
| `PUBLIC_URL` | URL | host setting | Origin header for application checks; example `http://localhost:8102`. |
| `TARGET` | enum | `sparkyfitness` | Selects the client snapshot contract; example `sparkyfitness`. |
| `PYTHONPATH` | path | `/harness/scripts` | Import location for the sample client; example `/harness/scripts`. |
| `PYTHONDONTWRITEBYTECODE` | string | `1` | Avoid bytecode writes to read-only mounts; example `1`. |

Credentials are mounted read-only at `/runtime/credentials.json`, not passed as API tokens in the addon environment. Application-specific environment entries and fixed database settings are defined in [compose.yaml](https://github.com/willtheorangeguy/sparkyfitness-addon-harness/blob/HEAD/compose.yaml).

## Examples

Let `python harness.py config` generate the initial file and validate Compose. To run a second instance, edit its generated `.env` with a unique name and ports while retaining generated secrets:

```dotenv title=".env settings for a second sandbox"
COMPOSE_PROJECT_NAME=sparkyfitness-addon-harness-trial
APP_PORT=8202
ADDON_PORT=9202
PUBLIC_URL=http://localhost:8202
SEED_END_DATE=2026-10-20
```

The [full environment template](https://github.com/willtheorangeguy/sparkyfitness-addon-harness/blob/HEAD/.env.example) includes the remaining required values. Changing a project's name selects different volumes rather than migrating existing data.

## Test controls

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `CHECK_EXAMPLE_ADDON` | boolean | `true` | Set `false` for a custom addon API; retains application and supplied-template checks. |
