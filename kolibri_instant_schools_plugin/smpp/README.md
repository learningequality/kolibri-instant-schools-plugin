To test this code locally, download the SMSC server simulator from:
http://www.seleniumsoftware.com/downloads.html

Then, unpack it, and run (for *NIX):

    sudo sh startsmppsim.sh

(the default SMPP settings we use here should match the settings needed for connecting to the simulator)

When an SMS is sent, it should show up in the simulator console as some lines like this:

    2017.10.17 17:33:25 797 INFO    19 short_message=To reset your Instant Schools account password
    2017.10.17 17:33:25 797 INFO    19  please click the following link: http://127.0.0.1:8080/user/#/passwordreset/8585551212/ca169cd40e7f
