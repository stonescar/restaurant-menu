# Restaurant Menus
A python web app to manage menus for several restaurants. This project is part of my Full Stack Nanodegree at [udacity.com](http://udacity.com).

## Prerequisits
It is recommended to run this app using a VM. The following software is required:
* [Python2.7](http://python.org)
* [Virtual Box](https://www.virtualbox.org/wiki/Downloads)
* [Vagrant](https://www.vagrantup.com/downloads.html)
* [GIT](https://git-scm.com/downloads) _(Recommended)_

## Installation
1. Install all software listed above.
2. In GIT or terminal, cd to your project folder and type<br>
    `git clone https://github.com/udacity/fullstack-nanodegree-vm`
3. Inside the vagrant folder, clone this repository<br>
    `git clone https://github.com/stonescar/restaurant-menu`
4. Type `vagrant up` to boot your virtual machine (This might take a while...)
5. When the VM is booted, log in with `vagrant ssh`
6. cd to the app folder with `cd /vagrant/menu`
7. To build the database, run the file `database_setup.py`<br>`python database_setup.py`
8. Run `python project.py` to start the server
9. The application is now live at http://localhost:5000

## Licensing
This project is licensed under the [MIT License](LICENSE).