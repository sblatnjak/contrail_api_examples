#!/bin/bash

#get metadata IPs
#add metadata flow IDs to flow_IDs
#get VM IP from metadata flow
#add VM flow IDs to flow_IDs
#get all flows from flow_IDs

metadata_IPs=()
VM_overlay_IPs=()
metadata_flow_IDs=()
vm_flow_IDs=()
flow_IDs=()
flows=()


get_metadata_IPs_list()
{
  while IFS= read -r line
  do
    IFS='/' read -r -a array <<< $line
    metadata_IP=${array[0]}
    metadata_IPs+=("$metadata_IP")
  done < <(ps -ef | grep agent-health | awk -F"-d" '{print $2}' | awk -F"-t" '{print $1}')
}
get_metadata_flow_ID_list()
{
  metadata_flow_IDs+=("$(flow -l --match "$1" | tail -5 | head -1 | awk -F"<=>" '{print $1}')")
}
get_VM_IPs_list()
{
  VM_overlay_IP=("$(flow --get "$1" | grep "Destination Information" -A 3 | grep "Matching Route" | awk -F':' '{print $2}')")
  VM_overlay_IPs+=("$(echo "$VM_overlay_IP" | awk -F"/" '{print $1}')")
}
get_VM_flow_ID_list()
{
  VM_flow_IDs+=("$(flow -l --match "$1" | tail -5 | head -1 | awk -F"<=>" '{print $1}')")
}
get_flows()
{
  flows+=("$(flow --get "$1")")
}

#get metadata IPs
get_metadata_IPs_list

##add metadata flow IDs to metadata_flow_IDs
for i in "${!metadata_IPs[@]}"; do
  if [ ! -z "${metadata_IPs[$i]}" ]; then
    get_metadata_flow_ID_list ${metadata_IPs[$i]}
  fi
done

##get VM IP from metadata flow
for i in "${!metadata_flow_IDs[@]}"; do
  if [ ! -z "${metadata_flow_IDs[$i]}" ]; then
    get_VM_IPs_list ${metadata_flow_IDs[$i]}
  fi
done

#add VM flow IDs to VM_flow_IDs
for i in "${!VM_overlay_IPs[@]}"; do
  if [ ! -z "${VM_overlay_IPs[$i]}" ]; then
    get_VM_flow_ID_list ${VM_overlay_IPs[$i]}
  fi
done

#VM + metadata flow_IDs
flow_IDs=("${metadata_flow_IDs[@]}" "${VM_flow_IDs[@]}")

for i in "${!flow_IDs[@]}"; do
  get_flows ${flow_IDs[$i]}
done

echo "Metadata_IPs: ${metadata_IPs[@]}" 
echo "VM_IPs: ${VM_overlay_IPs[@]}" 
echo "flow_IDs: ${flow_IDs[@]}"
echo "flows: ${flows[@]}" 
