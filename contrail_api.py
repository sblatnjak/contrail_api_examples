
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
VN = vnc_lib.virtual_network_read(fq_name=['default-domain', 'admin', 'test'])


RPs = vnc_lib.routing_policys_list()
RP1 = vnc_lib.routing_policy_read(fq_name=[u'default-domain', u'admin', u'My_Routing_Policy_1'])
RP2 = vnc_lib.routing_policy_read(fq_name=[u'default-domain', u'admin', u'My_Routing_Policy_2'])
RP3 = vnc_lib.routing_policy_read(fq_name=[u'default-domain', u'admin', u'My_Routing_Policy_3'])

 
rp1_attr = RoutingPolicyType(sequence='1.0')
rp2_attr = RoutingPolicyType(sequence='2.0')
rp3_attr = RoutingPolicyType(sequence='3.0')


VN.set_routing_policy(RP1, rp1_attr)

VN.set_routing_policy(RP1, rp1_attr)
VN.add_routing_policy(RP2, rp2_attr)
VN.add_routing_policy(RP3, rp3_attr)
VN.get_routing_policy_refs()
#[{'to': [u'default-domain', u'admin', u'My_Routing_Policy_1'], 'attr': sequence = 1.0, 'uuid': u'7bbd5323-81f0-46ac-ba68-020bb409b642'}, {'to': [u'default-domain', u'admin', u'My_Routing_Policy_2'], 'attr': sequence = 2.0, 'uuid': u'014e06d2-b739-4442-9422-3aa5c54e0e47'}, {'to': [u'default-domain', u'admin', u'My_Routing_Policy_3'], 'attr': sequence = 3.0, 'uuid': u'6d83cb00-522a-41b0-8c09-f79ebcb1cf73'}]

vnc_lib.virtual_network_update(VN)
#u'{"virtual-network": {"href": "https://overcloud-contrailcontroller-0.example.com:8082/virtual-network/58ec194e-8f59-4c06-b00e-dffd7be49bc1", "uuid": "58ec194e-8f59-4c06-b00e-dffd7be49bc1"}}'






