import sys
import random

def generate_sf(flen, plen, fnum, srcmac, dstmac):
    ip = []
    for f in range(fnum):
        while True:
            p1 = random.randint(0, 255)
            p2 = random.randint(0, 255)
            p3 = random.randint(0, 255)
            p4 = random.randint(0, 255)
            
            sip = str(p1) +"."+ str(p2) +"."+ str(p3) +"."+ str(p4)
            if sip not in ip:
                break
        ip.append(sip)
    
    # now we have `fnum` different IPs in array
    trace_name = f"/home/pc1/yhdang/pom_trace/trace-TCP-C{fnum}-F{flen}-P{plen}"
    filename = f"./TCP-flow-{fnum}-length-{flen}"
    # SF signifies 'SYN first'
    if syn_first == True:
        trace_name += "-SF"
        filename += "-sf"
    trace_name += ".pcap"
    filename += '.click'
    file = open(filename , "w")

    file.write('td :: ToDump("' + trace_name + '");\n')
    # tricky one: use my new element RRSS
    # The key is to forge pattern according to flow size
    file.write('rrss :: RoundRobinStrideSched(')
    # first, aggregate SYN
    for i in range(fnum):
        file.write('1, ')
    # then, all remaining packets
    file.write(f'{flen - 1}')
    for i in range(fnum):
        file.write(f', {flen - 1}')
    # finally, closing
    file.write(') -> Unqueue -> td;\n')

    # Connecting wires...
    # First, aggregate SYN
    random.shuffle(ip)
    for i in range(fnum):
        file.write(
            f"f{i} :: FastTCPFlows(RATE 0, LENGTH {plen}, LIMIT {flen}, SRCETH {srcmac}, SRCIP {ip[i]}, "
            f"DSTETH {dstmac}, DSTIP 192.168.1.0, FLOWS 1, FLOWSIZE {flen})"
        )
        file.write(f" -> [{i}]rrss;\n")
    # Second, aggregate data packets
    file.write('\n')
    for i in range(fnum):
        file.write(
            f'f{i} -> [{i+fnum}]rrss;\n'
        )
    
    print(f"Config file written to {filename}")

def generate(flen, plen, fnum, srcmac, dstmac):
    ip = []
    for f in range(fnum):
        while True:
            p1 = random.randint(0, 255)
            p2 = random.randint(0, 255)
            p3 = random.randint(0, 255)
            p4 = random.randint(0, 255)
            
            sip = str(p1) +"."+ str(p2) +"."+ str(p3) +"."+ str(p4)
            if sip not in ip:
                break
        ip.append(sip)
    
    # now we have `fnum` different IPs in array
    trace_name = f"/home/pc1/yhdang/pom_trace/trace-TCP-C{fnum}-F{flen}-P{plen}"
    filename = f"./TCP-flow-{fnum}-length-{flen}"
    trace_name += ".pcap"
    filename += '.click'
    file = open(filename , "w")

    file.write('td :: ToDump("' + trace_name + '");\n')
    file.write(f'rrms :: RoundRobinMultiSched(N {flen}) -> Unqueue -> td;\n')

    random.shuffle(ip)
    for i in range(fnum):
        file.write(
            f"f{i} :: FastTCPFlows(RATE 0, LENGTH {plen}, LIMIT {flen}, SRCETH {srcmac}, SRCIP {ip[i]}, "
            f"DSTETH {dstmac}, DSTIP 192.168.1.0, FLOWS 1, FLOWSIZE {flen})"
        )
        file.write(f" -> [{i}]rrms;\n")
    print(f"Config file written to {filename}")


if __name__ == '__main__':
    
    num_flows = 1000
    
    flow_length = 3

    pkt_length = 64

    syn_first = False

    src_eth = "b8:ce:f6:31:3b:56"
    dst_eth = "b8:ce:f6:31:3e:42"

    i = 0
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == '-flen':
            flow_length = int(sys.argv[i+1])
        if arg == '-plen':
            pkt_length = int(sys.argv[i+1])
        if arg == '-nflows':
            num_flows = int(sys.argv[i+1])
        if arg == '-synfirst':
            syn_first = True
        i += 1
    
    if syn_first == True:
        generate_sf(flow_length, pkt_length, num_flows, src_eth, dst_eth)
    else:
        generate(flow_length, pkt_length, num_flows, src_eth, dst_eth)