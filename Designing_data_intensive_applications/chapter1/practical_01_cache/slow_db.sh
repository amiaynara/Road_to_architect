#!/bin/bash

# Stand-in for "the main database": correct, but slow.
# Copied down from chapter3/simplest_db.sh, trimmed to just the functions.

db_set() {
  echo "$1,$2" >> database
}

db_get() {
  grep "$1," database | sed -e "s/^$1,//" | tail -n 1
}
