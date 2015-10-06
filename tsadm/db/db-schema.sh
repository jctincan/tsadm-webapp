#!/bin/bash
dbname='tsadmdevdb'
mydump_args='--opt --skip-comments --skip-set-charset'
echo 'SHOW TABLES' | mysql -BN $dbname | while read tname
do
    mysqldump $mydump_args -d $dbname $tname >schema/${tname}.tbl.sql
done
