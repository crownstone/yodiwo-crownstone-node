#!/bin/bash

RUNTIME_DIRECTORY=/var/run/crownstone

PID_FILE=$RUNTIME_DIRECTORY/yodiwo-crownstone.pid

case "$1" in 
start)
   /usr/bin/python3 /usr/local/bin/yodiwo-crownstone.py --configFile=/etc/yodiwo-crownstone.conf &
   echo $!>$PID_FILE
   ;;
stop)
   kill `cat $PID_FILE`
   rm $PID_FILE
   ;;
restart)
   $0 stop
   $0 start
   ;;
status)
   if [ -e $PID_FILE ]; then
      echo yodiwo-crownstone is running, pid=`cat $PID_FILE`
   else
      echo yodiwo-crownstone is NOT running
      exit 1
   fi
   ;;
*)
   echo "Usage: $0 {start|stop|status|restart}"
esac

exit 0 
