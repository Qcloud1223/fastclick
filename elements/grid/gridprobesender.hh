#ifndef GRIDPROBESENDER_HH
#define GRIDPROBESENDER_HH
#include <click/element.hh>
#include <click/etheraddress.hh>
#include <click/ipaddress.hh>
#include <click/vector.hh>
#include <click/bighashmap.hh>
#include <click/timer.hh>
CLICK_DECLS

/*
 * =c
 * GridProbeSender(E, I)
 * =s Grid
 * Produces a Grid route probe packet.
 * =d
 * 
 * E and I are this node's ethernet and IP addresses, respectively.
 * When the element's send_probe handler is called, pushes a
 * GRID_ROUTE_PROBE packet for the specified destination, with the
 * specified nonce.  This packet should probably be sent back through
 * the Grid input packet rocessing.
 *
 * =h send_probe write-only
 * arguments are the destination IP followed by a nonce, e.g: ``18.26.7.111 3242435''
 * 
 *
 * =a GridProbeReplyReceiver, GridProbeHandler, LookupLocalGridRoute */

class GridProbeSender : public Element {

 public:
  GridProbeSender();
  ~GridProbeSender();
  
  const char *class_name() const		{ return "GridProbeSender"; }
  const char *processing() const		{ return PUSH; }
  GridProbeSender *clone() const;
  int configure(Vector<String> &, ErrorHandler *);
  int initialize(ErrorHandler *);
  
  void send_probe(IPAddress &, unsigned int);

  void add_handlers();

private:
  IPAddress _ip;
  EtherAddress _eth;
};

CLICK_ENDDECLS
#endif
