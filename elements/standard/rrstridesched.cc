#include <click/config.h>
#include <click/error.hh>
#include <click/args.hh>
#include "rrstridesched.hh"
CLICK_DECLS

RRStrideSched::RRStrideSched()
    : _n(1), _n_cur(0), _all(0)
{

}

int RRStrideSched::configure(Vector<String> &conf, ErrorHandler *errh)
{
    _max = ninputs();
    /* Temporarily remove support for N and MAX */
    // if (Args(conf, this, errh)
    //     .read_or_set_p("N", _n, 1)
    //     .read_or_set_p("MAX", _max, ninputs())
    //     .complete() < 0)
    //     return -1;

    bool first = !_all;
    if (first && !(_all = new int[ninputs()]))
        return errh->error("OOM");
    for (int i = 0; i < conf.size(); i++) {
        int v;
        if (!IntArg().parse(conf[i], v))
            errh->error("argument %d should be number of schedule times (int)", i);
        else if (v < 0)
            errh->error("argument %d must be >= 0", i);
        else {
            _all[i] = v;
        }
    }
    return errh->nerrors() ? -1 : 0;
}

Packet *
RRStrideSched::pull(int)
{
    int i = _next;
    for (int j = 0; j < _max; j++) {
        Packet *p = (_signals[i] ? input(i).pull() : 0);
        if (p) {
            _n_cur++;
            /* if balance for this port is exhausted */
            if (_n_cur == _all[i]) {
                i++;
                /* rewind location */
                if (i >= _max) {
                    i = 0;
                }
                /* refill balance */
                _n_cur = 0;
            }
            /* remember the location of last pull */
            _next = i;
            return p;
        } else {
            i++;
            if (i >= _max) {
                i = 0;
            }
            _n_cur = 0;
        }
    }
    return 0;
}

#if HAVE_BATCH
PacketBatch *
RRStrideSched::pull_batch(int port, unsigned max) {
    PacketBatch *batch;
    MAKE_BATCH(RRStrideSched::pull(port), batch, max);
    return batch;
}
#endif

CLICK_ENDDECLS
EXPORT_ELEMENT(RRStrideSched)