set -e

RUN_MODE=dev

mysqladmin drop tsadm${RUN_MODE}db
mysqladmin create tsadm${RUN_MODE}db

for fpath in schema/*.tbl.sql procedures/*.sql db-${RUN_MODE}data.sql
do
    echo -n "  ${fpath} ... "
    mysql tsadm${RUN_MODE}db <$fpath
    echo "done"
done
