import bpy
import math

def create_gamer_bed():
    collection_name = "Cama_Gamer"
    collection = bpy.data.collections.new(collection_name)
    bpy.context.scene.collection.children.link(collection)

    # --- MATERIALES ---
    def create_material(name, color, roughness=0.8):
        mat = bpy.data.materials.get(name)
        if not mat:
            mat = bpy.data.materials.new(name=name)
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            nodes.clear()
            output = nodes.new('ShaderNodeOutputMaterial')
            output.location = (400, 0)
            shader = nodes.new('ShaderNodeBsdfPrincipled')
            shader.inputs['Base Color'].default_value = color
            shader.inputs['Roughness'].default_value = roughness
            shader.location = (0, 0)
            mat.node_tree.links.new(shader.outputs[0], output.inputs['Surface'])
        return mat

    mat_frame = create_material("Bed_Frame_Black", (0.05, 0.05, 0.05, 1), roughness=0.4)
    mat_mattress = create_material("Bed_Mattress_White", (0.9, 0.9, 0.95, 1), roughness=0.9)
    mat_blanket = create_material("Bed_Blanket_Navy", (0.05, 0.1, 0.3, 1), roughness=1.0)
    mat_pillow = create_material("Bed_Pillow_Grey", (0.7, 0.7, 0.75, 1), roughness=1.0)

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

    def add_softness(obj, bevel_width=0.05):
        bpy.context.view_layer.objects.active = obj
        mod = obj.modifiers.new(name="Bevel", type='BEVEL')
        mod.width = bevel_width
        mod.segments = 5
        bpy.ops.object.shade_smooth()

    # --- DIMENSIONES ---
    bed_w = 1.6  # Cama Queen/Matrimonial
    bed_l = 2.1
    bed_h = 0.5  # Altura colchón

    # --- CONSTRUCCIÓN ---

    # 1. Estructura (Base)
    # Patas
    leg_h = 0.2
    for x in [-1, 1]:
        for y in [-1, 1]:
            create_cube("Pata_Cama", (x*(bed_w/2 - 0.05), y*(bed_l/2 - 0.05), leg_h/2), (0.08, 0.08, leg_h), mat=mat_frame)
    
    # Marco
    create_cube("Marco_Cama", (0, 0, leg_h + 0.05), (bed_w, bed_l, 0.1), mat=mat_frame)

    # Cabecera (Headboard)
    head_h = 1.2
    create_cube("Cabecera", (0, bed_l/2, head_h/2), (bed_w, 0.1, head_h), mat=mat_frame)

    # 2. Colchón
    mattress_thick = 0.25
    mattress = create_cube("Colchon", (0, 0, leg_h + 0.1 + mattress_thick/2), (bed_w - 0.05, bed_l - 0.1, mattress_thick), mat=mat_mattress)
    add_softness(mattress, 0.05)

    # 3. Cobija / Edredón (Cubriendo la mitad inferior)
    blanket_l = bed_l * 0.6
    blanket_z = leg_h + 0.1 + mattress_thick + 0.02
    blanket = create_cube("Edredon", (0, -bed_l/2 + blanket_l/2, blanket_z), (bed_w + 0.1, blanket_l, 0.05), mat=mat_blanket)
    add_softness(blanket, 0.08)

    # 4. Almohadas
    pillow_w = 0.6
    pillow_l = 0.4
    pillow_h = 0.15
    
    # Almohada Izquierda
    p1 = create_cube("Almohada_L", (-bed_w/4, bed_l/2 - 0.4, blanket_z), (pillow_w, pillow_l, pillow_h), mat=mat_pillow)
    p1.rotation_euler = (math.radians(10), 0, math.radians(5)) # Un poco inclinada y rotada
    add_softness(p1, 0.08)

    # Almohada Derecha
    p2 = create_cube("Almohada_R", (bed_w/4, bed_l/2 - 0.4, blanket_z), (pillow_w, pillow_l, pillow_h), mat=mat_pillow)
    p2.rotation_euler = (math.radians(10), 0, math.radians(-5))
    add_softness(p2, 0.08)

    # --- ROOT OBJECT ---
    bpy.ops.object.empty_add(type='ARROWS', location=(0, 0, 0))
    root = bpy.context.active_object
    root.name = "Cama_Gamer_ROOT"
    collection.objects.link(root)
    for coll in root.users_collection:
        if coll != collection: coll.objects.unlink(root)

    # Emparentar
    for obj in collection.objects:
        if obj != root:
            obj.parent = root

    # Posicionar en la habitación (esquina opuesta al escritorio)
    root.location = (2.5, 2.5, 0)
    root.rotation_euler = (0, 0, math.radians(90))

    print("Cama Gamer creada.")

if __name__ == "__main__":
    create_gamer_bed()
