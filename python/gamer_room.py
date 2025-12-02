import bpy

def create_gamer_room():
    collection_name = "Gamer_Room"
    collection = bpy.data.collections.new(collection_name)
    bpy.context.scene.collection.children.link(collection)

    # --- MATERIALES ---
    def create_material(name, color, roughness=0.5, texture_type=None):
        mat = bpy.data.materials.get(name)
        if not mat:
            mat = bpy.data.materials.new(name=name)
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            nodes.clear()
            
            output = nodes.new('ShaderNodeOutputMaterial')
            output.location = (400, 0)
            
            shader = nodes.new('ShaderNodeBsdfPrincipled')
            shader.location = (0, 0)
            shader.inputs['Base Color'].default_value = color
            shader.inputs['Roughness'].default_value = roughness
            
            mat.node_tree.links.new(shader.outputs['BSDF'], output.inputs['Surface'])
        return mat

    # Colores oscuros para ambiente gamer
    mat_floor = create_material("Room_Floor_DarkWood", (0.05, 0.03, 0.01, 1), roughness=0.3)
    mat_wall = create_material("Room_Wall_DarkGrey", (0.1, 0.1, 0.12, 1), roughness=0.9)
    mat_baseboard = create_material("Room_Baseboard_Black", (0.02, 0.02, 0.02, 1), roughness=0.5)

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
    # Hacemos la habitación grande para que quepa todo
    room_size = 8.0 # 8x8 metros
    wall_height = 4.0
    wall_thick = 0.2
    
    # Offset para que el origen (0,0) quede cerca de la esquina, ideal para poner el escritorio
    # Paredes en +Y (Fondo) y -X (Izquierda)
    
    # 1. SUELO
    create_cube("Suelo", (0, 0, -0.1), (room_size, room_size, 0.2), mat=mat_floor)

    # 2. PAREDES (Forma de L)
    
    # Pared Trasera (Detrás del escritorio, en +Y)
    # La situamos en el borde del suelo
    wall_back_y = (room_size / 2)
    create_cube("Pared_Fondo", (0, wall_back_y, wall_height/2), (room_size + wall_thick, wall_thick, wall_height), mat=mat_wall)

    # Pared Lateral (Izquierda, en -X)
    wall_side_x = -(room_size / 2)
    create_cube("Pared_Lateral", (wall_side_x, 0, wall_height/2), (wall_thick, room_size, wall_height), mat=mat_wall)

    # 3. RODAPIÉS (Zócalos) - Para darle realismo
    # Fondo
    create_cube("Zocalo_Fondo", (0, wall_back_y - wall_thick/2 - 0.01, 0.075), (room_size, 0.02, 0.15), mat=mat_baseboard)
    # Lateral
    create_cube("Zocalo_Lateral", (wall_side_x + wall_thick/2 + 0.01, 0, 0.075), (0.02, room_size, 0.15), mat=mat_baseboard)

    print("Habitación Gamer (L-Shape) creada.")

if __name__ == "__main__":
    create_gamer_room()
