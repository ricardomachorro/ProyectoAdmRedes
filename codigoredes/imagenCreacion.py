from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
from collections import namedtuple
from graphviz import Digraph

Router = namedtuple('Router', ['destination_host', 'management_ip'])

def show_cdp(ip):
    device = {
        'device_type': 'cisco_ios_telnet',
        'host': ip,
        'username':'cisco',
        'password': 'cisco'
    }
    
    try:
        print("paso 1")
        with ConnectHandler(**device) as telnet:
            print("paso 2")
            return telnet.send_command('show cdp neighbors detail', use_textfsm=True)
    except NetmikoAuthenticationException:
        print('Authentication error')
    except NetmikoTimeoutException:
        print('Timeout error')
    except Exception as e:
        print(e)

def get_topology(main_router):
    routers = []
    next_router = [main_router]
    visited_routers = [main_router.destination_host]
    network = Digraph(comment='Network',format="png",directory="static/")

    while next_router:
        router = next_router.pop(0)
        routers.append(router)
        network.node(router.destination_host)
        print(show_cdp(router.management_ip))
        for neighbor in show_cdp(router.management_ip):
            network.edge(router.destination_host, neighbor['destination_host'])
            if neighbor['destination_host'] not in visited_routers:
                visited_routers.append(neighbor['destination_host'])
                next_router.append(Router(neighbor['destination_host'], neighbor['management_ip']))
    return routers, network


def hacer_imagen():
    main_router = Router('R1', ' 10.0.0.254 ')
    routers, topology = get_topology(main_router)
    for router in routers:
        print(router)
    print(topology.source)
    topology.render('topology')
    
    
    
    
    
    
    
    
    
