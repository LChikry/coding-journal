portnames = ["PAN", "AMS", "CAS", "NYC", "HEL"]

# https://sea-distances.org/
# nautical miles converted to km

D = [
        [0,8943,8019,3652,10545],
        [8943,0,2619,6317,2078],
        [8019,2619,0,5836,4939],
        [3652,6317,5836,0,7825],
        [10545,2078,4939,7825,0]
    ]

# https://timeforchange.org/co2-emissions-shipping-goods
# assume 20g per km per metric ton (of pineapples)

co2 = 0.020

# DATA BLOCK ENDS

# these variables are initialised to nonsensical values
# your program should determine the correct values for them
smallest = 1000000
bestroute = [0, 0, 0, 0, 0]

def permutations(route, ports):
    global smallest, bestroute
    if not ports or len(ports) == 0:
        emit = get_emissions(route)
        if smallest < emit: return
        smallest = emit
        bestroute = route.copy()
        return

    for i in range(len(ports)):
        new_route = route + [ports[i]]
        new_ports = ports[:i] + ports[i+1:]
        permutations(new_route, new_ports)


def get_emissions(route):
    dist = 0
    for i in range(len(route)-1):
        dist += D[route[i]][route[i+1]]

    return dist * co2


def main():
    # Do not edit any (global) variables using this function, as it will mess up the testing

    # this will start the recursion 
    permutations([0], list(range(1, len(portnames))))

    # print the best route and its emissions
    print(' '.join([portnames[i] for i in bestroute]) + " %.1f kg" % smallest)

main()