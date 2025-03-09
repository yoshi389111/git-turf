#!/bin/sh

docker build -t git-turf:latest .
git clone <YourAccount>/<YourRepo>.git
cd <YourRepo>
git config user.email "<YourEmail>"
git config user.name "<YourName>"
# dry-run
docker run --rm -v $(pwd):/workspace git-turf --date 2022-01-01 --dry-run "Hello, world"
docker run --rm -v $(pwd):/workspace git-turf --date 2022-01-09 --dry-run "It's a trap"

# run
docker run --rm -v $(pwd):/workspace git-turf --date 2022-01-09 "It's a trap"

# count commits
git rev-list HEAD --count