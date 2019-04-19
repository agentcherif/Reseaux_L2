#!/bin/bash

NBCLIENTS=2 # default
[ $# -eq 1 ] && NBCLIENTS=$1

[ ! -f server.py ] && echo "File server.py not found!" && exit 0
[ ! -f client.py ] && echo "File client.py not found!" && exit 0

# launch server
xterm -hold -T server -e python3 -u server.py &
SERVERPID=$!
sleep 1

# launch clients
for NUMCLIENT in $(seq $NBCLIENTS) ; do
    ID="client$NUMCLIENT"
    xterm -hold -T $ID -e bash -c 'python3 -u client.py' &
    CLIENTPIDS="$!"
done

trap 'kill $CLIENTPIDS $SERVERPID &> /dev/null' EXIT
echo "Press Ctrl-C to quit..."
wait $CLIENTPIDS

# EOF
