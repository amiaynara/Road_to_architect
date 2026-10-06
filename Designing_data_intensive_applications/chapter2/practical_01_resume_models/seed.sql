-- Loads the SAME 4 resumes twice: once as JSON documents, once as normalized tables.
-- Run:  sqlite3 resumes.db < seed.sql

DROP TABLE IF EXISTS resumes_doc;
DROP TABLE IF EXISTS positions;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS organizations;

------------------------------------------------------------------
-- MODEL A: document model. One row = one whole resume (a tree).
-- Org names are free text copied into every resume, like LinkedIn
-- before it had company pages.
------------------------------------------------------------------
CREATE TABLE resumes_doc (id INTEGER PRIMARY KEY, doc TEXT NOT NULL);

INSERT INTO resumes_doc (id, doc) VALUES
(1, '{"name":"Asha","positions":[
      {"title":"SDE",        "org":"Microsoft"},
      {"title":"Senior SDE", "org":"Google"}]}'),
(2, '{"name":"Ben","positions":[
      {"title":"Intern",     "org":"Microsoft"},
      {"title":"Engineer",   "org":"Stripe"}]}'),
(3, '{"name":"Chen","positions":[
      {"title":"Analyst",    "org":"Microsoft Corp"}]}'),
(4, '{"name":"Dara","positions":[
      {"title":"PM",         "org":"microsoft"},
      {"title":"Lead PM",    "org":"Google"}]}');

------------------------------------------------------------------
-- MODEL B: relational model. Organizations are their own entity;
-- a position stores only an ID pointing at one.
------------------------------------------------------------------
CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL);

CREATE TABLE organizations (id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE);

CREATE TABLE positions (
    id       INTEGER PRIMARY KEY,
    user_id  INTEGER NOT NULL REFERENCES users(id),
    org_id   INTEGER NOT NULL REFERENCES organizations(id),
    title    TEXT NOT NULL
);

INSERT INTO users (id, name) VALUES (1,'Asha'), (2,'Ben'), (3,'Chen'), (4,'Dara');
INSERT INTO organizations (id, name) VALUES (10,'Microsoft'), (20,'Google'), (30,'Stripe');
INSERT INTO positions (user_id, org_id, title) VALUES
    (1, 10, 'SDE'), (1, 20, 'Senior SDE'),
    (2, 10, 'Intern'), (2, 30, 'Engineer'),
    (3, 10, 'Analyst'),
    (4, 10, 'PM'), (4, 20, 'Lead PM');
