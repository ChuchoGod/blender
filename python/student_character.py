import bpy
import math

def create_student_character():
    collection_name = "Personaje_Estudiante"
    collection = bpy.data.collections.new(collection_name)
    bpy.context.scene.collection.children.link(collection)

    # --- MATERIALES ---
    def create_material(name, color, roughness=0.5):
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

    mat_skin = create_material("Skin_Tone", (0.8, 0.6, 0.5, 1), roughness=0.6)
    mat_shirt = create_material("Student_Hoodie_Grey", (0.2, 0.2, 0.25, 1), roughness=0.9)
    mat_pants = create_material("Student_Jeans_Blue", (0.1, 0.2, 0.5, 1), roughness=0.8)
    mat_shoes = create_material("Student_Sneakers_White", (0.9, 0.9, 0.9, 1), roughness=0.5)
    mat_hair = create_material("Student_Hair_Brown", (0.15, 0.1, 0.05, 1), roughness=0.8)
    mat_backpack = create_material("Student_Backpack_Red", (0.6, 0.1, 0.1, 1), roughness=0.7)

    # --- HELPERS ---
    def create_obj(type, name, loc, scale, rot=(0,0,0), mat=None):
        if type == 'CUBE':
            bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
        elif type == 'SPHERE':
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=loc, rotation=rot)
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
        
        # Suavizar
        if type in ['SPHERE', 'CYLINDER']:
            bpy.ops.object.shade_smooth()
            
        return obj

    # --- CONSTRUCCIÓN (Low Poly Stylized) ---
    
    # Altura total aprox: 1.75m
    
    # 1. Piernas (Pantalones)
    leg_h = 0.85
    leg_dist = 0.15
    # Pierna Izq
    create_obj('CYLINDER', "Pierna_L", (-leg_dist, 0, leg_h/2), (0.12, 0.12, leg_h), mat=mat_pants)
    # Pierna Der
    create_obj('CYLINDER', "Pierna_R", (leg_dist, 0, leg_h/2), (0.12, 0.12, leg_h), mat=mat_pants)

    # 2. Zapatos
    create_obj('CUBE', "Zapato_L", (-leg_dist, -0.05, 0.05), (0.14, 0.28, 0.1), mat=mat_shoes)
    create_obj('CUBE', "Zapato_R", (leg_dist, -0.05, 0.05), (0.14, 0.28, 0.1), mat=mat_shoes)

    # 3. Torso (Hoodie)
    torso_h = 0.6
    torso_z = leg_h + torso_h/2
    create_obj('CUBE', "Torso", (0, 0, torso_z), (0.45, 0.25, torso_h), mat=mat_shirt)

    # 4. Brazos (Mangas + Piel)
    arm_len = 0.6
    arm_z = leg_h + torso_h - 0.1
    
    # Brazo Izq (Relajado al lado)
    create_obj('CYLINDER', "Brazo_L", (-0.32, 0, arm_z - arm_len/2), (0.09, 0.09, arm_len), mat=mat_shirt)
    create_obj('SPHERE', "Mano_L", (-0.32, 0, arm_z - arm_len - 0.05), (0.08, 0.08, 0.08), mat=mat_skin)
    
    # Brazo Der (Relajado)
    create_obj('CYLINDER', "Brazo_R", (0.32, 0, arm_z - arm_len/2), (0.09, 0.09, arm_len), mat=mat_shirt)
    create_obj('SPHERE', "Mano_R", (0.32, 0, arm_z - arm_len - 0.05), (0.08, 0.08, 0.08), mat=mat_skin)

    # 5. Cabeza
    head_z = leg_h + torso_h + 0.15
    create_obj('SPHERE', "Cabeza", (0, 0, head_z), (0.22, 0.25, 0.28), mat=mat_skin)
    
    # Cuello
    create_obj('CYLINDER', "Cuello", (0, 0, leg_h + torso_h), (0.08, 0.08, 0.15), mat=mat_skin)

    # 6. Pelo (Casco simple)
    create_obj('SPHERE', "Pelo", (0, -0.02, head_z + 0.05), (0.24, 0.26, 0.25), mat=mat_hair)

    # 7. Mochila (El toque de estudiante)
    backpack_z = leg_h + torso_h/2
    bp = create_obj('CUBE', "Mochila", (0, 0.2, backpack_z), (0.35, 0.15, 0.45), mat=mat_backpack)
    # Tirantes (Simulados)
    create_obj('CUBE', "Tirante_L", (-0.1, 0.13, backpack_z + 0.1), (0.05, 0.02, 0.3), (math.radians(15), 0, 0), mat=mat_backpack)
    create_obj('CUBE', "Tirante_R", (0.1, 0.13, backpack_z + 0.1), (0.05, 0.02, 0.3), (math.radians(15), 0, 0), mat=mat_backpack)

    # --- ROOT OBJECT ---
    bpy.ops.object.empty_add(type='ARROWS', location=(0, 0, 0))
    root = bpy.context.active_object
    root.name = "Estudiante_ROOT"
    collection.objects.link(root)
    for coll in root.users_collection:
        if coll != collection: coll.objects.unlink(root)

    # Emparentar
    for obj in collection.objects:
        if obj != root:
            obj.parent = root

    # Posicionar en la habitación (De pie cerca de la silla)
    root.location = (-1.0, -1.0, 0)
    root.rotation_euler = (0, 0, math.radians(-45)) # Mirando hacia el setup

    print("Personaje Estudiante creado.")

if __name__ == "__main__":
    create_student_character()
