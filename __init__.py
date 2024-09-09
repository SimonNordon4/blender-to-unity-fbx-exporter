bl_info = {
	"name": "Unity FBX format",
	"author": "Angel 'Edy' Garcia (@VehiclePhysics)",
	"version": (1, 4, 1),
	"blender": (4, 00, 0),
	"location": "File > Export > Unity FBX",
	"description": "FBX exporter compatible with Unity's coordinate and scaling system.",
	"warning": "",
	"wiki_url": "",
	"category": "Import-Export",
}

from .blender_to_unity_fbx_exporter import properties

def register():
    properties.register()

def unregister():
    properties.unregister()

if __name__ == "__main__":
    register()
