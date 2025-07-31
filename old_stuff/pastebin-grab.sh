#!/bin/bash
site=`cat pastebin-site`
grab=`curl -s  "$site"| grep grabme | grep -oE "grabme(\w*?@[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3})endgrab"`
#echo "$grab" | grep -cP "(?<=grabme)(\w*@.*[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3})"
grab=`echo "$grab" | grep -oP "(?<=grabme)(\w*?@[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3})"`
grab=`echo "$grab" | xargs -d " " echo`

for i in $(seq 1 `echo -e "$grab" | wc -l`)
do
    thisline=`echo "$grab" | head -n $i | tail -n 1`
    
    if ! ./contains "$trustedaddrs" "$thisline"
    then
        trustedaddrs+=" "
        trustedaddrs+="$thisline"
    fi
done
trustedaddrs=`echo "$trustedaddrs" | sed "s/ /\n/g"`
#echo -e "$trustedaddrs"
echo -e "$trustedaddrs" | tail -n +2
