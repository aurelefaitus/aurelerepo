#!/bin/bash
# Script: remove plugins from a jmeter file
#########################################################
## Process paramters

exit_with_usage()
{
   echo "Usage: removePlugins.sh"
   echo "      -f <filename>"

   exit 1
}

#########################################################
## Process parameters
## List of options the program will accept;
## those options that take arguments are followed by a colon
optstring="f:"

## The loop calls getopts until there are no more options on the command line
## Each option is stored in $opt, any option arguments are stored in OPTARG
while getopts $optstring opt;
do
  case $opt in
    f) FILENAME=$OPTARG ;;
   \?) exit_with_usage ;;
  esac
done

#########################################################
## Verify arguments are valid

if [ -z "$FILENAME" ]
then
  exit_with_usage
else 
  echo "Processing File: "$FILENAME
fi

##############################################################
#Run

NEW_FILENAME=`echo $FILENAME | sed 's/\.jmx/_NoPlugins.jmx/g'`

SEARCH_RESULTS=(`grep '<kg.apc.jmeter' $FILENAME`)
SEARCH_RESULTS_CNT=`grep '<kg.apc.jmeter' $FILENAME | wc -l`

echo "Found following plugin entities in jmx file"

for result in "${SEARCH_RESULTS[@]}"
do
   echo ${result}|grep '<kg.apc.jmeter'
done
echo "Removing following:" $SEARCH_RESULTS_CNT

if [ "${#SEARCH_RESULTS[@]}" -gt 0 ];then
  echo "Converting "$FILENAME" to "$NEW_FILENAME
  sed '/<kg.apc.jmeter/,/<hashTree>/d' $FILENAME > $NEW_FILENAME
fi

exit

