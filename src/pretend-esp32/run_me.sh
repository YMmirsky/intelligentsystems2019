#!/bin/bash

for arg in "$@"
do
	if [ "$arg" == "--help" ] || [ "$arg" == "-h" ]
	then
		echo "Usage:"
		echo -e "\t $ ./run_me.sh <script.py> <host> <port>"
		exit 1
	fi
done

if [ -z "$1" ]
then
	echo "Usage:"
	echo -e "\t $ ./run_me.sh <script.py> <host> <port>"
	exit 1
fi

export FLASK_APP=$1
python -m flask run --host=$2 --port=$3