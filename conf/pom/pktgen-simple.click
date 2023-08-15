/* simple pktgen that replays */
define(
    $iface 0,
    $frommac b8:ce:f6:31:3b:56,
    $tomac   b8:ce:f6:31:3e:42,
    $burst   32
)

define($trace /home/pc1/yhdang/pom_trace/trace-UDP-C2-I1-F1.pcap)
define($limit 500000) //Number of packets to preload
define($replay_count 10000000) //Number of time we'll replay those packets
define($quick true)
define($ignore 0)

// ensure DPDK buffer
// (1 << 19) - 1
DPDKInfo(524287)

fd :: FromDump($trace, STOP false, TIMING false);
td :: ToDPDKDevice($iface, BURST $burst, IQUEUE $burst, BLOCKING true, NDESC 0, TCO 1);

elementclass NoNumberise { $magic |
    input
    -> Strip(14) 
    -> check :: CheckIPHeader(CHECKSUM false) 
    -> Unstrip(14) 
    -> output
}

elementclass Generator { $magic |
    input
      -> EnsureDPDKBuffer
      -> rwIN :: EtherRewrite($frommac,$tomac)
      -> Pad()
      -> NoNumberise($magic)
    // `limit`: limit to preloaded packets
    // `timing`: the percentage to respect the original capture timestamp
    // upd: TIMING=10 will run 10% the speed of TIMING=100
    // TODO: find out the reason
      -> replay :: ReplayUnqueue(STOP 0, STOP_TIME 0, QUICK_CLONE $quick, VERBOSE false, ACTIVE true, LIMIT 500000, TIMING 100)

      -> avgSIN :: AverageCounter(IGNORE $ignore)
      -> { input[0] -> MarkIPHeader(OFFSET 14) -> ipc :: IPClassifier(tcp or udp, -) ->  ResetIPChecksum(L4 true) -> [0]output; ipc[1] -> [0]output; }
      -> output;
}

// since there is only one thread, there is no point in spinlock
fd -> gen0 :: Generator(\<5601>) -> td;StaticThreadSched(gen0/replay 0);

avgSIN :: HandlerAggregate( ELEMENT gen0/avgSIN);

link_initialized :: Script(TYPE PASSIVE,
    print "Link initialized !",
    wait 1s,
    print "Starting replay...",
    write gen0/avgSIN.reset,
    write gen0/replay.stop $replay_count, write gen0/replay.active true,
    print "Time is $(now)",
);

display_th :: Script(TYPE PASSIVE,
    print "Starting iterative...",

    set stime $(now),
    label g,
    write gen0/avgSIN.reset,
    wait 1,
    set diff $(sub $(now) $time),
    print "Diff $diff",
    set time $(sub $(now) $stime),
    set sent $(avgSIN.add count),
    print "IGEN-$time-RESULT-ICOUNT $received",
    print "IGEN-$time-RESULT-IDROPPED $(sub $sent $received)",
    print "IGEN-$time-RESULT-IDROPPEDPS $(div $(sub $sent $received) $diff)",
    print "IGEN-$time-RESULT-ITHROUGHPUT $rx",

    print "IGEN-$time-RESULT-ITX $tx",
    print "IGEN-$time-RESULT-ILOSS $(sub $rx $tx)",
    goto g
);

DriverManager(
    print "waiting for preload...",
    pause,
    wait 1,
    write link_initialized.run,
    set starttime $(now),
    pause,
    set stoptime $(now),
    set sent $(avgSIN.add count),
    print "RESULT-TESTTIME $(sub $stoptime $starttime)",
    print "RESULT-SENT $sent",
    print "RESULT-TXBPS" $(div $(avgSIN.add link_rate) 1000000000)"G",
    print "RESULT-TXPPS" $(div $(avgSIN.add rate) 1000000)"M",
    stop
);
