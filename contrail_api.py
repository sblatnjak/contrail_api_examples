
#! /usr/bin/python 
#/usr/lib/python2.7/site-packages/schema_transformer
#test RP https://github.com/Juniper/contrail-controller/blob/master/src/config/schema-transformer/test/test_service_policy.py

from vnc_api import vnc_api 
import pprint 
import pdb 
from vnc_api.vnc_api import (VirtualNetwork, SequenceType, VirtualNetworkType,
        VirtualNetworkPolicyType, NoIdError, NetworkIpam, VirtualMachine,
        VnSubnetsType, IpamSubnetType, SubnetType, FloatingIpPool,
        FloatingIp, VirtualMachineInterfacePropertiesType, PortType,
        VirtualMachineInterface, InterfaceMirrorType, MirrorActionType,
        ServiceChainInfo, RoutingPolicy, RoutingPolicyServiceInstanceType,
        RouteListType, RouteAggregate,RouteTargetList, ServiceInterfaceTag,
        PolicyBasedForwardingRuleType, RoutingPolicyType)


#  non tls 
vnc_lib = vnc_api.VncApi(api_server_host='10.1.0.35', auth_host='10.1.0.21',api_server_port='8082',username='admin', password='D6QMVufER4GgmNWFDkwBNTg8A',tenant_name = 'admin')

#haproxy listen keystone_admin to get auth_host
vnc_lib = vnc_api.VncApi(api_server_host='overcloud-contrailcontroller-0.example.com', auth_host='overcloud-controller-0.ctlplane.example.com'
,api_server_port='8082',username='admin', password='D6QMVufER4GgmNWFDkwBNTg8A',tenant_name = 'admin', apicertfile='/etc/contrail/ssl/certs/server.pem', apikeyfile='/etc/contrail/ssl/private/server-privkey.pem',domain_name='default')

#taking keys from config 
vnc_lib = vnc_api.VncApi(api_server_host='overcloud-contrailcontroller-0.example.com', auth_host='overcloud-controller-0.ctlplane.example.com',api_server_port='8082',username='admin', password='D6QMVufER4GgmNWFDkwBNTg8A',tenant_name = 'admin',domain_name='default')



VNs =  vnc_lib.virtual_networks_list()
VN = vnc_lib.virtual_network_read(fq_name=['default-domain', 'admin', 'net-1'])


RPs = vnc_lib.routing_policys_list()
RP1 = vnc_lib.routing_policy_read(fq_name=[u'default-domain', u'admin', u'My_Routing_Policy_1'])
RP2 = vnc_lib.routing_policy_read(fq_name=[u'default-domain', u'admin', u'My_Routing_Policy_2'])
RP3 = vnc_lib.routing_policy_read(fq_name=[u'default-domain', u'admin', u'My_Routing_Policy_3'])
RP4 = vnc_lib.routing_policy_read(fq_name=[u'default-domain', u'admin', u'My_Routing_Policy_4'])

 
rp1_attr = RoutingPolicyType(sequence='1.0')
rp2_attr = RoutingPolicyType(sequence='2.0')
rp3_attr = RoutingPolicyType(sequence='3.0')
rp4_attr = RoutingPolicyType(sequence='4.0')


VN.set_routing_policy(RP1, rp1_attr)

VN.set_routing_policy(RP1, rp1_attr)
VN.add_routing_policy(RP2, rp2_attr)
VN.add_routing_policy(RP3, rp3_attr)
VN.add_routing_policy(RP4, rp4_attr)


#>>> VN.get_routing_policy_refs()
#[{'to': [u'default-domain', u'admin', u'My_Routing_Policy_1'], 'attr': sequence = 1.0, 'uuid': u'7bbd5323-81f0-46ac-ba68-020bb409b642'}, {'to': [u'default-domain', u'admin', u'My_Routing_Policy_2'], 'attr': sequence = 2.0, 'uuid': u'014e06d2-b739-4442-9422-3aa5c54e0e47'}, {'to': [u'default-domain', u'admin', u'My_Routing_Policy_3'], 'attr': sequence = 3.0, 'uuid': u'6d83cb00-522a-41b0-8c09-f79ebcb1cf73'}, {'to': [u'default-domain', u'admin', u'My_Routing_Policy_4'], 'attr': sequence = 4.0, 'uuid': u'e977a248-1897-4bee-a078-efda3e95692e'}]



