import bpy

def create_gamer_shelf():
    collection_name = "Mueble_Coleccionables"
    collection = bpy.data.collections.new(collection_name)
    bpy.context.scene.collection.children.link(collection)

    # --- MATERIALES ---
    def create_material(name, color, roughness=0.5, emission=False, emission_strength=1.0):
        mat = bpy.data.materials.get(name)
        if not mat:
            mat = bpy.data.materials.new(name=name)
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            nodes.clear()
            
            output = nodes.new('ShaderNodeOutputMaterial')
            output.location = (400, 0)
            
            if emission:
                shader = nodes.new('ShaderNodeEmission')
                shader.inputs['Color'].default_value = color
                shader.inputs['Strength'].default_value = emission_strength
            else:
                shader = nodes.new('ShaderNodeBsdfPrincipled')
                shader.inputs['Base Color'].default_value = color
                shader.inputs['Roughness'].default_value = roughness
            
            shader.location = (0, 0)
            mat.node_tree.links.new(shader.outputs[0], output.inputs['Surface'])
        return mat

    mat_wood = create_material("Shelf_BlackWood", (0.05, 0.05, 0.06, 1), roughness=0.6)
    mat_back = create_material("Shelf_BackPanel", (0.03, 0.03, 0.03, 1), roughness=0.8)
    mat_led = create_material("Shelf_LED_White", (1.0, 0.9, 0.8, 1), emission=True, emission_strength=5.0)

    # --- HELPERS ---
    def create_cube(name, loc, scale, mat=None):
        bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
        obj = bpy.context.active_object
        obj.name = name
        obj.scale = scale
        
        if mat:
            if obj.data.materials: obj.data.materials[0] = mat
            else: obj.data.materials.append(mat)
            
        for coll in obj.users_collection: coll.objects.unlink(obj)
        collection.objects.link(obj)
        return obj

    # --- DIMENSIONES ---
    width = 1.2
    height = 2.0
    depth = 0.35
    thickness = 0.02 # Grosor de la madera

    # --- CONSTRUCCIÓN ---
    
    # 1. Estructura Externa
    # Panel Izquierdo
    create_cube("Estante_Lado_L", (-width/2 + thickness/2, 0, height/2), (thickness, depth, height), mat=mat_wood)
    # Panel Derecho
    create_cube("Estante_Lado_R", (width/2 - thickness/2, 0, height/2), (thickness, depth, height), mat=mat_wood)
    # Panel Superior
    create_cube("Estante_Techo", (0, 0, height - thickness/2), (width, depth, thickness), mat=mat_wood)
    # Panel Inferior (Zócalo un poco elevado)
    create_cube("Estante_Suelo", (0, 0, 0.05), (width, depth, 0.1), mat=mat_wood)
    
    # Panel Trasero (Fondo)
    create_cube("Estante_Fondo", (0, depth/2 - thickness/2, height/2), (width - thickness*2, thickness, height - thickness*2), mat=mat_back)

    # 2. Repisas Interiores (Shelves)
    num_shelves = 4
    spacing = (height - 0.1) / (num_shelves + 1)
    
    for i in range(num_shelves):
        z_pos = 0.1 + spacing * (i + 1)
        
        # La repisa
        create_cube(f"Repisa_{i}", (0, 0, z_pos), (width - thickness*2, depth - thickness, thickness), mat=mat_wood)
        
        # Tira LED oculta debajo de cada repisa (para iluminar las figuras)
        create_cube(f"Repisa_LED_{i}", (0, -depth/2 + 0.05, z_pos - thickness), (width - thickness*4, 0.01, 0.005), mat=mat_led)

    # --- ROOT OBJECT ---
    bpy.ops.object.empty_add(type='ARROWS', location=(0, 0, 0))
    root = bpy.context.active_object
    root.name = "Mueble_Coleccionables_ROOT"
    collection.objects.link(root)
    for coll in root.users_collection:
        if coll != collection: coll.objects.unlink(root)

    # Emparentar
    for obj in collection.objects:
        if obj != root:
            obj.parent = root

    # Posicionar en la habitación (por defecto contra una pared lateral imaginaria)
    root.location = (-3.5, 2.0, 0) 
    root.rotation_euler = (0, 0, 0)

    print("Mueble para coleccionables creado.")

if __name__ == "__main__":
    create_gamer_shelf()
