#!/bin/sh

docker build -t git-turf:latest .
git clone <YourAccount>/helloworld.git
git config user.email "<YourEmail>"
git config user.name "<YourName>"
docker run --rm -v $(pwd):/workspace -v ~/.ssh:/home/.ssh:ro git-turf "Hello, world"
#   #      ## ##                            ##    #
#   #       #  #                             #    #
#   #  ##   #  #  ##        # # #  ##  # ##  #  ###
##### #  #  #  # #  #       # # # #  # ##    # #  #
#   # ####  #  # #  # ##    # # # #  # #     # #  #
#   # #     #  # #  #  #     # #  #  # #     # #  #
#   #  ##   #  #  ##  #      # #   ##  #     #  ###