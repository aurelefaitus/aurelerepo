#!/bin/bash
# Script: triggerThreadDump is designed to monitor a log and
#         when a hit for a specified word is matched it will 
#         call a kill -3 to a JVM process 10 times 5 seconds 
#         apart then shut down
#########################################################
## Process paramters

exit_with_usage()
{
   echo "      "
   echo "      "
   echo "Usage: triggerThreadDump.sh"
   echo "      -w <word to match in log>"
   echo "      -s <word to match in ps>"
   echo "      -l <log filename with full directory>"
   echo "      -t <period time to wait before next check ( in seconds default 30 )"
   echo "      "
   echo "      "
   echo "Example: ./triggerThreadDump.sh -t 60 -s CLCLMCTR -w deadlock -l /some_directory/some_log" 
   echo "      "
   echo "      "

   exit 1
}

#########################################################
## Process parameters
## List of options the program will accept;
## those options that take arguments are followed by a colon
optstring="w:s:l:t:"

## The loop calls getopts until there are no more options on the command line
## Each option is stored in $opt, any option arguments are stored in OPTARG
while getopts $optstring opt;
do
  case $opt in
    w) SEARCHWORDLOG=$OPTARG ;;
    s) SEARCHWORDPID=$OPTARG ;;
    l) LOG=$OPTARG ;;
    t) PERIOD=$OPTARG ;;
   \?) exit_with_usage ;;
  esac
done

#########################################################
## Verify arguments are valid

if [ -z "$SEARCHWORDLOG" ]
then
  echo "Log Search Word: None"
  exit_with_usage
else 
  echo "Log Search Word: "$SEARCHWORDLOG
fi

if [ -z "$SEARCHWORDPID" ]
then
  echo "PID Search Word: None"
  exit_with_usage
else 
  echo "PID Search Word: "$SEARCHWORDPID
fi

if [ -z "$PERIOD" ]
then
  PERIOD=30
fi
  echo "Check Interval: "$PERIOD" Second(s)"

if [ -z "$LOG" ]
then
  exit_with_usage
else
  echo "Log Monitor: "$LOG
fi


##############################################################
#Run
echo "Checking for existence of file "$LOG
if [ -e "$LOG" ]
then
  echo "File Does exist. Starting monitoring..."
else
  echo "File Does not exist "
  exit
fi

PID=`ps -ef | grep java | grep $SEARCHWORDPID | awk -F' ' '{print $2}'`

if [ -z "$PID" ]
then
  echo "Process ID can not be found. Exiting"
  exit
else
  echo "JVM Process ID found on search word: "$PID
fi

while true; do
  RESULTS=`grep $SEARCHWORDLOG $LOG`

  if [ -z "$RESULTS" ]
  then
    echo "No word match detected"
  else
    echo "Word detected inducing thread dump"
    PID=`ps -ef | grep java | grep $SEARCHWORDPID | awk -F' ' '{print $2}'`

    if [ -z "$PID" ]
    then
      echo "Process ID can not be found. Exiting"
      exit
    else
      echo "JVM Process ID found on search word: "$PID
    fi
    KILL_CMD="kill -3 "$PID

    echo $KILL_CMD
    eval $KILL_CMD
    sleep 60
    eval $KILL_CMD
    sleep 60
    eval $KILL_CMD
    sleep 60
    eval $KILL_CMD
    sleep 60
    eval $KILL_CMD
    sleep 60
    eval $KILL_CMD
  
    mailx -s "Deadlock identified and thread dumps collected" "Jeff.Reid@LibertyMutual.com Timothy.Pirozzi@LibertyMutual.com" </dev/null

    exit
  fi

  sleep $PERIOD
done
