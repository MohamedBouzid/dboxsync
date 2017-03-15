#!/bin/bash


# start mongodb service
sudo service mongod start &

# Verify the existance of one parmeter 
while [ "$#" -ne "2" ]
do

	echo "Saisissez un paramètre"	
	return
done

# Do the job
/usr/bin/python dboxsync.py $1 $2 &


