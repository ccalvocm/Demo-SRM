#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 18:41:23 2021

@author: faarrosp
"""

from functools import singledispatch
from itertools import chain
from typing import (List, 
                    Tuple,
                    TypeVar)

from shapely.geometry import (GeometryCollection,
                              LinearRing,
                              LineString,
                              Point,
                              Polygon)
from shapely.geometry.base import (BaseGeometry,
                                   BaseMultipartGeometry)


import numpy as np
import shapely as sh

def getPolyCoords(geom, coord_type):
    """Returns the coordinates ('x|y') of edges/vertices of a Polygon/others"""

    # Parse the geometries and grab the coordinate
    geometry = geom
    #print(geometry.type)

    if geometry.type=='Polygon':
        if coord_type == 'x':
            # Get the x coordinates of the exterior
            # Interior is more complex: xxx.interiors[0].coords.xy[0]
            return list( geometry.exterior.coords.xy[0] )
        elif coord_type == 'y':
            # Get the y coordinates of the exterior
            return list( geometry.exterior.coords.xy[1] )

    if geometry.type in ['Point', 'LineString']:
        if coord_type == 'x':
            return list( geometry.xy[0] )
        elif coord_type == 'y':
            return list( geometry.xy[1] )

    if geometry.type=='MultiLineString':
        all_xy = []
        for ea in geometry:
            if coord_type == 'x':
                all_xy.append(list( ea.xy[0] ))
            elif coord_type == 'y':
                all_xy.append(list( ea.xy[1] ))
        return all_xy

    if geometry.type=='MultiPolygon':
        all_xy = []
        for ea in geometry:
            if coord_type == 'x':
                all_xy.append(list( ea.exterior.coords.xy[0] ))
            elif coord_type == 'y':
                all_xy.append(list( ea.exterior.coords.xy[1] ))
        return all_xy

    else:
        # Finally, return empty list for unknown geometries
        return []

Geometry = TypeVar('Geometry', bound=BaseGeometry)


@singledispatch
def to_coords(geometry: Geometry) -> List[Tuple[float, float]]:
    """Returns a list of unique vertices of a given geometry object."""
    raise NotImplementedError(f"Unsupported Geometry {type(geometry)}")


@to_coords.register
def _(geometry: Point):
    return [(geometry.x, geometry.y)]


@to_coords.register
def _(geometry: LineString):
    return list(geometry.coords)


@to_coords.register
def _(geometry: LinearRing):
    return list(geometry.coords[:-1])


@to_coords.register
def _(geometry: BaseMultipartGeometry):
    return list(set(chain.from_iterable(map(to_coords, geometry))))


@to_coords.register
def _(geometry: Polygon):
    return to_coords(GeometryCollection([geometry.exterior, *geometry.interiors]))

if __name__=='__main__':
    print('hola')
else:
    pass