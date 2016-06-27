#!/usr/bin/env python

#This routine reads in an arterial tree and solves the static lung
#perfusion model as published in Burrowes et al. 2009 Ann Biomed Eng
#Vol 37, pp 2497-2509The model reads in an arterial tree only and #solves Pressure-Resistance-Flow equations within this tree for compliant vessels. Pressure is defined at terminal arteries as a function of gravitational height.

from aether.diagnostics import set_diagnostics_on
from aether.indices import perfusion_indices, get_ne_radius
from aether.filenames import read_geometry_main,get_filename
from aether.geometry import append_units,define_node_geometry, define_1d_elements,define_rad_from_geom
from aether.exports import export_1d_elem_geometry, export_node_geometry, export_1d_elem_field
from aether.pressure_resistance_flow import evaluate_prq

from pulmonary.utils.io_files import get_default_geometry_path, get_default_output_path


def main():
    set_diagnostics_on(False)

    #define model geometry and indices
    perfusion_indices()

    #Read in geometry files
    define_node_geometry(get_default_geometry_path('Small.ipnode'))
    define_1d_elements(get_default_geometry_path('Small.ipelem'))
    append_units()

    #define radius by Strahler order
    s_ratio=1.5
    inlet_rad=12.0
    order_system = 'strahler'
    order_options = 'all'
    name = 'inlet'
    define_rad_from_geom(order_system, s_ratio, name, inlet_rad, order_options,'')

    #Call solve
    evaluate_prq()

    #export geometry
    group_name = 'perf_model'
    export_1d_elem_geometry(get_default_output_path('small.exnode'), group_name)
    export_node_geometry(get_default_output_path('small.exelem'), group_name)

    # export element field for radius
    field_name = 'radius_perf'
    ne_radius = get_ne_radius()
    export_1d_elem_field(ne_radius, get_default_output_path('radius_perf.exelem'), name, field_name)


if __name__ == '__main__':
    main()