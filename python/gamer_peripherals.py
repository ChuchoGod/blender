import bpy
import math

def create_peripherals():
    collection_name = "Perifericos_Gamer"
    collection = bpy.data.collections.new(collection_name)
    bpy.context.scene.collection.children.link(collection)

    # --- MATERIALES ---
    def create_material(name, color, emission=False, emission_strength=1.0):
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
                shader.inputs['Roughness'].default_value = 0.4
                shader.inputs['Metallic'].default_value = 0.1
            
            shader.location = (0, 0)
            mat.node_tree.links.new(shader.outputs[0], output.inputs['Surface'])
        return mat

    mat_black = create_material("Peri_Black_Plastic", (0.05, 0.05, 0.05, 1))
    mat_screen = create_material("Peri_Screen_Glow", (0.05, 0.1, 0.2, 1), emission=True, emission_strength=2.0)
    mat_rgb = create_material("Peri_RGB_Rainbow", (0.0, 1.0, 1.0, 1), emission=True, emission_strength=3.0)
    mat_mouse_led = create_material("Peri_Mouse_Red", (1.0, 0.0, 0.0, 1), emission=True, emission_strength=5.0)

    # --- HELPERS ---
    def create_obj(type, name, loc, scale, rot=(0,0,0), mat=None):
        if type == 'CUBE':
            bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
        elif type == 'CYLINDER':
            bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=1, location=loc, rotation=rot)
        elif type == 'SPHERE':
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=loc, rotation=rot)
            
        obj = bpy.context.active_object
        obj.name = name
        obj.scale = scale
        
        if mat:
            if obj.data.materials: obj.data.materials[0] = mat
            else: obj.data.materials.append(mat)
        
        # Mover a colección
        for coll in obj.users_collection: coll.objects.unlink(obj)
        collection.objects.link(obj)
        
        # Suavizar si es esfera o cilindro
        if type in ['SPHERE', 'CYLINDER']:
            bpy.ops.object.shade_smooth()
            
        return obj

    # --- 1. MONITOR ---
    # Base
    create_obj('CYLINDER', "Monitor_Base", (0, 0.1, 0.01), (0.4, 0.3, 0.02), mat=mat_black)
    # Soporte vertical
    create_obj('CYLINDER', "Monitor_Stand", (0, 0.15, 0.25), (0.08, 0.08, 0.5), (math.radians(10), 0, 0), mat=mat_black)
    
    # Pantalla (Cuerpo)
    screen_w, screen_h = 1.2, 0.7
    create_obj('CUBE', "Monitor_Body", (0, 0, 0.6), (screen_w, 0.05, screen_h), mat=mat_black)
    # Pantalla (Panel luminoso)
    create_obj('CUBE', "Monitor_Panel", (0, -0.026, 0.6), (screen_w-0.05, 0.01, screen_h-0.05), mat=mat_screen)

    # --- 2. TECLADO ---
    # Ubicación relativa al centro
    kb_loc_y = -0.5
    kb_tilt = math.radians(5)
    
    # Base del teclado
    create_obj('CUBE', "Teclado_Base", (0, kb_loc_y, 0.03), (0.9, 0.35, 0.04), (kb_tilt, 0, 0), mat=mat_black)
    
    # Teclas (Simuladas como tiras RGB para efecto "retroiluminado")
    # Fila 1
    create_obj('CUBE', "Teclas_F1", (0, kb_loc_y + 0.08, 0.05), (0.85, 0.04, 0.02), (kb_tilt, 0, 0), mat=mat_rgb)
    # Fila 2
    create_obj('CUBE', "Teclas_F2", (0, kb_loc_y + 0.02, 0.045), (0.85, 0.04, 0.02), (kb_tilt, 0, 0), mat=mat_rgb)
    # Fila 3
    create_obj('CUBE', "Teclas_F3", (0, kb_loc_y - 0.04, 0.04), (0.85, 0.04, 0.02), (kb_tilt, 0, 0), mat=mat_rgb)
    # Barra espaciadora
    create_obj('CUBE', "Tecla_Espacio", (0, kb_loc_y - 0.1, 0.035), (0.4, 0.05, 0.02), (kb_tilt, 0, 0), mat=mat_rgb)

    # --- 3. MOUSE ---
    mouse_x = 0.7
    mouse_y = -0.5
    
    # Cuerpo del mouse (Esfera aplastada)
    create_obj('SPHERE', "Mouse_Body", (mouse_x, mouse_y, 0.04), (0.15, 0.25, 0.12), mat=mat_black)
    
    # Rueda del mouse (Scroll)
    create_obj('CYLINDER', "Mouse_Wheel", (mouse_x, mouse_y + 0.08, 0.06), (0.02, 0.02, 0.01), (0, math.radians(90), 0), mat=mat_mouse_led)

    # --- ROOT OBJECT ---
    bpy.ops.object.empty_add(type='ARROWS', location=(0, 0, 0))
    root = bpy.context.active_object
    root.name = "Perifericos_ROOT"
    collection.objects.link(root)
    for coll in root.users_collection:
        if coll != collection: coll.objects.unlink(root)

    # Emparentar todo al root
    for obj in collection.objects:
        if obj != root:
            obj.parent = root
            
    # --- AJUSTES FINALES ---
    # Escalar y posicionar sobre el escritorio
    root.scale = (2.0, 2.0, 2.0)
    root.location = (0, 0.3, 0.75) # Altura de escritorio estándar

    print("Monitor, Teclado y Mouse creados exitosamente.")

if __name__ == "__main__":
    create_peripherals()
