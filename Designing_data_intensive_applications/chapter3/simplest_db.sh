#!/bin/bash

# The world's simplest databse

db_set() {
  echo "$1,$2" >> database
}

db_get() {
  grep "$1," database | sed -e "s/^$1,//" | tail -n 1
}

#db_set 123 '{"name": "amiay"}'


#db_set 124 '{"name": "sumit"}'
#db_set 12433 'any random value'

db_get 12433