>>> RP1.routing_policy_entries
term = [term_match_condition = protocol = [u'static'], prefix = [], community = None, community_list = [], community_match_all = False, extcommunity_list = [], extcommunity_match_all = None, term_action_list = update = as_path = None, community = None, extcommunity = None, local_pref = None, med = 101, action = next]
>>> RP2.routing_policy_entries
term = [term_match_condition = protocol = [u'static'], prefix = [], community = None, community_list = [], community_match_all = False, extcommunity_list = [], extcommunity_match_all = None, term_action_list = update = as_path = None, community = None, extcommunity = None, local_pref = 102, med = None, action = next]
>>> RP3.routing_policy_entries
term = [term_match_condition = protocol = [u'static'], prefix = [], community = None, community_list = [], community_match_all = False, extcommunity_list = [], extcommunity_match_all = None, term_action_list = update = as_path = None, community = add = community = [u'999:103'], remove = None, set = None, extcommunity = None, local_pref = None, med = None, action = next]
>>> RP4.routing_policy_entries
term = [term_match_condition = protocol = [u'static'], prefix = [], community = None, community_list = [], community_match_all = False, extcommunity_list = [], extcommunity_match_all = None, term_action_list = update = as_path = expand = asn_list = [65004], community = None, extcommunity = None, local_pref = None, med = None, action = accept]


