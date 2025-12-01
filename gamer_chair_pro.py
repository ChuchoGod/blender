import bpy
import math

def create_gamer_chair():
    # NOTA: Ya no borramos los objetos existentes para respetar tu escena.
    
    # Crear una colección nueva para mantener todo organizado
    collection_name = "SillaGamer_Pro"
    collection = bpy.data.collections.new(collection_name)
    bpy.context.scene.collection.children.link(collection)
    
    # --- MATERIALES ---
    def create_material(name, color, roughness=0.5, metallic=0.0):
        mat = bpy.data.materials.get(name)
        if not mat:
            mat = bpy.data.materials.new(name=name)
            mat.use_nodes = True
            
            # Buscar el nodo por tipo para evitar errores de idioma o versión
            bsdf = next((n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
            
            if not bsdf:
                bsdf = mat.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
                
            bsdf.inputs['Base Color'].default_value = color
            bsdf.inputs['Roughness'].default_value = roughness
            bsdf.inputs['Metallic'].default_value = metallic
        return mat

    mat_black = create_material("Gamer_Black_Leather", (0.05, 0.05, 0.05, 1), 0.4)
    mat_red = create_material("Gamer_Red_Accent", (0.8, 0.05, 0.05, 1), 0.4)
    mat_metal = create_material("Gamer_Metal", (0.2, 0.2, 0.2, 1), 0.2, 1.0)
    mat_plastic = create_material("Gamer_Plastic", (0.1, 0.1, 0.1, 1), 0.6)

    # --- HELPERS ---
    def add_bevel(obj, width=0.015, segments=3):
        """Añade un modificador de biselado para que no se vea tan 'low poly'"""
        bpy.context.view_layer.objects.active = obj
        mod = obj.modifiers.new(name="Bevel", type='BEVEL')
        mod.width = width
        mod.segments = segments
        bpy.ops.object.shade_smooth() # Suavizar sombreado

    def create_primitive(type, name, location, scale, rotation=(0,0,0), material=None):
        if type == 'CUBE':
            bpy.ops.mesh.primitive_cube_add(size=1, location=location, rotation=rotation)
        elif type == 'CYLINDER':
            bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=1, location=location, rotation=rotation)
        
        obj = bpy.context.active_object
        obj.name = name
        obj.scale = scale
        
        # Asignar material
        if material:
            if obj.data.materials:
                obj.data.materials[0] = material
            else:
                obj.data.materials.append(material)
        
        # Mover a la colección
        for coll in obj.users_collection:
            coll.objects.unlink(obj)
        collection.objects.link(obj)
        
        return obj

    # --- CONSTRUCCIÓN ---

    # 1. Asiento (Estilo Cubo - Bucket Seat)
    # Base central del asiento
    seat_base = create_primitive('CUBE', "Asiento_Base", (0, 0, 0.5), (0.5, 0.55, 0.1), material=mat_black)
    add_bevel(seat_base, 0.02)

    # Alas laterales del asiento (Bolsters)
    seat_wing_l = create_primitive('CUBE', "Asiento_Ala_L", (-0.28, 0, 0.55), (0.12, 0.55, 0.15), (0, math.radians(15), 0), mat_red)
    add_bevel(seat_wing_l)
    
    seat_wing_r = create_primitive('CUBE', "Asiento_Ala_R", (0.28, 0, 0.55), (0.12, 0.55, 0.15), (0, math.radians(-15), 0), mat_red)
    add_bevel(seat_wing_r)

    # 2. Respaldo (Backrest)
    # Parte central
    back_center = create_primitive('CUBE', "Respaldo_Centro", (0, 0.2, 1.1), (0.4, 0.1, 1.1), (math.radians(-10), 0, 0), mat_black)
    add_bevel(back_center, 0.03)

    # Alas laterales del respaldo (Hombros)
    back_wing_l = create_primitive('CUBE', "Respaldo_Ala_L", (-0.25, 0.22, 1.0), (0.15, 0.1, 0.8), (math.radians(-10), math.radians(15), 0), mat_red)
    add_bevel(back_wing_l)

    back_wing_r = create_primitive('CUBE', "Respaldo_Ala_R", (0.25, 0.22, 1.0), (0.15, 0.1, 0.8), (math.radians(-10), math.radians(-15), 0), mat_red)
    add_bevel(back_wing_r)

    # Parte superior (Cabecera integrada)
    head_area = create_primitive('CUBE', "Respaldo_Cabeza", (0, 0.3, 1.55), (0.5, 0.1, 0.3), (math.radians(-10), 0, 0), mat_black)
    add_bevel(head_area)

    # 3. Cojines (Lumbar y Cabeza)
    lumbar = create_primitive('CUBE', "Cojin_Lumbar", (0, 0.15, 0.75), (0.35, 0.08, 0.2), (math.radians(-10), 0, 0), mat_red)
    add_bevel(lumbar, 0.04, 5) # Más suave

    head_pillow = create_primitive('CUBE', "Cojin_Cabeza", (0, 0.26, 1.55), (0.3, 0.08, 0.18), (math.radians(-10), 0, 0), mat_red)
    add_bevel(head_pillow, 0.04, 5)

    # 4. Reposabrazos (Ajustables)
    arm_height = 0.75
    arm_x = 0.38
    
    for side, x_pos in [("L", -arm_x), ("R", arm_x)]:
        # Poste vertical
        create_primitive('CYLINDER', f"Brazo_Poste_{side}", (x_pos, 0, 0.6), (0.08, 0.08, 0.3), material=mat_plastic)
        # Superficie de apoyo
        arm_rest = create_primitive('CUBE', f"Brazo_Apoyo_{side}", (x_pos, 0, arm_height), (0.1, 0.35, 0.04), material=mat_black)
        add_bevel(arm_rest, 0.01)

    # 5. Base Mecánica
    # Mecanismo debajo del asiento
    create_primitive('CUBE', "Mecanismo_Base", (0, 0, 0.42), (0.3, 0.3, 0.1), material=mat_metal)
    
    # Pistón de gas
    create_primitive('CYLINDER', "Piston", (0, 0, 0.25), (0.08, 0.08, 0.4), material=mat_metal)
    create_primitive('CYLINDER', "Piston_Cover", (0, 0, 0.2), (0.1, 0.1, 0.3), material=mat_plastic)

    # 6. Estrella y Ruedas
    star_center = create_primitive('CYLINDER', "Estrella_Centro", (0, 0, 0.1), (0.12, 0.12, 0.1), material=mat_plastic)
    
    for i in range(5):
        angle = math.radians(i * (360/5))
        leg_len = 0.35
        
        # Pata
        lx = math.sin(angle) * (leg_len / 2)
        ly = math.cos(angle) * (leg_len / 2)
        leg = create_primitive('CUBE', f"Pata_{i}", (lx, ly, 0.1), (0.06, leg_len, 0.04), (0, 0, -angle), mat_plastic)
        add_bevel(leg)

        # Rueda (Caster)
        wx = math.sin(angle) * leg_len
        wy = math.cos(angle) * leg_len
        
        # Soporte rueda
        create_primitive('CYLINDER', f"Rueda_Soporte_{i}", (wx, wy, 0.06), (0.03, 0.03, 0.08), material=mat_plastic)
        # Rueda en sí (doble disco simple)
        wheel = create_primitive('CYLINDER', f"Rueda_{i}", (wx, wy, 0.03), (0.08, 0.08, 0.04), (0, math.radians(90), angle), mat_black)

    # Crear un objeto Empty para mover toda la silla junta fácilmente
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    root = bpy.context.active_object
    root.name = "SillaGamer_ROOT"
    collection.objects.link(root)
    # Mover root a la colección correcta si se creó fuera
    for coll in root.users_collection:
        if coll != collection:
            coll.objects.unlink(root)

    # Emparentar todo al root
    for obj in collection.objects:
        if obj != root:
            obj.parent = root

    # --- AJUSTES FINALES (Escala y Rotación) ---
    # Ajusta estos números si la silla sale muy chica o mal orientada
    root.scale = (3.0, 3.0, 3.0)  # 3 veces más grande (ajusta según tu escritorio)
    root.rotation_euler = (0, 0, math.radians(-90)) # Rotada -90 grados en Z (mirando al frente)

    print("Silla Gamer Pro creada en la colección 'SillaGamer_Pro'")

if __name__ == "__main__":
    create_gamer_chair()
