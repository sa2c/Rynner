The host module
===============
TODO  (could Connection be in a separate module?)

The Connection Class
++++++++++++++++++++

.. autoclass::  rynner.host.Connection
   :members: 

The Host Class
++++++++++++++
A fat base class to specialise.

.. autoclass:: rynner.host.Host
   :members:

The GenericClusterHost, SlurmHost and PBSHost Classes
+++++++++++++++++++++++++++++++++++++++++++++++++++++

Classes representing cluster frontends. 
The specialisations for SLURM and PBS are provided.

.. autoclass:: rynner.host.GenericClusterHost
   :members:

.. autoclass:: rynner.host.SlurmHost
   :members:

.. autoclass:: rynner.host.PBSHost
   :members:


