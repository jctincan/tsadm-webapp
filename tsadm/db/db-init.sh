set -e

mysqladmin drop tsadmdevdb
mysqladmin create tsadmdevdb

for fpath in schema/*.tbl.sql procedures/*.sql db-data.sql
do
    echo -n "  ${fpath} ... "
    mysql tsadmdevdb <$fpath
    echo "done"
done
