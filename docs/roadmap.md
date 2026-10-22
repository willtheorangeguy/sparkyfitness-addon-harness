# Roadmap

This baseline is a local API/addon fixture rather than a production deployment or universal addon system. Its documented boundaries are:

- PowerSync/mobile offline synchronization, provider accounts, SMTP and paid AI integrations are outside the seeded baseline.
- Browser UI is available for manual checks; automated checks exercise HTTP APIs and the example addon.
- Application images are pinned to tested revisions and need explicit updates/revalidation.
- Sample data remains anchored to its initial end date rather than advancing daily.
- The API seeder cannot atomically commit an upstream request and its local progress journal; interruption can leave duplicates.
- Addons with another interface need their own readiness checks and test expectations.

Use `python harness.py test` to verify the current baseline. Actionable defects found during this documentation pass are recorded separately in the repository's internal findings; they are excluded from the site.
