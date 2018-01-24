#!/usr/bin/env python

#This routine reads in an arterial tree and solves the static lung
#perfusion model as published in Burrowes et al. 2009 Ann Biomed Eng
#Vol 37, pp 2497-2509The model reads in an arterial tree only and #solves Pressure-Resistance-Flow equations within this tree for compliant vessels. Pressure is defined at terminal arteries as a function of gravitational height.
import time
from aether.diagnostics import set_diagnostics_on
from aether.indices import perfusion_indices, get_ne_radius
from aether.filenames import read_geometry_main,get_filename
from aether.geometry import append_units,define_node_geometry, define_1d_elements,define_rad_from_geom,add_matching_mesh
from aether.exports import export_1d_elem_geometry, export_node_geometry, export_1d_elem_field,export_node_field,export_terminal_perfusion
from aether.pressure_resistance_flow import evaluate_prq

from pulmonary.utils.io_files import get_default_geometry_path, get_default_output_path


def main():
    start = time.clock() 
    set_diagnostics_on(False)

    #define model geometry and indices
    perfusion_indices()
    #Read in geometry files
    define_node_geometry(get_default_geometry_path('P2BRP268-H12816_matched_arteries.ipnode'))
    define_1d_elements(get_default_geometry_path('P2BRP268-H12816_matched_arteries.ipelem'))
#    define_node_geometry(get_default_geometry_path('Small.ipnode'))
#    define_1d_elements(get_default_geometry_path('Small.ipelem'))
    #define_node_geometry('/Users/acla148/P2BRP268-H12816_Artery_Full.ipnode')
    #define_1d_elements('/Users/acla148/P2BRP268-H12816_Artery_Full.ipelem')
    #define_node_geometry('/Users/acla148/git/geometries/Smallish.ipnode')
    #define_1d_elements('/Users/acla148/git/geometries/Smallish.ipelem')
    append_units()
    
    
    add_matching_mesh()

    #define radius by Strahler order
    s_ratio=1.54
    inlet_rad=12.0
    order_system = 'strahler'
    order_options = 'all'
    name = 'inlet'
    define_rad_from_geom(order_system, s_ratio, name, inlet_rad, order_options,'')
    
    s_ratio_ven=1.55
    inlet_rad_ven=15.0
    order_system = 'strahler'
    order_options = 'list'
    name = 'inlet'
    #define_rad_from_geom(order_system, s_ratio, '6', inlet_rad, order_options,'10')
    #define_rad_from_geom(order_system, s_ratio_ven, '61358', inlet_rad_ven, order_options,'122716')#arteryfull
    define_rad_from_geom(order_system, s_ratio_ven, '61361', inlet_rad_ven, order_options,'122720')#matched arteries
    #define_rad_from_geom(order_system, s_ratio, '4', inlet_rad, order_options,'8')

    ##Call solve
    evaluate_prq()

    ##export geometry
    group_name = 'perf_model'
    export_1d_elem_geometry('../results/small.exelem', group_name)
    export_node_geometry('../results/small.exnode', group_name)

    # export element field for radius
    field_name = 'radius_perf'
    ne_radius = get_ne_radius()
    export_1d_elem_field(ne_radius, get_default_output_path('../results/radius_perf.exelem'), name, field_name)
    
    # export flow element
    filename = '../results/flow_perf.exelem'
    field_name = 'flow'
    export_1d_elem_field(7,filename, group_name, field_name)


    #export node field for pressure
    filename='../results/pressure_perf.exnode'
    field_name = 'pressure_perf'
    export_node_field(1, filename, group_name, field_name)
    
    # Export terminal solution
    export_terminal_perfusion(get_default_output_path('../results/terminal.exnode'), group_name)
    elapsed = time.clock()
    elapsed = elapsed - start
    print "Time spent solving is: ", elapsed


if __name__ == '__main__':
    main()