#####RESULT#######
VN config :
{
  "virtual-network": {
    "parent_uuid": "c9ea6875-ebe4-4c98-bf4f-2e4135e25837",
    "address_allocation_mode": "user-defined-subnet-only",
    "parent_type": "project",
    "route_target_list": {},
    "route_table_refs": [
      {
        "to": [
          "default-domain",
          "admin",
          "My_Net_Route_table"
        ],
        "href": "https://overcloud-contrailcontroller-0.internalapi.example.com:8082/route-table/7d9bcd4b-3ee1-4ec4-a425-7cd9cd7a56af",
        "attr": null,
        "uuid": "7d9bcd4b-3ee1-4ec4-a425-7cd9cd7a56af"
      }
    ],
    "mac_learning_enabled": false,
    "fabric_snat": false,
    "pbb_etree_enable": false,
    "fq_name": [
      "default-domain",
      "admin",
      "net-1"
    ],
    "uuid": "845315d9-a33d-474f-b7a1-feaa85769034",
    "id_perms": {
      "enable": true,
      "description": null,
      "creator": null,
      "created": "2019-05-16T18:55:07.641703",
      "user_visible": true,
      "last_modified": "2019-06-18T14:51:55.719175",
      "permissions": {
        "owner": "admin",
        "owner_access": 7,
        "other_access": 7,
        "group": "admin",
        "group_access": 7
      },
      "uuid": {
        "uuid_mslong": 9534988860564260000,
        "uuid_lslong": 13232137188528263000
      }
    },
    "routing_policy_refs": [
      {
        "to": [
          "default-domain",
          "admin",
          "My_Routing_Policy_1"
        ],
        "href": "https://overcloud-contrailcontroller-0.internalapi.example.com:8082/routing-policy/7bbd5323-81f0-46ac-ba68-020bb409b642",
        "attr": {
          "sequence": "1.0"
        },
        "uuid": "7bbd5323-81f0-46ac-ba68-020bb409b642"
      },
      {
        "to": [
          "default-domain",
          "admin",
          "My_Routing_Policy_3"
        ],
        "href": "https://overcloud-contrailcontroller-0.internalapi.example.com:8082/routing-policy/6d83cb00-522a-41b0-8c09-f79ebcb1cf73",
        "attr": {
          "sequence": "3.0"
        },
        "uuid": "6d83cb00-522a-41b0-8c09-f79ebcb1cf73"
      },
      {
        "to": [
          "default-domain",
          "admin",
          "My_Routing_Policy_4"
        ],
        "href": "https://overcloud-contrailcontroller-0.internalapi.example.com:8082/routing-policy/e977a248-1897-4bee-a078-efda3e95692e",
        "attr": {
          "sequence": "4.0"
        },
        "uuid": "e977a248-1897-4bee-a078-efda3e95692e"
      },
      {
        "to": [
          "default-domain",
          "admin",
          "My_Routing_Policy_2"
        ],
        "href": "https://overcloud-contrailcontroller-0.internalapi.example.com:8082/routing-policy/014e06d2-b739-4442-9422-3aa5c54e0e47",
        "attr": {
          "sequence": "2.0"
        },
        "uuid": "014e06d2-b739-4442-9422-3aa5c54e0e47"
      }
    ],
    "instance_ip_back_refs": [
      {
        "to": [
          "e98ee9bd-5454-46ac-a9dd-ec27c56bf839"
        ],
        "href": "https://overcloud-contrailcontroller-0.internalapi.example.com:8082/instance-ip/e98ee9bd-5454-46ac-a9dd-ec27c56bf839",
        "attr": null,
        "uuid": "e98ee9bd-5454-46ac-a9dd-ec27c56bf839"
      },
      {
        "to": [
          "960781f6-b243-4c38-9f0a-99b43682c7f8"
        ],
        "href": "https://overcloud-contrailcontroller-0.internalapi.example.com:8082/instance-ip/960781f6-b243-4c38-9f0a-99b43682c7f8",
        "attr": null,
        "uuid": "960781f6-b243-4c38-9f0a-99b43682c7f8"
      }
    ],
    "multi_policy_service_chains_enabled": false,
    "virtual_network_properties": {
      "mirror_destination": false,
      "allow_transit": false,
      "rpf": "enable"
    },
    "ecmp_hashing_include_fields": {},
    "virtual_machine_interface_back_refs": [
      {
        "to": [
          "default-domain",
          "admin",
          "b3e108b0-0f57-48fd-ab74-05a1d0b25e88"
        ],
        "href": "https://overcloud-contrailcontroller-0.internalapi.example.com:8082/virtual-machine-interface/b3e108b0-0f57-48fd-ab74-05a1d0b25e88",
        "attr": null,
        "uuid": "b3e108b0-0f57-48fd-ab74-05a1d0b25e88"
      },
      {
        "to": [
          "default-domain",
          "admin",
          "sub_interface_net-1"
        ],
        "href": "https://overcloud-contrailcontroller-0.internalapi.example.com:8082/virtual-machine-interface/3423d1e7-cd93-464b-95dd-23254023e8bc",
        "attr": null,
        "uuid": "3423d1e7-cd93-464b-95dd-23254023e8bc"
      }
    ],
    "network_policy_refs": [
      {
        "to": [
          "default-domain",
          "admin",
          "all"
        ],
        "href": "https://overcloud-contrailcontroller-0.internalapi.example.com:8082/network-policy/dcd9ce58-ed53-4dc3-bbdc-b9aeb05fa2a2",
        "attr": {
          "timer": null,
          "sequence": {
            "major": 0,
            "minor": 0
          }
        },
        "uuid": "dcd9ce58-ed53-4dc3-bbdc-b9aeb05fa2a2"
      }
    ],
    "parent_href": "https://overcloud-contrailcontroller-0.internalapi.example.com:8082/project/c9ea6875-ebe4-4c98-bf4f-2e4135e25837",
    "import_route_target_list": {},
    "perms2": {
      "owner": "c9ea6875ebe44c98bf4f2e4135e25837",
      "owner_access": 7,
      "global_access": 0,
      "share": []
    },
    "display_name": "net-1",
    "routing_instances": [
      {
        "to": [
          "default-domain",
          "admin",
          "net-1",
          "net-1"
        ],
        "href": "https://overcloud-contrailcontroller-0.internalapi.example.com:8082/routing-instance/d44df5b8-acce-49e2-aa78-a33a2f2ce023",
        "uuid": "d44df5b8-acce-49e2-aa78-a33a2f2ce023"
      }
    ],
    "virtual_network_network_id": 6,
    "provider_properties": null,
    "name": "net-1",
    "access_control_lists": [
      {
        "to": [
          "default-domain",
          "admin",
          "net-1",
          "net-1"
        ],
        "href": "https://overcloud-contrailcontroller-0.internalapi.example.com:8082/access-control-list/1e253fe1-8220-4947-ba7e-d6c475fcad74",
        "uuid": "1e253fe1-8220-4947-ba7e-d6c475fcad74"
      }
    ],
    "export_route_target_list": {},
    "router_external": false,
    "pbb_evpn_enable": false,
    "href": "https://overcloud-contrailcontroller-0.internalapi.example.com:8082/virtual-network/845315d9-a33d-474f-b7a1-feaa85769034",
    "flood_unknown_unicast": false,
    "layer2_control_word": false,
    "network_ipam_refs": [
      {
        "to": [
          "default-domain",
          "default-project",
          "default-network-ipam"
        ],
        "href": "https://overcloud-contrailcontroller-0.internalapi.example.com:8082/network-ipam/82aadead-20b4-40f9-9a56-851545565d21",
        "attr": {
          "ipam_subnets": [
            {
              "subnet": {
                "ip_prefix": "192.168.1.0",
                "ip_prefix_len": 24
              },
              "dns_server_address": "192.168.1.2",
              "enable_dhcp": true,
              "default_gateway": "192.168.1.1",
              "subnet_uuid": "80762d22-cfa2-4e8f-b75f-d7db4d89c25b",
              "subnet_name": "80762d22-cfa2-4e8f-b75f-d7db4d89c25b",
              "addr_from_start": true
            },
            {
              "subnet": {
                "ip_prefix": "10.0.0.0",
                "ip_prefix_len": 24
              },
              "dns_server_address": "10.0.0.2",
              "enable_dhcp": true,
              "default_gateway": "10.0.0.1",
              "subnet_uuid": "45cc2677-5b25-4315-91c1-adc72e85550e",
              "subnet_name": "45cc2677-5b25-4315-91c1-adc72e85550e",
              "addr_from_start": true
            }
          ]
        },
        "uuid": "82aadead-20b4-40f9-9a56-851545565d21"
      }
    ],
    "is_shared": false
  }
}



https://overcloud.example.com:8143/#p=mon_infra_control&q%5Btype%5D=controlNode&q%5Bview%5D=details&q%5BfocusedElement%5D%5Bnode%5D=overcloud-contrailcontroller-0.example.com&q%5BfocusedElement%5D%5Btab%5D=details&q%5Btab%5D%5Bcontrol_nodes_details-tab%5D=control_node_routes_grid_view

15.0.0.0/24 StaticRoute (static) 10.1.0.43 28  - default-domain:admin:net-1

{

    protocol: StaticRoute (static)
    last_modified: 2019-Jun-18 14:50:04.268553
    local_preference: 102
    med: 101
    local_as: 0
    peer_as: 0
    peer_router_id: 
    source: 
    as_path: 65004
    as4_path: 
    next_hop: 10.1.0.43
    label: 28
    origin: incomplete
    replicated: false
    primary_table: 
    secondary_tables:  {
        list:  { ... }
    }
    communities:  {
        list:  {
            element:  [
                999:101
                999:103
                accept-own-nexthop
                encapsulation:gre
                encapsulation:udp
                mobility:non-sticky:1
                secgroup:64515:8000002
                originvn:64515:6
            ]
        }
    }
    origin_vn: default-domain:admin:net-1
...

