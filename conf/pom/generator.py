import math
import random
import sys


ips = []


def generate_traces(client, limit, proto, plength, interleave, flows_per_client, pkt_per_flow, file_location, trace_loc, src_eth, dst_eth, dst_ip, trace_name=None):

    for c in range(client):
        done=False
        while not done:
            p1 = 10
            p2 = 0
            p1 = random.randrange(1, 255)
            p2 = random.randrange(1, 255)
            p3 = random.randrange(1, 255)
            p4 = random.randrange(1, 255)

            src = str(p1) +"."+ str(p2) +"."+ str(p3) +"."+ str(p4)
            if not ips.__contains__(src):
                done=True

        ips.append(src)

    if trace_name is None:
        trace_name = trace_loc + "/trace-" + proto + "-C" + str(client) + "-I" + str(interleave) + "-F" + str(flows_per_client) + ".pcap"
    # show number of flows in click filename
    file_name = "flow-" + str(client) + "-" + "interleave-" + str(interleave) + ".click"
    file = open(file_location + file_name , "w+")
    file.write('td :: ToDump("' + trace_name + '");\n')
    file.write('rr :: RoundRobinMultiSched(N ' + str(interleave) + ') -> Unqueue -> td;\n')

    random.shuffle(ips)
    for c in range(client):
        file.write(
            "Fast" + proto + "Flows(RATE 0, LENGTH " + str(plength) + ", LIMIT "+ str(int(limit/client)) +", SRCETH "+ src_eth +", SRCIP " + ips[c] +
            ", DSTETH "+dst_eth+", DSTIP "+dst_ip+", FLOWS "+flows_per_client+", FLOWSIZE "+pkt_per_flow+", STOP true)"
            " -> NumberPacket(OFFSET 52) -> [" + str(c) + "]rr;\n"
        )

    file.close()
    print("trace configurations generated: " + file_location + file_name)
    return

def generate_traces_sequential(client, limit, proto, plength, interleave, flows_per_client, pkt_per_flow, file_location, trace_loc, src_eth, dst_eth, dst_ip, trace_name=None, intertwine=True):
    # Forge traffic to roll against a striding fashion: odd goes first, and then even
    p1 = 192
    p2 = 168
    if client >= 65536:
        print("State space above 65536 is currently not supported")
        print("consider making the whole IP/port field configurable")
        exit(-1)

    # intertwine of 2
    ip_odd = []
    ip_even = []

    for i in range(0, client, 2):
        p3 = i >> 8
        p4 = i % 256
        src = str(p1) +"."+ str(p2) +"."+ str(p3) +"."+ str(p4)
        ip_odd.append(src)

    for i in range(1, client, 2):
        p3 = i >> 8
        p4 = i % 256
        src = str(p1) +"."+ str(p2) +"."+ str(p3) +"."+ str(p4)
        ip_even.append(src)
    
    # intertwine of 4
    # ip_1 = []
    # ip_2 = []
    # ip_3 = []
    # ip_4 = []
    # for i in range(0, client, 4):
    #     p3 = i >> 8
    #     p4 = i % 256
    #     src = str(p1) +"."+ str(p2) +"."+ str(p3) +"."+ str(p4)
    #     ip_1.append(src)

    # for i in range(1, client, 4):
    #     p3 = i >> 8
    #     p4 = i % 256
    #     src = str(p1) +"."+ str(p2) +"."+ str(p3) +"."+ str(p4)
    #     ip_2.append(src)
    
    # for i in range(2, client, 4):
    #     p3 = i >> 8
    #     p4 = i % 256
    #     src = str(p1) +"."+ str(p2) +"."+ str(p3) +"."+ str(p4)
    #     ip_3.append(src)
    
    # for i in range(3, client, 4):
    #     p3 = i >> 8
    #     p4 = i % 256
    #     src = str(p1) +"."+ str(p2) +"."+ str(p3) +"."+ str(p4)
    #     ip_4.append(src)

    if trace_name is None:
        trace_name = trace_loc + "/trace-" + proto + "-C" + str(client) + "-I" + str(interleave) + "-F" + str(flows_per_client) + "-seq"
        if intertwine == False:
            trace_name += ".pcap"
        else:
            trace_name += "-intw.pcap"
    # show number of flows in click filename
    file_name = "flow-" + str(client) + "-" + "interleave-" + str(interleave) + "-seq"
    if intertwine == False:
        file_name += ".click"
    else:
        file_name += "-intw.click"
    file = open(file_location + file_name , "w+")
    file.write('td :: ToDump("' + trace_name + '");\n')
    file.write('rr :: RoundRobinMultiSched(N ' + str(interleave) + ') -> Unqueue -> td;\n')

    # random.shuffle(ips)
    if intertwine == False:
        # Nah, I don't really care about performance here
        for i in range(int(client/2)):
            ips.append(ip_odd[i])
            ips.append(ip_even[i])
    else:
        ips.extend(ip_odd)
        ips.extend(ip_even)

        # ips.extend(ip_1)
        # ips.extend(ip_2)
        # ips.extend(ip_3)
        # ips.extend(ip_4)
    
    for c in range(client):
        file.write(
            "Fast" + proto + "Flows(RATE 0, LENGTH " + str(plength) + ", LIMIT "+ str(int(limit/client)) +", SRCETH "+ src_eth +", SRCIP " + ips[c] +
            ", DSTETH "+dst_eth+", DSTIP "+dst_ip+", FLOWS "+flows_per_client+", FLOWSIZE "+pkt_per_flow+", STOP true)"
            " -> NumberPacket(OFFSET 52) -> [" + str(c) + "]rr;\n"
        )

    file.close()
    print("trace configurations generated: " + file_location + file_name)

