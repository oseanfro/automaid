
#!/bin/bash
AUTOMAID_LINK=$1

PROCESS_SOURCE="${AUTOMAID_LINK}/processed"
SCRIPT_SOURCE="${AUTOMAID_LINK}/scripts/main.py"

REMOVE_PROCESS="${PROCESS_SOURCE}/*"

if [ -d $PROCESS_SOURCE ];then
rm -rf $REMOVE_PROCESS
fi

cd $AUTOMAID_LINK
python ./scripts/main.py 2>&1

echo "finished"

