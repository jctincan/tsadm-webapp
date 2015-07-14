set -e
dbname='tsadmdevdb'
dbversion=$(echo 'SELECT `dbversion` FROM `tsadm`;' | mysql -BN ${dbname})
echo "dbversion ${dbversion}"
for upversion in $(ls upgrade/ | cut -d'.' -f1 | sort -u)
do
    if test ${dbversion} -lt ${upversion}
    then
        echo -n "upgrade to ${upversion}, using "
        if test -s upgrade/${upversion}.bash
        then
            echo -n "bash"
            bash upgrade/${upversion}.bash | mysql -BN ${dbname}
        elif test -s upgrade/${upversion}.sql
        then
            echo -n "sql"
            mysql -BN ${dbname} <upgrade/${upversion}.sql
        fi
        echo " done!"
    fi
done
