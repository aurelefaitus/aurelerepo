#!/bin/bash
# Script: replace variables from a jmeter file
#########################################################
## Process paramters

exit_with_usage()
{
   echo "Usage: replaceVariables.sh"
   echo "      -f <filename>"
   echo "      -s <search string>"
   echo "      -r <replace string>"

   exit 1
}

#########################################################
## Process parameters
## List of options the program will accept;
## those options that take arguments are followed by a colon
optstring="f:s:r:"

## The loop calls getopts until there are no more options on the command line
## Each option is stored in $opt, any option arguments are stored in OPTARG
while getopts $optstring opt;
do
  case $opt in
    f) FILENAME=$OPTARG ;;
    s) SEARCH_STRING=$OPTARG ;;
    r) REPLACE_STRING=$OPTARG ;;
   \?) exit_with_usage ;;
  esac
done

#########################################################
## Verify arguments are valid

if [ -z "$FILENAME" ]
then
  echo "No file name. Exiting."
  exit_with_usage
else 
  echo "Checking for existence of file "$FILENAME
  if [ -e "$FILENAME" ]
  then
    echo "File Does exist. Starting process..."
  else
    echo "File Does not exist. Exit "
    exit
  fi
fi

if [ -z "$SEARCH_STRING" ]
then
  echo "No search string. Exiting."
  exit_with_usage
else 
  echo "Search String: "$SEARCH_STRING
fi

if [ -z "$REPLACE_STRING" ]
then
  echo "No replace string. Exiting."
  exit_with_usage
else 
  echo "Replace String: "$REPLACE_STRING
fi

##############################################################
#Run

NEW_FILENAME=`echo $FILENAME | sed 's/\.jmx/_VarChange.jmx/g'`

SEARCH_RESULTS=(`grep 'SEARCH_STRING' $FILENAME`)
SEARCH_RESULTS_CNT=`grep '$SEARCH_STRING' $FILENAME | wc -l`

echo "Found following plugin entities in jmx file"

for result in "${SEARCH_RESULTS[@]}"
do
   echo $result
done

echo "Removing following:" $SEARCH_RESULTS_CNT

exit


if [ "${#SEARCH_RESULTS[@]}" -gt 0 ];then
  echo "Converting "$FILENAME" to "$NEW_FILENAME
  sed '/<kg.apc.jmeter/,/<hashTree>/d' $FILENAME > $NEW_FILENAME
fi

exit

