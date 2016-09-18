# Ingenious Redistribution System <sub><sup>v2.0<sup><sub>

An "ingenious" program to download music and then parse metadata for the downloaded file.

## Examples

To download the Arctic Monkeys' album AM, you would type `$ irs album AM by Arctic Monkeys`  
To download a single song you would do `$ irs song Should I Stay Or Should I Go by The Clash`

## Installation/Dependencies

First, actually install python and pip:
 - To install python3 and `pip` for Ubuntu run this command:

 ```bash
 $ sudo apt-get install python3 python3-pip
 ```
 - For Windows follow [this](http://www.howtogeek.com/197947/how-to-install-python-on-windows/) guide to install python (remember to install ~v3.4), and [this](https://pip.pypa.io/en/latest/installing/) guide to install `pip`.
 - For OSX follow [this](http://docs.python-guide.org/en/latest/starting/install/osx/) guide that goes through python and `pip`. Also, remember to install ~v3.4.

Then install `requirements.txt` from the repository:
```bash
$ pip install -r requirements.txt
```
And you should be good to just run `irs.py`!

## License
Ingenious Redistribution System, A system built to redistribute media to the consumer.

Copyright (C) 2016  Cooper Hammond

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
