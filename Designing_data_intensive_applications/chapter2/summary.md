# Chapter 2 — Data Models and Query Languages

## One-to-many vs many-to-one

![](relationships.png)

Same kind of link; the name depends on which end you read it from.

- **User → positions: one-to-many.** Positions are *owned* by one user. It's a tree, so nest them in a document.
- **Positions → org: many-to-one.** The org is *shared*. Either copy it (drift, N-place updates) or reference it by ID (join).
- **Rule:** owned means nest; shared means reference. The FK lives on the "many" side (`positions.org_id`).
- **Normalization** = store shared things once and refer to them by ID. Apps start tree-shaped, and features make data more interconnected.

## Hierarchical → network → relational

| Model | Example | Many-to-one via | Pain |
|---|---|---|---|
| Hierarchical | IBM IMS (1960s) | Not supported (duplicate / manual links) | Duplication, drift |
| Network | CODASYL (1970s) | Pointers; a record can have many parents | Hand-coded **access paths**; schema changes break queries |
| Relational | SQL | Foreign key + join | Joins to assemble a whole; the **query optimizer** picks the path |

Document DBs are hierarchical again for one-to-many data (locality: one read) and use **document references** (FKs by another name) for many-to-one data.

**Decision checklist:** Owned or shared? Always read as a whole? Queried from the other end? How many places does a change touch?

Practical: `task_01_one_to_many_vs_many_to_one.pdf` (same resumes as JSON docs vs tables in SQLite; 2 TODO queries show drifted copies and a 1-row rename).
