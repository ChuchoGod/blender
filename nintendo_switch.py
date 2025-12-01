import bpy
import math

def create_nintendo_switch():
    collection_name = "Nintendo_Switch"
    collection = bpy.data.collections.new(collection_name)
    bpy.context.scene.collection.children.link(collection)

    # --- MATERIALES ---
    def create_material(name, color, roughness=0.5, emission=False):
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
                shader.inputs['Strength'].default_value = 2.0
            else:
                shader = nodes.new('ShaderNodeBsdfPrincipled')
                shader.inputs['Base Color'].default_value = color
                shader.inputs['Roughness'].default_value = roughness
                shader.inputs['Metallic'].default_value = 0.1
            
            shader.location = (0, 0)
            mat.node_tree.links.new(shader.outputs[0], output.inputs['Surface'])
        return mat

    mat_body = create_material("Switch_Black", (0.1, 0.1, 0.1, 1), roughness=0.4)
    mat_screen_off = create_material("Switch_Screen", (0.02, 0.02, 0.02, 1), roughness=0.1)
    mat_joy_l = create_material("JoyCon_Blue", (0.0, 0.6, 1.0, 1), roughness=0.4) # Neon Blue
    mat_joy_r = create_material("JoyCon_Red", (1.0, 0.2, 0.2, 1), roughness=0.4)  # Neon Red
    mat_buttons = create_material("Switch_Buttons", (0.05, 0.05, 0.05, 1), roughness=0.5)

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
        
        # Bevel modifier for smoothness
        if type == 'CUBE':
            mod = obj.modifiers.new(name="Bevel", type='BEVEL')
            mod.width = 0.02 if "Joy" in name else 0.005
            mod.segments = 3
            bpy.ops.object.shade_smooth()
            
        return obj

    # --- DIMENSIONES ---
    # Escala realista aproximada (en metros)
    console_w = 0.17
    console_h = 0.10
    console_d = 0.015
    joy_w = 0.035

    # --- CONSTRUCCIÓN ---

    # 1. Consola Central (Tablet)
    tablet = create_obj('CUBE', "Switch_Tablet", (0, 0, 0), (console_w, console_d, console_h), mat=mat_body)
    
    # Pantalla
    screen_w = console_w - 0.02
    screen_h = console_h - 0.015
    create_obj('CUBE', "Switch_Screen", (0, -console_d/2 - 0.001, 0), (screen_w, 0.001, screen_h), mat=mat_screen_off)

    # 2. Joy-Con Izquierdo (Azul)
    joy_l_pos = (-console_w/2 - joy_w/2, 0, 0)
    create_obj('CUBE', "JoyCon_L", joy_l_pos, (joy_w, console_d, console_h), mat=mat_joy_l)
    
    # Joystick L
    stick_l_pos = (joy_l_pos[0], -console_d/2 - 0.005, 0.02)
    create_obj('CYLINDER', "Stick_L", stick_l_pos, (0.015, 0.015, 0.005), (math.radians(90), 0, 0), mat=mat_buttons)
    
    # Botones Flechas (D-Pad separado)
    btn_size = 0.008
    btn_dist = 0.012
    dpad_center = (joy_l_pos[0], -console_d/2 - 0.002, -0.02)
    # Arriba, Abajo, Izq, Der
    create_obj('CYLINDER', "Btn_Up", (dpad_center[0], dpad_center[1], dpad_center[2] + btn_dist), (btn_size, btn_size, 0.002), (math.radians(90), 0, 0), mat=mat_buttons)
    create_obj('CYLINDER', "Btn_Down", (dpad_center[0], dpad_center[1], dpad_center[2] - btn_dist), (btn_size, btn_size, 0.002), (math.radians(90), 0, 0), mat=mat_buttons)
    create_obj('CYLINDER', "Btn_Left", (dpad_center[0] - btn_dist, dpad_center[1], dpad_center[2]), (btn_size, btn_size, 0.002), (math.radians(90), 0, 0), mat=mat_buttons)
    create_obj('CYLINDER', "Btn_Right", (dpad_center[0] + btn_dist, dpad_center[1], dpad_center[2]), (btn_size, btn_size, 0.002), (math.radians(90), 0, 0), mat=mat_buttons)
    
    # Botón -
    create_obj('CUBE', "Btn_Minus", (joy_l_pos[0] + 0.01, -console_d/2 - 0.002, 0.04), (0.008, 0.002, 0.002), mat=mat_buttons)

    # 3. Joy-Con Derecho (Rojo)
    joy_r_pos = (console_w/2 + joy_w/2, 0, 0)
    create_obj('CUBE', "JoyCon_R", joy_r_pos, (joy_w, console_d, console_h), mat=mat_joy_r)
    
    # Joystick R (Más abajo)
    stick_r_pos = (joy_r_pos[0], -console_d/2 - 0.005, -0.02)
    create_obj('CYLINDER', "Stick_R", stick_r_pos, (0.015, 0.015, 0.005), (math.radians(90), 0, 0), mat=mat_buttons)
    
    # Botones ABXY (Más arriba)
    abxy_center = (joy_r_pos[0], -console_d/2 - 0.002, 0.02)
    create_obj('CYLINDER', "Btn_X", (abxy_center[0], abxy_center[1], abxy_center[2] + btn_dist), (btn_size, btn_size, 0.002), (math.radians(90), 0, 0), mat=mat_buttons)
    create_obj('CYLINDER', "Btn_B", (abxy_center[0], abxy_center[1], abxy_center[2] - btn_dist), (btn_size, btn_size, 0.002), (math.radians(90), 0, 0), mat=mat_buttons)
    create_obj('CYLINDER', "Btn_Y", (abxy_center[0] - btn_dist, abxy_center[1], abxy_center[2]), (btn_size, btn_size, 0.002), (math.radians(90), 0, 0), mat=mat_buttons)
    create_obj('CYLINDER', "Btn_A", (abxy_center[0] + btn_dist, abxy_center[1], abxy_center[2]), (btn_size, btn_size, 0.002), (math.radians(90), 0, 0), mat=mat_buttons)

    # Botón +
    create_obj('CUBE', "Btn_Plus_V", (joy_r_pos[0] - 0.01, -console_d/2 - 0.002, 0.04), (0.002, 0.002, 0.008), mat=mat_buttons)
    create_obj('CUBE', "Btn_Plus_H", (joy_r_pos[0] - 0.01, -console_d/2 - 0.002, 0.04), (0.008, 0.002, 0.002), mat=mat_buttons)

    # --- ROOT OBJECT ---
    bpy.ops.object.empty_add(type='ARROWS', location=(0, 0, 0))
    root = bpy.context.active_object
    root.name = "Nintendo_Switch_ROOT"
    collection.objects.link(root)
    for coll in root.users_collection:
        if coll != collection: coll.objects.unlink(root)

    # Emparentar
    for obj in collection.objects:
        if obj != root:
            obj.parent = root

    # Posicionar sobre el escritorio (asumiendo que el escritorio está en Z=0.75 aprox)
    # La ponemos un poco inclinada como si estuviera en su patita o apoyada
    root.location = (0.5, -0.2, 0.76) 
    root.rotation_euler = (math.radians(-15), 0, math.radians(10))
    root.scale = (1.5, 1.5, 1.5) # Un poco más grande para que se vea bien

    print("Nintendo Switch creada.")

if __name__ == "__main__":
    create_nintendo_switch()
