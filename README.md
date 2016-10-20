#LISP DC migration Report Project - Niall Masterson, Cisco

This is my project to report via email the status of a DC migration using LISP IP mobility.

The LISP DC migration solution uses the Cisco CSR1000v router in both the legacy and new datacenters. Workloads can be migrated between the DCs without changing IP addressing. The purpose of this script is to provide a report on the number of workloads that are still in the legacy DC and the number of workloads that have been migrated to the new DC.

The script uses the REST-API on the CSR1000v to gather the LISP routes in the routing table on the CSR1000v routers in each site. It then does a count on the number of workloads on each DC and does a reverse DNS lookup to identify the hostnames of the servers in each DC. An email is then sent out with the details collected.

Note this script was tested on the CSR1000v before support for LISP was added to the REST-API. Support for querying the LISP databse via the REST-API was added in version 3.13. So I used the routing table to match LISP routes rather than the LISP database itself.

