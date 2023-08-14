i1 :: InfiniteSource(\<11>, LIMIT 10)
i2 :: InfiniteSource(\<22>, LIMIT 10, STOP true)
// i3 :: InfiniteSource(\<33>, LIMIT 10)
// i4 :: InfiniteSource(\<44>, LIMIT 10)
rrss :: RoundRobinStrideSched(1, 1, 4, 4)


i1 -> [0] rrss; i2 -> [1]rrss; i1 -> [2]rrss; i2 -> [3]rrss;
rrss -> Print -> Discard;