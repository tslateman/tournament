The purpose of this project is to use SQL and Python code to 
handle the data for a tournament.

This was written for the second project of the Udacity Full Stack 
Developer nanodegree.

-------------------------------------------------------------------

List Of Files

Be sure that you have saved in your directory the following files:

tournament.py
tournament_test.py
tournament.sql

You should also have this README file, but it's not required to run.

-------------------------------------------------------------------

Instructions For Usage

You will need to have Vagrant setup. For more help on that:

https://www.udacity.com/wiki/ud197/install-vagrant

Once you have vagrant, you will need to type the following commands:

vagrant up
vagrant ssh

This gets you to the virtual machine. From there you will need to 
navigate to the synced home directory. Note, you might need to enter
"cd ../../vagrant" depending on where you start.

Once in the right directory, the sql setup can be run by entering:

psql
\i tournament.sql
\q

To test the code you will need to have Python installed first. 
This was created with 2.7.10, so if you want to match please select 
that version and install on your machine. Then to run the program,
navigate to the directory you saved the files and enter the following:

python tournament_test.py

If you prefer a UI to the command line, python's IDLE is helpful.
To download python 2.7.10 or to get IDLE google "install python" or
go to https://www.python.org/downloads/ 

-------------------------------------------------------------------

The tournament_test.py file was written by Udacity. 
The tournament.py had initial function headers already and then
edits were made to the function bodies to fulfill requirements
and pass the unit tests. 
The tournament.sql file contains the code for setting up the 
tables and views of the database. 