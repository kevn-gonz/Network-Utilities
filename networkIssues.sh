#!/bin/bash

logpath=$(dirname "$(realpath $0)")
hostsfile=$logpath/hosts.txt

mkdir -p $logpath/temp

parallel -j8 -k "ping -c5 {} >> $logpath/temp/ping.{}.out; echo $'\n\n' >> $logpath/temp/ping.{}.out;" :::: $hostsfile
parallel -j8 -k "traceroute {} >> $logpath/temp/traceroute.{}.out; echo $'\n\n' >> $logpath/temp/traceroute.{}.out;" :::: $hostsfile
parallel -j8 -k "echo 'Mtr to {}...' >> $logpath/temp/mtr.{}.out;  mtr --report --report-cycles 5 {} >> $logpath/temp/mtr.{}.out; echo $'\n\n' >> $logpath/temp/mtr.{}.out;" :::: $hostsfile
wait #waiting for parallel to complete all processes

cat temp/ping.* >> ping.txt 2>/dev/null
cat temp/traceroute.* >> traceroute.txt 2>/dev/null
cat temp/mtr.* >> mtr.txt 2>/dev/null

rm -rf $logpath/temp/
echo 'complete!'

