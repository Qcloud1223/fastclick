td :: ToDump("/home/pc1/yhdang/pom_trace/trace-UDP-C2-I32-F1.pcap");
rr :: RoundRobinMultiSched(N 32) -> Unqueue -> td;
FastUDPFlows(RATE 0, LENGTH 1000, LIMIT 400, SRCETH b8:ce:f6:31:3b:56, SRCIP 13.152.249.159, DSTETH b8:ce:f6:31:3e:42, DSTIP 192.168.1.1, FLOWS 1, FLOWSIZE 400, STOP true) -> NumberPacket(OFFSET 52) -> [0]rr;
FastUDPFlows(RATE 0, LENGTH 1000, LIMIT 400, SRCETH b8:ce:f6:31:3b:56, SRCIP 55.159.78.128, DSTETH b8:ce:f6:31:3e:42, DSTIP 192.168.1.1, FLOWS 1, FLOWSIZE 400, STOP true) -> NumberPacket(OFFSET 52) -> [1]rr;
