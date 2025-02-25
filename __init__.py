from .blender_to_unity_fbx_exporter import properties

def register():
    properties.register()

def unregister():
    properties.unregister()

if __name__ == "__main__":
    register()
