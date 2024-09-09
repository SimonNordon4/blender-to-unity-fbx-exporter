import bpy
from bpy_extras.io_utils import ExportHelper  # type: ignore
from bpy.props import StringProperty, BoolProperty, EnumProperty # type: ignore
from bpy.types import Operator # type: ignore

from .export import export_unity_fbx

class ExportUnityFbx(Operator, ExportHelper):
	"""FBX exporter compatible with Unity's coordinate and scaling system"""
	bl_idname = "export_scene.unity_fbx"
	bl_label = "Export Unity FBX"
	bl_options = {'UNDO_GROUPED'}

	# ExportHelper mixin class uses this
	filename_ext = ".fbx"

	filter_glob: StringProperty(
		default="*.fbx",
		options={'HIDDEN'},
		maxlen=255,  # Max internal buffer length, longer would be clamped.
	) # type: ignore

	# List of operator properties, the attributes will be assigned
	# to the class instance from the operator settings before calling.

	# SELECTION
	active_collection: BoolProperty(
		name="Active Collection Only",
		description="Export objects in the active collection only (and its children). May be combined with Selected Objects Only",
		default=False,
	) # type: ignore

	selected_objects: BoolProperty(
		name="Selected Objects Only",
		description="Export selected objects only. May be combined with Active Collection Only",
		default=False,
	) # type: ignore
 
	# OBJECTS
 
	export_collections_as_empties: BoolProperty(
     name="Export Collections as Empties",
     description="Maintain the hierachy of your blender scene by replacing collections with empty objects. Useful if you use collections to organize your scene, and you want to maintain the same hierarchy in Unity",
     default=False,
    ) # type: ignore
 
	include_custom_properties: BoolProperty(
		name="Include Custom Properties",
		description="Exports custom object properties",
		default=False,
	) # type: ignore
 
 	# MESHES

	tangent_space: BoolProperty(
		name="Export tangents",
		description="Add binormal and tangent vectors, together with normal they form the tangent space (tris/quads only). Meshes with N-gons won't export tangents unless the option Triangulate Faces is enabled",
		default=False,
	) # type: ignore

	triangulate_faces: BoolProperty(
		name="Triangulate Faces",
		description="Convert all faces to triangles. This is necessary for exporting tangents in meshes with N-gons. Otherwise Unity will show a warning when importing tangents in these meshes",
		default=False,
	) # type: ignore
 
	# ARMATURES

	deform_bones: BoolProperty(
		name="Only Deform Bones",
		description="Only write deforming bones (and non-deforming ones when they have deforming children)",
		default=False,
	) # type: ignore

	leaf_bones: BoolProperty(
		name="Add Leaf Bones",
		description="Append a final bone to the end of each chain to specify last bone length (use this when you intend to edit the armature from exported data)",
		default=False,
	) # type: ignore
 
	# BONE AXES

	primary_bone_axis: EnumProperty(
		name="Primary",
		description="Axis to use as the primary axis for bones. Default 'Y'",
		items=(('X', "X Axis", ""),
				('Y', "Y Axis", ""),
				('Z', "Z Axis", ""),
				('-X', "-X Axis", ""),
				('-Y', "-Y Axis", ""),
				('-Z', "-Z Axis", ""),
		),
		default='Y',
	) # type: ignore

	secondary_bone_axis: EnumProperty(
		name="Secondary",
		description="Axis to use as the secondary axis for bones. Default 'X'",
		items=(('X', "X Axis", ""),
				('Y', "Y Axis", ""),
				('Z', "Z Axis", ""),
				('-X', "-X Axis", ""),
				('-Y', "-Y Axis", ""),
				('-Z', "-Z Axis", ""),
		),
		default='X',
	) # type: ignore



	# Custom draw method
	# https://blender.stackexchange.com/questions/55437/add-gui-elements-to-exporter-window
	# https://docs.blender.org/api/current/bpy.types.UILayout.html

	def draw(self, context):
		layout = self.layout

		# Selection Box
		box = layout.box()
		box.label(text="Selection", icon='OBJECT_DATA')
		box.prop(self, "active_collection", text="Active Collection")
		box.prop(self, "selected_objects", text="Selected Objects")

		layout.separator()

		# Objects Box
		box = layout.box()
		box.label(text="Objects", icon='OUTLINER_OB_MESH')
		box.prop(self, "export_collections_as_empties", text="Export Collections", icon='EMPTY_AXIS')
		box.prop(self, "include_custom_properties", text="Custom Properties", icon='SCRIPT')

		layout.separator()

		# Meshes Box
		box = layout.box()
		box.label(text="Meshes", icon='MESH_DATA')
		box.prop(self, "tangent_space", text="Use Tangent Space", icon='NORMALS_VERTEX')
		box.prop(self, "triangulate_faces", text="Triangulate Faces", icon='MESH_ICOSPHERE')

		layout.separator()

		# Armatures Box
		box = layout.box()
		box.label(text="Armatures", icon='ARMATURE_DATA')
		box.prop(self, "deform_bones", text="Deform Bones", icon='BONE_DATA')
		box.prop(self, "leaf_bones", text="Include Leaf Bones", icon='BONE_DATA')

		layout.separator()

		# Bone Axes Box
		box = layout.box()
		box.label(text="Bone Axes", icon='BONE_DATA')
		
		row = box.row()
		row.label(text="Primary", icon='AXIS_FRONT')
		row.prop(self, "primary_bone_axis", text="")

		row = box.row()
		row.label(text="Secondary", icon='AXIS_SIDE')
		row.prop(self, "secondary_bone_axis", text="")



	def execute(self, context):
		return export_unity_fbx(context,
                          self.filepath,
                          self.active_collection,
                          self.selected_objects,
                          self.export_collections_as_empties,
                          self.include_custom_properties,
                          self.tangent_space,
                          self.triangulate_faces,
                          self.deform_bones,
                          self.leaf_bones,
                          self.primary_bone_axis,
                          self.secondary_bone_axis
					)
  
def menu_func_export(self, context):
	self.layout.operator(ExportUnityFbx.bl_idname, text="Unity FBX (.fbx)")
  
def register():
	bpy.utils.register_class(ExportUnityFbx)
	bpy.types.TOPBAR_MT_file_export.append(menu_func_export)

def unregister():
	bpy.utils.unregister_class(ExportUnityFbx)
	bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
 
def reload():
    bpy.utils.register_class(ExportUnityFbx)
