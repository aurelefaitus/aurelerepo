#!/bin/bash
# Script: Converts hard coded Windows paths in a jmeter jmx file
# to variable form to achieve platform agnostics scripts 
#########################################################
## Process paramters

exit_with_usage()
{
   echo "This script converts hard coded Windows paths in a jmeter jmx file to variable form to achieve platform agnostics scripts."
   echo " Example: C:\mypath\file to ${GUDV_TestDataPath}${PATH_SEP}file"
   echo "   "
   echo "Usage: convertWinPathsToVars.sh"
   echo "      -f <filename>"

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

#if [ -z "$SEARCH_STRING" ]
#then
#  echo "No search string. Exiting."
#  exit_with_usage
#else 
#  echo "Search String: "$SEARCH_STRING
#fi

#if [ -z "$REPLACE_STRING" ]
#then
#  echo "No replace string. Exiting."
#  exit_with_usage
#else 
#  echo "Replace String: "$REPLACE_STRING
#fi

##############################################################
#Run

NEW_FILENAME=`echo $FILENAME | sed 's/\.jmx/_PathChng.jmx/g'`

sed 's/C:.*JMX_CNG/${GUDV_TestDataPath}${PATH_SEP}JMX_CNG/g' $FILENAME > $NEW_FILENAME

sed -i 's/${GUDV_TestDataPath}\\/${GUDV_TestDataPath}${PATH_SEP}/g' $NEW_FILENAME

SEARCH_RESULTS=(`grep '\${GUDV_TestDataPath' $NEW_FILENAME | awk -F'}' '{print$3}' | awk -F'\' '{print$1}' | uniq`)
SEARCH_RESULTS_CNT=`grep '${GUDV_TestDataPath' $NEW_FILENAME | awk -F'}' '{print$3}' | awk -F'\' '{print$1}' | wc -l`

echo "Found "$SEARCH_RESULTS_CNT" hard coded paths in jmx file"

for result in "${SEARCH_RESULTS[@]}"
do
   echo $result
   CMD="sed -i 's/$result\\\/$result\${PATH_SEP}/g' $NEW_FILENAME"
   echo $CMD
   eval $CMD
   #grep $result $NEW_FILENAME
done

echo "Removing following:" $SEARCH_RESULTS_CNT
grep "PATH_SEP" $NEW_FILENAME
exit



