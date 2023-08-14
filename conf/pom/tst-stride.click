i1 :: InfiniteSource(\<11>, LIMIT 10)
i2 :: InfiniteSource(\<22>, LIMIT 10)
i3 :: InfiniteSource(\<33>, LIMIT 10)
i4 :: InfiniteSource(\<44>, LIMIT 10, STOP true)
ss :: StrideSched(1, 1, 2, 2)
i1 -> [0] ss; i2 -> [1]ss; i3 -> [2]ss; i4 -> [3]ss
ss -> Print -> Discard