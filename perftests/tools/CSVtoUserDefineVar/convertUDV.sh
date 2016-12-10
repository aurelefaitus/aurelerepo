#!/bin/bash
# Script: convert a user defined variable csv into a UserDefinedElement in a jmeter file
#########################################################
## Process paramters

exit_with_usage()
{
   echo "Usage: convertUDV.sh"
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

NEW_FILENAME=`echo $FILENAME | sed 's/csv/jmx/g' | sed 's/CSV/jmx/g'`
echo $NEW_FILENAME

cat header.tpl > $NEW_FILENAME 

OLDIFS=$IFS
IFS=,
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }
while read name value
do
	echo "Name : $name"
	echo "Value : $value"
        cp element.tpl temp.tpl
        SED1_CMD="sed -i 's/VAR_NAME/$name/g' temp.tpl"
        SED2_CMD="sed -i 's/VAR_VAL/$value/g' temp.tpl"
        eval $SED1_CMD
        eval $SED2_CMD
        cat temp.tpl >> $NEW_FILENAME
        rm temp.tpl
done < $FILENAME
IFS=$OLDIFS

cat footer.tpl >> $NEW_FILENAME

exit

