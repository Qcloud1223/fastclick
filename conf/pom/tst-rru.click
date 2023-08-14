// rru :: RoundRobinUnqueue(BURSTSIZE 1)
// rru2 :: RoundRobinUnqueue(BURSTSIZE 1)
// rru_both :: RoundRobinUnqueue(BURSTSIZE 0)

rrs :: RoundRobinMultiSched(N 1)
rrs2 :: RoundRobinMultiSched(N 5)
rrs_both :: RoundRobinMultiSched(N 1)


i1 :: InfiniteSource(\<11>, LIMIT 10)
i2 :: InfiniteSource(\<22>, LIMIT 10)
// i3 :: InfiniteSource(\<33>, LIMIT 10)
// i4 :: InfiniteSource(\<44>, LIMIT 10)
// ps :: PrioSched()

/* connect source to queue, so that multiple downstream elements can pull from the same source */
// q1 :: Queue
// q2 :: Queue
// q3 :: Queue
// q4 :: Queue

// i1 -> q1;
// i2 -> q2;
// i3 -> q3;
// i4 -> q4;

i1 -> Script(print "I1 is invoked") -> [0]rrs;
i1 -> Script(print "I2 is invoked") -> [0]rrs2;
i2 -> Script(print "I3 is invoked") -> [1]rrs;
i2 -> Script(print "I4 is invoked") -> [1]rrs2;

// i1 -> [0]rrs;
// i2 -> [1]rrs;
// i3 -> [0]rrs2;
// i4 -> [1]rrs2;

rrs -> [0]rrs_both;
rrs2 -> [1]rrs_both;

rrs_both -> Unqueue -> Discard;