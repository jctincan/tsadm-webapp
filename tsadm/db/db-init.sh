set -e

mysqladmin drop tsadmtestdb
mysqladmin create tsadmtestdb

for fpath in schema/*.tbl.sql procedures/*.sql db-data.sql
do
    echo -n "  ${fpath} ... "
    mysql tsadmtestdb <$fpath
    echo "done"
done
