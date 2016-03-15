#!/bin/sh
suffix=`date "+%Y%m%d%k"`
log_name=$1'.'$suffix
if [ -f $1 ];then
    mv $1 $log_name
fi
