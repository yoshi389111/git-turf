========
git-turf
========

The git-turf program outputs ASCII art to GitHub contribution graph.

Examples
========

::
    $ git-turf "Hello, world"
    #   #      ## ##                            ##    #
    #   #       #  #                             #    #
    #   #  ##   #  #  ##        # # #  ##  # ##  #  ###
    ##### #  #  #  # #  #       # # # #  # ##    # #  #
    #   # ####  #  # #  # ##    # # # #  # #     # #  #
    #   # #     #  # #  #  #     # #  #  # #     # #  #
    #   #  ##   #  #  ##  #      # #   ##  #     #  ###
    $ git push

Requirements
============

* Python 3.5 or higher

Installation
============

Install
-------

::
    $ git clone https://github.com/yoshi389111/git-turf.git
    $ cd git-turf
    $ pip3 install -e .

or

::
    $ pip3 install git+https://github.com/yoshi389111/git-turf.git

Uninstall
---------

::
    $ pip3 uninstall git-turf

Usage
=====

Usage:
------

::
    git-turf [-h]
    git-turf [-v]
    git-turf [-d DATE] [-t TIME] [-n] MESSAGE

Options:
--------

::
    -h,      --help       show this help message and exit
    -v,      --version    show program's version number and exit
    -d DATE, --date DATE  start date. format is YYYY-MM-DD
    -t TIME, --time TIME  commit time. format is HH:MM:SS
    -n,      --dry-run    display message only

Copyright and License
=====================

Program
-------

Copyright (C) 2019, SATO_Yoshiyuki

This software is released under the MIT License.
http://opensource.org/licenses/mit-license.php

Fonts
-----

The bitmap is created based on misaki_gothic.bdf font and k6x8.bdf font.

misaki_gothic.bdf
^^^^^^^^^^^^^^^^^

* Copyright(C) 2000-2007 Num Kadoma
* http://littlelimit.net/misaki.htm
* Version: 2019-06-03a

k6x8.bdf
^^^^^^^^

* Copyright(C) 2002-2019 Num Kadoma
* http://littlelimit.net/k6x8.htm
* k6x8 period beta2

License
^^^^^^^

* http://littlelimit.net/font.htm

    These fonts are free software.
    Unlimited permission is granted to use, copy, and distribute them,
    with or without modification, either commercially or noncommercially.
    THESE FONTS ARE PROVIDED "AS IS" WITHOUT WARRANTY.
