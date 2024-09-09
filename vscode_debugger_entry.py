import bpy
import sys
import os
import importlib


sys.path.append(os.path.dirname(os.path.realpath(__file__)))
    

import blender_to_unity_fbx_exporter.properties as properties
import blender_to_unity_fbx_exporter.export as export
import blender_to_unity_fbx_exporter.collections_as_empties as collections_as_empties

# Reload the modules (useful for debugging)

importlib.reload(collections_as_empties)
importlib.reload(properties)
importlib.reload(export)

# Register the add-on

properties.reload()
