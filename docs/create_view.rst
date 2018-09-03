The `create_view` module
========================

The `create_view` module contains a set of components that can be used to build
an interface to *create* a run. The main class is
:class:`RunCreateView<rynner.create_view.RunCreateView>`, which is instantiated
passing a list of :ref:`field objects<field_classes>` to the constructor. The
input values of each field are packaged into a dictionary which can be accessed
with the :func:`data()<rynner.create_view.RunCreateView.data>` method.


.. autoclass:: rynner.create_view.RunCreateView
   :members:


More information about the components scan be found in the :ref:`field classes
<field_classes>` section.

.. toctree::

   field_classes
