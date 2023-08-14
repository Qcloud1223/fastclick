#ifndef CLICK_RRSTRIDESCHED_H
#define CLICK_RRSTRIDESCHED_H
#include <click/notifier.hh>
#include "rrsched.hh"

CLICK_DECLS

class RRStrideSched : public RRSched {
    public:
        RRStrideSched() CLICK_COLD;
        const char *class_name() const override { return "RoundRobinStrideSched"; }
        int configure(Vector<String> &conf, ErrorHandler *) CLICK_COLD;
        Packet *pull(int port);
    #if HAVE_BATCH
        PacketBatch *pull_batch(int port, unsigned max) override;
    #endif

    private:
        int _n;
        int _n_cur;
        int *_all;
};

CLICK_ENDDECLS
#endif