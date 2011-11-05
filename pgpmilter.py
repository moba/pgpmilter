#!/usr/bin/python

## To roll your own milter, create a class that extends Milter.  
#  See the pymilter project at http://bmsi.com/python/milter.html
#  based on Sendmail's milter API http://www.milter.org/milter_api/api.html
#  This code is open-source on the same terms as Python.

## Milter calls methods of your class at milter events.
## Return REJECT,TEMPFAIL,ACCEPT to short circuit processing for a message.
## You can also add/del recipients, replacebody, add/del headers, etc.

import Milter
import StringIO
import time
import email
import sys
import os
from socket import AF_INET, AF_INET6
from Milter.utils import parse_addr
if True:
  from multiprocessing import Process as Thread, Queue
else:
  from threading import Thread
  from Queue import Queue

_PGPHEADER = "-----BEGIN PGP MESSAGE-----"
maxmsglen = 5000
socket = os.getenv("HOME") + "/milter/pgpmilter.sock"

class pgpMilter(Milter.Base):

  def __init__(self):  # A new instance with each new connection.
    self.id = Milter.uniqueID()  # Integer incremented with each call.
    self.mailbody = None

  @Milter.noreply
  def connect(self, IPname, family, hostaddr):
    self.mailbody = StringIO.StringIO()
    return Milter.CONTINUE

  def body(self, chunk):
    self.mailbody.write(chunk)
    currentBody = self.mailbody.getvalue()
    if currentBody.find(_PGPHEADER)>-1:
      return Milter.ACCEPT 
    if len(currentBody) > maxmsglen:
      self.setreply('550','5.7.1','We only accept PGP encrypted mail. PGP header not found within %s first characters of body' % maxmsglen)
      return Milter.REJECT
    return Milter.CONTINUE

  def eom(self):
    self.setreply('550','5.7.1','We only accept PGP encrypted mail')
    return Milter.REJECT

## ===
    
def main():
  bt = Thread()
  bt.start()
  timeout = 60
  # Register to have the Milter factory create instances of your class:
  Milter.factory = pgpMilter
  # we don't modify mails
  Milter.set_flags(0)
  Milter.runmilter("pgpmilter",socket,timeout)
  bt.join()

if __name__ == "__main__":
  if len(sys.argv) >= 2:
    socket = sys.argv[1] 
  if len(sys.argv) >= 3:
    maxmsglen = sys.argv[2]
  main()
