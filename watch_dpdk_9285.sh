#!/bin/bash

#CEM-9285
#https://github.com/Juniper/contrail-vrouter/blob/master/dpdk/vr_dpdk_lcore.c#L1805
#https://github.com/Juniper/contrail-vrouter/blob/R4.1/dpdk/vr_dpdk_netlink.c#L311
#dpdk loops while trying to init the communication socket with the agent
#dpdk logs gets filled (4 x 0.001 sec) with:
#timestamp VROUTER:     error creating NetLink server socket: Address already in use (98) 
#next step: we have to save dpdk logs (options: backup logs, cmd outputs + restart or just to OR just stop vrouter supervisor)!

#this script will run untill specific error message is found in dpdk logs
#exit  options:
#option1 when hit the error, this script will take backup of dpdk logs, cmd outputs, restart supervisor to fix the problem and exit
#option2 when hit the error, this script will not take backup of dpdk logs but will stop the supervisor service and exit
#
option1=true #option2=false 
#log paths
logs_to_search=/var/log/contrail/contrail-vrouter-dpdk*
back_logs_dir=/var/log/contrail/dpdk_backup/
#error messages
error_message="error creating NetLink server socket" #general message (vr_dpdk_netlink.c#L311); will end up with same logs behaviour
#error_message="Address already in use" #more specific message (vr_dpdk_netlink.c#L311) 

#functions to collect pids, mk bck dir
fun_add_processIDs_to_array()
{  
#collect pids from: ss -l -p -A 'netlink' | grep vro
ss -l -p -A 'netlink' | grep vro > $back_logs_dir"ss_output"
while IFS= read -r line
do
   IFS='/' read -r -a array <<< $line
   processID=${array[1]}
   processIDs+=( "$processID" )
done < <(ss -l -p -A 'netlink' | grep vro | awk '{print $4}')
} 
fun_create_backup_dir()
{
#mkdir backup dir for dpdk logs if not exist
if [[ ! -e $1 ]]; then
  mkdir $back_logs_dir
elif [[ ! -d $1 ]]; then
  echo "$1 already exists but is not a directory" 1>&2
fi
}
#end functions

if [ option1 ]
then
  #mkdir backup dir for dpdk logs if not exist
  fun_create_backup_dir
fi

processIDs=()
while true; 
do
  #don't search if at least .5 dpdk log was not generated
  ls -al /var/log/contrail/contrail-vrouter-dpdk-stdout.log.5 > /dev/null
  if [ $? -eq 0 ];
  then
    #search dpdk logs for error message
    #if grep -rin "error creating NetLink server socket" /var/log/contrail/contrail-vrouter-dpdk* > /dev/null ;
    if grep -rin "$error_message" $logs_to_search > /dev/null ;
    then
      if [ option1 ]
      then
        echo "Detected error message:'$error_message' in $logs_to_search, backup files and cmd outputs, restart vrouter, exit"; 
        cp -v $logs_to_search $back_logs_dir
        #get more data
        #fun_create_backup_dir $back_logs_dir #no need for this in option1
        fun_add_processIDs_to_array
        for i in "${processIDs[@]}"  
        do  
            ps aux | grep $i > $back_logs_dir"ps_aux_proc_"$i
            lsof -Pn -p $i > $back_logs_dir"lsof_proc_"$i
            netstat -anlp | grep $i > $back_logs_dir"netstat_proc_"$i

        done 
        #end get more data
        service supervisor-vrouter restart
        exit 0
      else #option2; stop services
        service supervisor-vrouter stop
        echo "Detected error message:'$error_message' in $logs_to_search, stop vrouter, exit"
        exit 0
      fi
    fi
  fi
  sleep 60
done
