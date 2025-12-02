import bpy
import math

def create_gamer_desk_with_rgb():
    collection_name = "Escritorio_Gamer_RGB"
    # Verificar si ya existe la colección, si no crearla
    if collection_name in bpy.data.collections:
        collection = bpy.data.collections[collection_name]
    else:
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

    mat_desk_black = create_material("Desk_Black_Carbon", (0.05, 0.05, 0.05, 1), roughness=0.3)
    mat_rgb_strip = create_material("Desk_RGB_Rainbow", (1.0, 0.0, 1.0, 1), emission=True, emission_strength=5.0) # Magenta neon

    # --- HELPERS ---
    def create_obj(type, name, loc, scale, rot=(0,0,0), mat=None):
        if type == 'CUBE':
            bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
        elif type == 'CYLINDER':
            bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=1, location=loc, rotation=rot)
            
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
    desk_w = 2.0
    desk_d = 0.8
    desk_h = 0.75
    thickness = 0.05

    # --- CONSTRUCCIÓN ---
    
    # 1. Tablero Principal
    table_top = create_obj('CUBE', "Escritorio_Tablero", (0, 0, desk_h), (desk_w, desk_d, thickness), mat=mat_desk_black)
    
    # 2. Patas (Estilo Z o K gamer)
    leg_w = 0.1
    leg_d_base = 0.6
    
    # Pata Izquierda
    create_obj('CUBE', "Pata_L_Vertical", (-desk_w/2 + 0.2, 0, desk_h/2), (leg_w, 0.1, desk_h), mat=mat_desk_black)
    create_obj('CUBE', "Pata_L_Base", (-desk_w/2 + 0.2, 0, 0.05), (leg_w, leg_d_base, 0.05), mat=mat_desk_black)
    
    # Pata Derecha
    create_obj('CUBE', "Pata_R_Vertical", (desk_w/2 - 0.2, 0, desk_h/2), (leg_w, 0.1, desk_h), mat=mat_desk_black)
    create_obj('CUBE', "Pata_R_Base", (desk_w/2 - 0.2, 0, 0.05), (leg_w, leg_d_base, 0.05), mat=mat_desk_black)

    # 3. Tiras RGB (El toque gamer)
    
    # Tira Trasera (Borde posterior del tablero)
    create_obj('CUBE', "RGB_Back", (0, desk_d/2 + 0.01, desk_h), (desk_w, 0.02, 0.02), mat=mat_rgb_strip)
    
    # Tiras Laterales
    create_obj('CUBE', "RGB_Side_L", (-desk_w/2 - 0.01, 0, desk_h), (0.02, desk_d, 0.02), mat=mat_rgb_strip)
    create_obj('CUBE', "RGB_Side_R", (desk_w/2 + 0.01, 0, desk_h), (0.02, desk_d, 0.02), mat=mat_rgb_strip)

    # --- ANIMACIÓN DE COLOR (Opcional, simple cambio de color en frame 1) ---
    # Para que sea un arcoíris real se necesitarían nodos más complejos, 
    # pero aquí configuramos un color base vibrante.
    
    # --- ROOT OBJECT ---
    bpy.ops.object.empty_add(type='ARROWS', location=(0, 0, 0))
    root = bpy.context.active_object
    root.name = "Escritorio_Gamer_ROOT"
    collection.objects.link(root)
    for coll in root.users_collection:
        if coll != collection: coll.objects.unlink(root)

    # Emparentar
    for obj in collection.objects:
        if obj != root:
            obj.parent = root

    # Posicionar (En el centro, donde debería ir)
    root.location = (0, 0, 0)
    
    print("Escritorio Gamer con RGB creado.")

if __name__ == "__main__":
    create_gamer_desk_with_rgb()
