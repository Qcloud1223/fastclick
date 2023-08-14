i1 :: InfiniteSource(\<11>, LIMIT 10)
i2 :: InfiniteSource(\<22>, LIMIT 10, STOP true)

i1 -> ss1 :: StrideSwitch(1, 1, 1, 1);
i2 -> ss2 :: StrideSwitch(1, 1);


// ss1[0] -> Script(print "ss1 output 0", write ss1.tickets1 4) -> Discard;
ss1[0] -> Script(print "ss1 output 0") -> Discard;

// ss1[1] -> Script(print "ss1 output 1", write ss1.tickets0 4) -> Discard;
ss1[1] -> Script(print "ss1 output 1") -> Discard;

ss1[2] -> Script(print "ss1 output 2") -> Discard;
ss1[3] -> Script(print "ss1 output 3") -> Discard;


// ss2[0] -> Script(print "ss2 output 0", write ss2.tickets1 4) -> Discard;
ss2[0] -> Script(print "ss2 output 0") -> Discard;

// ss2[1] -> Script(print "ss2 output 1", write ss2.tickets0 4) -> Discard;
ss2[1] -> Script(print "ss2 output 1") -> Discard;

