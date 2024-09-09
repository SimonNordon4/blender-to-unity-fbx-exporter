import bpy

def create_empties_as_collection_proxy(use_selection=False):
    def create_empty_for_collection(collection):
        print(f"Creating empty for collection: {collection.name}")
        # Create an empty object for the collection
        empty = bpy.data.objects.new(f"Collection: {collection.name}", None)
        bpy.context.scene.collection.objects.link(empty)
        return empty

    def parent_selected_objects_to_empty(collection, empty):
        # Parent only selected objects in the collection to the empty
        print(f"Parenting selected object to {collection.name}")
        for obj in collection.objects:
            if obj.select_get():
                obj.parent = empty

    def parent_collection_objects_to_empty(collection, empty):
        # Parent all objects in the collection to the empty (used when not using selection)
        print(f"Parenting all objects to {collection.name}")
        for obj in collection.objects:
            obj.parent = empty

    def get_collections_with_selected_objects():
        # Collect the collections that contain at least one selected object
        selected_collections = set()
        for obj in bpy.context.selected_objects:
            for col in obj.users_collection:
                selected_collections.add(col)
        return selected_collections


    # Get a list of our collections to process.
    if use_selection:
        collections_to_process = get_collections_with_selected_objects()
    else:
        collections_to_process = bpy.context.scene.collection.children_recursive
    
    collection_proxy_dict = {}
    empties = []
    
    for collection in collections_to_process:
        # Create an empty for the collection
        empty = create_empty_for_collection(collection)
        empties.append(empty)
        collection_proxy_dict[collection] = empty
        
        if use_selection:
            # Parent only selected objects in the collection to the empty
            parent_selected_objects_to_empty(collection, empty)
        else:
            # Parent all objects in the collection to the empty (used when not using selection)
            parent_collection_objects_to_empty(collection, empty)
        
    # iterate the dictionary to parent the empties to the collection
    for collection, empty in collection_proxy_dict.items():
        collection_children = collection.children
        
        for child in collection_children:
            # check if it exists in teh dict
            if child in collection_proxy_dict:
                # parent the empty to the collection
                child_empty = collection_proxy_dict[child]
                print(f"Found {child_empty.name} is a child of {empty.name}")
                child_empty.parent = empty
                
    if use_selection:
         # Select the empties
            for empty in collection_proxy_dict.values():
                empty.select_set(True)
        

    # Return the created empties for reference
    return empties

def remove_empties(empties):
    print("Removing empties")
    for empty in list(empties):  # Create a copy of the list to iterate over
        if empty.name in bpy.data.objects:  # Check by object name
            bpy.data.objects.remove(empty, do_unlink=True)
            
    



