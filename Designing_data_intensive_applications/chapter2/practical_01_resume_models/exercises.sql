-- sqlite3 -box resumes.db   then paste one section at a time.
-- Reset any time with:  sqlite3 resumes.db < seed.sql

------------------------------------------------------------------
-- 1. "Who has worked at Microsoft?"  (correct answer: 4 people)
------------------------------------------------------------------

-- Document model: scan every resume and string-match the copies.
SELECT json_extract(doc, '$.name') AS name, p.value ->> 'org' AS org
FROM resumes_doc, json_each(doc, '$.positions') AS p
WHERE p.value ->> 'org' = 'Microsoft';

-- Relational model.
-- TODO: names of everyone with a position at org_id 10 (join positions -> users).


------------------------------------------------------------------
-- 2. Microsoft rebrands to "Microsoft Corporation"
------------------------------------------------------------------

-- Document model: rewrite every embedded copy inside every document.
UPDATE resumes_doc
SET doc = json_set(doc, '$.positions', (
    SELECT json_group_array(
        CASE WHEN p.value ->> 'org' = 'Microsoft'
             THEN json_set(p.value, '$.org', 'Microsoft Corporation')
             ELSE json(p.value) END)
    FROM json_each(doc, '$.positions') AS p))
WHERE EXISTS (SELECT 1 FROM json_each(doc, '$.positions') AS p
              WHERE p.value ->> 'org' = 'Microsoft');
SELECT changes() AS docs_rewritten;
SELECT id, doc FROM resumes_doc;   -- which copies did it miss?

-- Relational model.
-- TODO: the same rename. How many rows does it touch?
