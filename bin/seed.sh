#! /usr/bin/env bash
# this file handles seeding our app data in the database or rds in the correct order
#(schema first, then business data, then user accounts)
# To run this file, we have 2 commands:
# bash bin/seed.sh local (this is the default if no argument is given)
# bash bin/seed.sh rds

# $1 is referring to the first argument typed after the script name
TARGET="{$1:local}"

# answers the question, which db are we seeding?
if [ "$TARGET" == "local"]; then

    ## TODO: Replace the details in the db url below with YOUR details