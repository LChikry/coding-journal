portnames = ["PAN", "AMS", "CAS", "NYC", "HEL"]

def permutations(route, ports):
    if len(ports) == 0 or not ports:
        print(' '.join([portnames[i] for i in route]))
        return
    
    for i in range(len(ports)):
        new_route = route + [ports[i]]
        left_ports = ports[:i] + ports[i+1:]
        permutations(new_route, left_ports)


# This will start the recursion with 0 ("PAN") as the first stop
permutations([0], list(range(1, len(portnames))))