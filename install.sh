#!/bin/sh
PATH=/sbin:/usr/sbin:/bin:/usr/bin
NAME=pgpmilter
DEST=/usr/local/bin/
PIDFILE=/var/run/$NAME.pid
INITSCRIPT=/etc/init.d/$NAME
SOCKETDIR=/var/spool/postfix/milter/
CHUID=postfix

echo "Copying $NAME.py to $DEST"
cp -i $NAME.py $DEST 

echo "Copying initdscript to $INITSCRIPT"
cp -i initdscript "$INITSCRIPT"
echo "Creating rc links"
for level in 2 3 4 5; do
    ln -f -s "$INITSCRIPT" /etc/rc$level.d/S20pgpmilter
done
for level in 0 6; do
    ln -f -s "$INITSCRIPT" /etc/rc$level.d/K20pgpmilter
done

echo "Creating socket directory $SOCKETDIR"
mkdir -p $SOCKETDIR
chown $CHUID $SOCKETDIR 
 
$INITSCRIPT start

echo
echo "OK.  Now you need to edit /etc/postfix/main.cf:"
echo "    smtpd_milters = unix:/milter/pgpmilter.sock"
echo "    milter_default_action = tempfail"
echo 
echo "For other MTA: Change CHUID in $INITSCRIPT and"
echo "possibly change default values for socket location"
echo "in $DEST$NAME or use arguments" 
