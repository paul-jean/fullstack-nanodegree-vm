### Swiss-pairings tournament database

This repo contains PostgresSQL schema and python application code for running a
simple swiss-pairings game tournament.

(In a "swiss-pairings" style tournament, each player in a given round is paired up
with another player with roughly the same win-loss record in the tournament so far. Nobody is
eliminated until the final round.)

### Application code

The python application code in `tournament.py` consists of a series of functions
that perform add/remove operations on the `player` and `matches` tables, as well
as functions for computing swiss pairings given the current tournament standings
(win-loss records for each player).

### Database schema

The Postgres db schema in `tournament.sql` creates tables for `players` and
`matches`, and provides saved _views_ for computing player standings.

### Test suite

The test suite contained in `tournament_test.py` tests the application code for
running the tournament.


```
    vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$ python tournament_test.py
    1. Old matches can be deleted.
    2. Player records can be deleted.
    3. After deleting, countPlayers() returns zero.
    4. After registering a player, countPlayers() returns 1.
    5. Players can be registered and deleted.
    6. Newly registered players appear in the standings with no matches.
    7. After a match, players have updated standings.
    8. After one match, players with one win are paired.
    Success!  All tests pass!
```

### Virtual machine

To start the vagrant VM, run `vagrant up` in the project root:

``` bash
    [rule146@rule146: vagrant]$ vagrant up
    Bringing machine 'default' up with 'virtualbox' provider...
    ==> default: Checking if box 'ubuntu/trusty32' is up to date...
    ==> default: Clearing any previously set forwarded ports...
    ==> default: Clearing any previously set network interfaces...
    ==> default: Preparing network interfaces based on configuration...
        default: Adapter 1: nat
    ==> default: Forwarding ports...
        default: 8000 => 8000 (adapter 1)
        default: 8080 => 8080 (adapter 1)
        default: 5000 => 5000 (adapter 1)
        default: 22 => 2222 (adapter 1)
    ==> default: Booting VM...
    ==> default: Waiting for machine to boot. This may take a few minutes...
        default: SSH address: 127.0.0.1:2222
        default: SSH username: vagrant
        default: SSH auth method: private key
        default: Warning: Connection timeout. Retrying...
    ==> default: Machine booted and ready!
    ==> default: Checking for guest additions in VM...
    ==> default: Mounting shared folders...
        default: /vagrant => /Users/rule146/code/fullstack/vagrant
    ==> default: Machine already provisioned. Run `vagrant provision` or use the `--provision`
    ==> default: to force provisioning. Provisioners marked to run always will still run.
```

Then run `vagrant ssh` to log in:

``` bash
    [rule146@rule146: vagrant]$ vagrant ssh
    Welcome to Ubuntu 14.04.1 LTS (GNU/Linux 3.13.0-45-generic i686)

     * Documentation:  https://help.ubuntu.com/

      System information as of Wed Mar  4 02:04:23 UTC 2015

      System load:  0.37              Processes:           91
      Usage of /:   3.1% of 39.34GB   Users logged in:     0
      Memory usage: 13%               IP address for eth0: 10.0.2.15
      Swap usage:   0%

      Graph this data and manage this system at:
        https://landscape.canonical.com/

      Get cloud support with Ubuntu Advantage Cloud Guest:
        http://www.ubuntu.com/business/services/cloud


    Last login: Sun Mar  1 21:17:33 2015 from 10.0.2.2
```

Go to the `/vagrant/tournament` directory inside the VM:

``` bash
    vagrant@vagrant-ubuntu-trusty-32:~$ cd /vagrant/tournament

    vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$ ls
    tournament.py  tournament.pyc  tournament.sql  tournament_test.py
```

To set up the database schema, create a `tournament` database in Postgres and
import the SQL file:

``` bash
    vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$ psql tournament
    psql (9.3.6)
    Type "help" for help.

    tournament=> \i tournament.sql
    CREATE TABLE
    CREATE TABLE
    CREATE VIEW
    CREATE VIEW
```
