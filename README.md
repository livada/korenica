korenica
========

Console application for processing track logs and generating hang gliding competition results based on rules devised especially for Ljubomir Tomašković Memorial Competition held traditionally in Korenica, Croatia.


Copyright (C) 2012-2014 Davor Bokun <bokundavor@gmail.com>


This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.



NOTE: Although this program is licensed under GPL the actual rules it implements are not. To use these rules for a competition or distribute them you have to acquire a permission from the author (Davor Bokun <bokundavor@gmail.com>). Please contact the author for more details.


Installation
============

Released linux binaries are available at launchpad PPA.

ppa:bokundavor/livada.ppa

To install the latest released version on Ubuntu or Debian execute:

> sudo apt-add-repository ppa:bokundavor/livada.ppa

> sudo apt-get update

> sudo apt-get install korenica

For more info go to 

https://launchpad.net/~bokundavor/+archive/ubuntu/livada.ppa


Build
=====

For optimized version use:

> scons all install --prefix=\<path-to-install-dir\>


If you need debug symbols use --debug-flags like this:

> scons --debug-flags all install --prefix=\<path-to-install-dir\>


Requirements
============

libGeographic (>= 9.3.0)

python (>= 2.7)



Usage
=====

Add the install directory to the $PATH environment variable. In root of the repository execute:

> export PATH=$PATH:\<path-to-install-dir\>


After setting the environment you can use the tool like this:


```
korenica [option] input.igc [output.kml] | [task_cylinders.kml]

options:
    --verbose (default)  - Verbose track info output
    --csv                - Only CSV output
    --csv-header         - Print header for CSV output
    --task-cylinders     - Output task cylinders to kml file
    -h --help            - Print this help 
```
