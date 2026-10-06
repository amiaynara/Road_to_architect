# Chapter 1 — Reliable, Scalable and Maintainable Applications

## Application-managed caching

Apps often stitch together specialized tools (cache, search index, main DB);
the app is responsible for keeping them in sync — nothing does this
automatically.

| Strategy | Write path | Staleness | Extra write latency | Use when |
|---|---|---|---|---|
| Cache-aside | App writes DB, then deletes/invalidates cache key | Possible if invalidation missed/delayed | None | Read-heavy, staleness tolerable |
| Read-through | Same as cache-aside, but cache library handles the miss-and-populate | Same as cache-aside | None | Read-heavy, want less app plumbing |
| Write-through | App writes cache; cache synchronously writes DB | None | Yes | Reads must never be stale, low-moderate writes |
| Write-behind | App writes cache; cache asynchronously flushes to DB | None (DB may lag) | No | Very high write throughput, small data-loss window OK |

**Decision checklist** (before naming a tool):
1. Read:write ratio?
2. Staleness tolerance for readers?
3. Acceptable data loss on crash for the most recent write?
4. Should sync logic live in app code, or a managed layer (e.g. DAX does write-through automatically)?

Practical: `task_01_caching_strategy.pdf` (Redis cache-aside over the ch3 toy DB; breaks invalidation on purpose to show a stale read; 3 scenarios mapped to the table above).
