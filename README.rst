

=================
Lung Applications
=================

A collection of Python Scripts for running pulmonary simulations using the `Aether <https://github.com/LungNoodle/lungsim>`_ library.  To run these scripts without modifying them you will need the following:

  * The Aether library built with the Python bindings
  * The Aether library bindings made available to the Python environment in which the script is going to be run.
  * The geometry files placed in a sibling directory of the application scripts and their packages.

See the Aether library for instructions on the ways you can make the Aether library available from a Python environment.

Pulmonary Python Library
========================

The pulmonary python package contains scripts and helper functions for running the main scripts that are common to at least two scripts.

Ventilation Model
=================

Simulates ventilation of the lung.

Perfusion Burrowes 2009
=======================

Simulates perfusion of the lung according to Burrowes 2009.