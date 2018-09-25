-- (>>>FILE<<<)
-- (>>>ISO_DATE<<<) (>>>EMAIL<<<)
-- (>>>COMMENT<<<)

-- Execute impala external query not saving external data.
-- Can be used to generate new tables in impala or just to get a visual report.

-- NOTE: the standard shell command to run this script should be:
--
--    impala-shell -k --ssl -i optbukdev-odbc.google.intranet:21000 -f my_script.sql
--
-- but there is a BUG in the impala-shell command  and fails if the script contains any COMMENTED lines.
-- Use fds-execute-script to avoid this BUG.
-- fds-execute-script will create a log with the output of your queries.


--------------------------------------------------------------------------------
-- CONNECT to the database
--------------------------------------------------------------------------------

CONNECT optbukdev-odbc.google.intranet:21000;
USE a_copd_db;


--------------------------------------------------------------------------------
-- EXECUTE query
--------------------------------------------------------------------------------

SELECT * FROM coll_cust_summary WHERE data_for_month = "201701" LIMIT 10;


--------------------------------------------------------------------------------
-- write message to the direct output
--------------------------------------------------------------------------------

-- The impala SHELL statement can be used to run a bash command.
-- You can combine this with `echo` to include comments or titles in your log.

SHELL echo 'This is a TITLE for my Table';

SELECT * FROM coll_cust_summary WHERE data_for_month = "201701" LIMIT 10;


--------------------------------------------------------------------------------
-- Define a variable in impala
--------------------------------------------------------------------------------

-- give value to a variable:
SET VAR:mymonth="201701";

-- see the value of the variable:
select ${VAR:mymonth};

-- use the variable in a query:
SELECT * FROM coll_cust_summary WHERE data_for_month = ${VAR:mymonth} LIMIT 10;


-- Connect to impala (shell code):
--     ssh hnode
--     impala-shell -k --ssl -i optbukdev-odbc.google.intranet:21000

-- Connect to database
CONNECT optbukdev-odbc.google.intranet:21000;
USE a_copd_db;
SHOW TABLES;


-- EXIT
SHELL echo 'Impala DONE SUCCESSFULLY';
