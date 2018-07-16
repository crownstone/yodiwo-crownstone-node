#!/bin/bash

case "$1" in 
start)
   /usr/bin/python3 /usr/local/bin/yodiwo-crownstone.py --configFile=/etc/yodiwo-crownstone.conf &
   echo $!>/var/run/yodiwo-crownstone.pid
   ;;
stop)
   kill `cat /var/run/yodiwo-crownstone.pid`
   rm /var/run/yodiwo-crownstone.pid
   ;;
restart)
   $0 stop
   $0 start
   ;;
status)
   if [ -e /var/run/yodiwo-crownstone.pid ]; then
      echo yodiwo-crownstone is running, pid=`cat /var/run/yodiwo-crownstone.pid`
   else
      echo yodiwo-crownstone is NOT running
      exit 1
   fi
   ;;
*)
   echo "Usage: $0 {start|stop|status|restart}"
esac

exit 0 
