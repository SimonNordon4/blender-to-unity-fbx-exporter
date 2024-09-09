import bpy

import bpy

def create_empties_as_collection_proxy(use_selection=False):
    def create_empty_for_collection(collection):
        # Create an empty object for the collection
        empty = bpy.data.objects.new(f"Collection: {collection.name}", None)
        bpy.context.scene.collection.objects.link(empty)
        return empty

    def parent_collection_objects_to_empty(collection, empty):
        # Parent all objects in the collection to the empty
        for obj in collection.objects:
            obj.parent = empty

    def recursive_create_empties(collection, parent_empty=None):
        # Create an empty for the current collection
        empty = create_empty_for_collection(collection)
        
        if parent_empty:
            empty.parent = parent_empty
        
        # Parent objects in the current collection to the empty
        parent_collection_objects_to_empty(collection, empty)
        
        # Recursively create empties for child collections
        for child in collection.children:
            recursive_create_empties(child, empty)
        
        return empty

    def get_collections_with_selected_objects():
        # Collect the collections that contain at least one selected object
        selected_collections = set()
        for obj in bpy.context.selected_objects:
            for col in obj.users_collection:
                selected_collections.add(col)
        return selected_collections

    empties_list = []
    
    if use_selection:
        # If using selection, filter the collections containing selected objects
        collections_to_process = get_collections_with_selected_objects()
    else:
        # Process all root collections if not using selection
        collections_to_process = bpy.context.scene.collection.children
    
    for collection in collections_to_process:
        empty = recursive_create_empties(collection)
        empties_list.append(empty)
        
        # Add the created empty to selected objects
        if use_selection:
            for obj in bpy.context.selected_objects:
                obj.parent = empty

    return empties_list

# Call the function
empties = create_empties_as_collection_proxy(use_selection=True)
print("Created empties:", empties)


def remove_empties(empties):
    """
    Removes the specified empty objects from the scene and unparents any objects that were parented to them.
    
    Args:
        empties (list): A list of empty objects to remove.
    """
    for empty in empties:
        if empty.type == 'EMPTY':
            # Unparent all objects that are parented to this empty
            for obj in empty.children:
                obj.parent = None

            # Unlink the empty from the scene
            bpy.context.scene.collection.objects.unlink(empty)

            # Delete the empty
            bpy.data.objects.remove(empty, do_unlink=True)


