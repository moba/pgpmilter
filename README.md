pgpmilter
==========

This is a very simple [milter](https://www.milter.org/) in Python
using pymilter that rejects any non-PGP mail.

About Milters
-------------

Milters are a way to reject or modify mail before it goes into the
mail queue.  This is useful because it lets me bounce spam to its
real sender, not the forged from-address on the mail, so I don't
become part of the backscatter problem.

MTAs that support milters include
[Sendmail](http://www.sendmail.org/),
[Postfix](http://www.postfix.org), and
[qpsmtpd](http://smtpd.develooper.com/).

Functionality
-------------

This milter is part of a concept that requires mailservers to only 
accept PGP mail. I have no idea what you might want to use it for. It looks
for a PGP header in the body of a mail and once it finds one, it will
ACCEPT the mail. After 5000 characters into scanning the body, 
all mail is REJECTed. Actually it might scan some more because pymilter reads the mail body in possibly larger chunks.

Installation
------------

PGPMilter is preconfigured for Postfix, but can be easily altered to be used
with other MTAs. Possibly, the only thing you need to change is the CHUID
in its initscript.

Requires: Python, python-milter
To install, run `chmod +x install.sh && ./install.sh`

1. copies initscript to /etc/init.d/pgpmilter
2. copies pgpmilter.py to /usr/local/bin
3. creates rc.d symlinks
4. runs /etc/init.d/pgpmilter

### Integration in Postfix

add to /etc/postfix/main.cf:

	smtpd_milters = unix:/milter/pgpmilter.sock
	milter_default_action = tempfail

### Integration in other MTAs

PGPMilter is preconfigured for Postfix, but can be easily altered to be used
with other MTAs. Possibly, the only thing you need to change is the CHUID
in its initscript.

About Backscatter
-----------------

Backscatter is when spam sent from a forged `From` address gets
bounced back to that address, effectively turning the spam's first
recipient into an inadvertent spam source.  To avoid creating
backscatter, don't bounce mail after accepting it; instead, refuse the
mail at SMTP-time.

Getting it
----------

    git clone git://github.com/moba/pgpmilter.git 

Based on
--------

The documentation and install script is based on minimilter,
https://github.com/kragen/minimilter