def generate_rules(client, rules_file):

    print("generating rules...")
    additional = 10000 - client
    for c in range(additional):
        done=False
        while not done:
            p1 = random.randrange(1, 255)
            p2 = random.randrange(1, 255)
            p3 = random.randrange(1, 255)
            p4 = random.randrange(1, 255)

            src = str(p1) +"."+ str(p2) +"."+ str(p3) +"."+ str(p4)
            if not ips.__contains__(src):
                done=True

        ips.append(src)

    rules = ""
    for ip in ips:
        rules = rules + "allow src net " + ip + "/32 \n"

    rules = rules + "1 all"
    file = open(rules_file, "w+")
    file.write(rules)
    file.close()
    print("rules generated ... :)")


if __name__ == '__main__':

    # generate firewall rules file
    gen_rules = False

    # Firewall rules file
    rules_file = "./fw-rules"

    # number of clients
    client = 2048

    # total number of packets
    limit = 320000

    # protocol
    proto = "UDP"

    # I list
    interleave = 1

    flows_per_client = 1

    pkt_per_flow = 32

    plength = 64

    file_location = ""

    trace_loc = "/mnt/traces/synthetic"

    # network params
    src_eth = "b8:ce:f6:31:3b:56"
    dst_eth = "b8:ce:f6:31:3e:42"
    # this doesn't matter
    dst_ip = "192.168.1.1"

    trace_name=None

    seq = False

    intw = False

    i=0
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "-interleave":
            interleave = int(sys.argv[i+1])
        if arg == "--print-rules":
            gen_rules=True
        if arg == "-clients":
            client = int(sys.argv[i+1])
        if arg == "-conf-loc":
            file_location = sys.argv[i+1]
        if arg == "-trace-loc":
            trace_loc = sys.argv[i+1]
        if arg == "-plength":
            plength = sys.argv[i+1]
        if arg == "-client-flows":
            flows_per_client = sys.argv[i+1]
        if arg == "-pkt-per-flow":
            pkt_per_flow = sys.argv[i+1]
        if arg == "-rules-file":
            rules_file = sys.argv[i+1]
        if arg == "-limit":
            limit = int(sys.argv[i+1])
        if arg == "-src-eth":
            src_eth = sys.argv[i+1]
        if arg == "-dst-eth":
            dst_eth = sys.argv[i+1]
        if arg == "-dst-ip":
            dst_ip = sys.argv[i+1]
        if arg == "-trace-name":
            trace_name = sys.argv[i+1]
        if arg == "-sequential":
            seq = True
        if arg == "-intertwine":
            intw = True
        i=i+1

    # calculate limit
    limit = int(pkt_per_flow) * int(flows_per_client) * client

    if int(flows_per_client) != 1:
        print("WARNING: number of flows (TCP/IP five tuple) is not the number of clients (ETH/IP four tuple)")

    # print("files location is: " + file_location)
    print("number of clients is: " + str(client))
    print("packet per flow is: " + str(pkt_per_flow))
    print("packets length is: " + str(plength))
    # print("rules file is: " + str(rules_file))

    if seq == False:
        generate_traces(client, limit, proto, plength, interleave, flows_per_client, pkt_per_flow, file_location, trace_loc, src_eth, dst_eth, dst_ip, trace_name)
    else:
        generate_traces_sequential(client, limit, proto, plength, interleave, flows_per_client, pkt_per_flow, file_location, trace_loc, src_eth, dst_eth, dst_ip, trace_name, intw)
    if gen_rules:
        generate_rules(client, rules_file)
