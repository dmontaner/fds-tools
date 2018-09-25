#!/bin/bash
# (>>>FILE<<<)
# (>>>ISO_DATE<<<) (>>>EMAIL<<<)
# (>>>COMMENT<<<)

source ../.job.conf

################################################################################

# Use this file as a template to extract data from impala into a tsv file.

# Parameters:
# - myquery  : the query you want to run.
#              Keep the single quotes here.
#              You can use double quotes within the query.
# - myoutfile: the file name you want to write.
#              Will be tab separated and gziped. Keep the .tsv.gz extension.
#              Will be written in your raw data folders according to config file.

cd $dir_rawdat

myquery='
SELECT *
FROM coll_cust_summary
WHERE cus_idr IN (SELECT DISTINCT cus_idr FROM coll_cust_summary ORDER BY cus_idr LIMIT 10)
AND data_for_month="201603"
ORDER BY cus_idr
;
'

myoutfile="transactions_per_day_demographics_201603.tsv.gz"

impala-shell -B --print_header -k --ssl -i optbukdev-odbc.gmail.intranet:21000 -d a_copd_db -q "$myquery" | gzip -c > $myoutfile

# EXIT
echo "Bash DONE SUCCESSFULLY"
