# API

The harness exposes the real upstream application's API through its frontend and a separate read-only JSON addon. `harness.py` is a host CLI; it does not implement an application API.

## Example addon

| Field | Contract |
| --- | --- |
| Method/path | GET `/` (the implementation handles GET on any path). |
| Authentication | No incoming addon authentication; it reads source credentials from the read-only runtime mount. |
| Success | HTTP 200 with snapshot JSON. |
| Failure | HTTP 503 with `{"error":"message"}` when snapshot reads raise an exception. |
| Port | Internal 8080; host `127.0.0.1:9102` by default. |

```sh
curl --fail http://localhost:9102/
```

The response includes `platform`, `date`, `checkin` and `food_entries`. `checkin` is the upstream object, not a fixed reduced schema.

Example field subset for a fixture ending on 2026-10-20 (the actual upstream object includes additional fields):

```json
{"platform":"sparkyfitness","date":"2026-10-20","checkin":{"weight":81.09},"food_entries":3}
```

## Application API

The internal origin is `http://server:3010`. Use the `api_key` from the runtime credentials file in `x-api-key`. The snapshot reads `/api/measurements/check-in/END_DATE` and `/api/food-entries/by-date/END_DATE`. Tests additionally read date-range check-ins and exercise entries and perform an isolated check-in create/read/delete.

The client sends `PUBLIC_URL` as its Origin header. Health readiness uses `/api/health` on the server. Private source requests without credentials are expected to fail with HTTP 401 or 403 in the tests.

For a live contract, inspect the pinned upstream application. The fixture's [client](https://github.com/willtheorangeguy/sparkyfitness-addon-harness/blob/HEAD/scripts/client.py) and [tests](https://github.com/willtheorangeguy/sparkyfitness-addon-harness/blob/HEAD/tests/integration/test_platform.py) show the exact consumed routes and assertions.
