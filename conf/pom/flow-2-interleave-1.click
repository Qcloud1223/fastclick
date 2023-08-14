td :: ToDump("/home/pc1/yhdang/pom_trace/test_script.pcap");
// burst size=0 means to drain one input and then pull from the next
rru :: RoundRobinUnqueue(BURSTSIZE 0);
rr :: RoundRobinMultiSched(N 1) -> [0]rru -> td;
FastUDPFlows(RATE 0, LENGTH 100, LIMIT 20, SRCETH b8:ce:f6:31:3b:56, SRCIP 200.82.189.71, DSTETH b8:ce:f6:31:3e:42, DSTIP 192.168.1.1, FLOWS 1, FLOWSIZE 20, STOP true) -> NumberPacket(OFFSET 52) -> [0]rr;
FastUDPFlows(RATE 0, LENGTH 100, LIMIT 20, SRCETH b8:ce:f6:31:3b:56, SRCIP 116.164.176.143, DSTETH b8:ce:f6:31:3e:42, DSTIP 192.168.1.1, FLOWS 1, FLOWSIZE 20, STOP true) -> NumberPacket(OFFSET 52) -> [1]rr;

rr2 :: RoundRobinMultiSched(N 2) -> [1]rru -> td;
FastUDPFlows(RATE 0, LENGTH 1000, LIMIT 20, SRCETH b8:ce:f6:31:3b:56, SRCIP 200.82.189.71, DSTETH b8:ce:f6:31:3e:42, DSTIP 192.168.1.1, FLOWS 1, FLOWSIZE 20, STOP true) -> NumberPacket(OFFSET 52) -> [0]rr;
FastUDPFlows(RATE 0, LENGTH 1000, LIMIT 20, SRCETH b8:ce:f6:31:3b:56, SRCIP 200.82.189.71, DSTETH b8:ce:f6:31:3e:42, DSTIP 192.168.1.1, FLOWS 1, FLOWSIZE 20, STOP true) -> NumberPacket(OFFSET 52) -> [0]rr;
