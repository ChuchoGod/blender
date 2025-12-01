import bpy
import math
import random

def create_gamer_pc():
    # Nombre de la colección
    collection_name = "PC_Gamer_Ultra"
    
    # Crear colección
    collection = bpy.data.collections.new(collection_name)
    bpy.context.scene.collection.children.link(collection)

    # --- MATERIALES ---
    def create_material(name, color, type='PRINCIPLED', emission_strength=1.0, transparency=0.0):
        mat = bpy.data.materials.get(name)
        if not mat:
            mat = bpy.data.materials.new(name=name)
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            
            # Limpiar nodos por defecto
            nodes.clear()
            
            # Output
            output = nodes.new(type='ShaderNodeOutputMaterial')
            output.location = (400, 0)

            if type == 'PRINCIPLED':
                shader = nodes.new(type='ShaderNodeBsdfPrincipled')
                shader.location = (0, 0)
                shader.inputs['Base Color'].default_value = color
                shader.inputs['Roughness'].default_value = 0.2
                shader.inputs['Metallic'].default_value = 0.8 if "Metal" in name else 0.1
                
                if transparency > 0:
                    # Ajuste para que el vidrio sea transparente inmediatamente (Alpha bajo)
                    shader.inputs['Alpha'].default_value = 0.2 
                    shader.inputs['Transmission Weight'].default_value = transparency
                    shader.inputs['Roughness'].default_value = 0.0
                    
                    # Compatibilidad con versiones antiguas
                    if hasattr(mat, 'blend_method'):
                        mat.blend_method = 'BLEND'
                    if hasattr(mat, 'shadow_method'):
                        mat.shadow_method = 'NONE'
                
                mat.node_tree.links.new(shader.outputs['BSDF'], output.inputs['Surface'])
                
            elif type == 'EMISSION':
                shader = nodes.new(type='ShaderNodeEmission')
                shader.location = (0, 0)
                shader.inputs['Color'].default_value = color
                shader.inputs['Strength'].default_value = emission_strength
                mat.node_tree.links.new(shader.outputs['Emission'], output.inputs['Surface'])
                
        return mat

    # Definir materiales
    mat_case_black = create_material("PC_Case_Black", (0.05, 0.05, 0.05, 1))
    mat_glass = create_material("PC_Glass", (0.9, 0.9, 0.9, 1), transparency=0.95)
    mat_pcb = create_material("PC_Motherboard", (0.02, 0.1, 0.02, 1))
    mat_gpu = create_material("PC_GPU_Plastic", (0.1, 0.1, 0.1, 1))
    mat_metal = create_material("PC_Metal_Silver", (0.8, 0.8, 0.8, 1))
    
    # RGB Materials (Neon)
    mat_rgb_blue = create_material("RGB_Blue", (0.0, 0.5, 1.0, 1), type='EMISSION', emission_strength=15.0)
    mat_rgb_purple = create_material("RGB_Purple", (0.6, 0.0, 1.0, 1), type='EMISSION', emission_strength=15.0)
    mat_rgb_red = create_material("RGB_Red", (1.0, 0.1, 0.1, 1), type='EMISSION', emission_strength=15.0)

    # --- HELPERS ---
    def create_obj(primitive_type, name, location, scale, rotation=(0,0,0), material=None):
        if primitive_type == 'CUBE':
            bpy.ops.mesh.primitive_cube_add(size=1, location=location, rotation=rotation)
        elif primitive_type == 'CYLINDER':
            bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=1, location=location, rotation=rotation)
            
        obj = bpy.context.active_object
        obj.name = name
        obj.scale = scale
        
        if material:
            if obj.data.materials:
                obj.data.materials[0] = material
            else:
                obj.data.materials.append(material)
        
        # Mover a colección
        for coll in obj.users_collection:
            coll.objects.unlink(obj)
        collection.objects.link(obj)
        
        return obj

    # --- CONSTRUCCIÓN ---
    
    # Dimensiones del gabinete
    case_w, case_d, case_h = 0.22, 0.45, 0.48 # Metros aprox
    
    # 1. Gabinete (Chasis)
    # Estructura principal (hueca visualmente simulada con paneles)
    # Panel trasero/fondo/techo/suelo
    chassis = create_obj('CUBE', "Chasis_Main", (0, 0, case_h/2), (case_w, case_d, case_h), material=mat_case_black)
    
    # Panel frontal (Plástico/Metal)
    front_panel = create_obj('CUBE', "Panel_Frontal", (0, -case_d/2 - 0.01, case_h/2), (case_w, 0.02, case_h), material=mat_case_black)
    
    # Panel lateral (Vidrio Templado)
    glass_panel = create_obj('CUBE', "Panel_Vidrio", (case_w/2 + 0.005, 0, case_h/2), (0.01, case_d-0.02, case_h-0.02), material=mat_glass)

    # Patas
    for x in [-1, 1]:
        for y in [-1, 1]:
            create_obj('CYLINDER', "Pata", (x*(case_w/2 - 0.03), y*(case_d/2 - 0.03), 0.01), (0.04, 0.04, 0.02), material=mat_case_black)

    # 2. Componentes Internos
    
    # Motherboard (Placa base)
    mobo = create_obj('CUBE', "Motherboard", (-case_w/2 + 0.02, 0, case_h/2 + 0.05), (0.01, 0.24, 0.30), material=mat_pcb)
    
    # GPU (Tarjeta Gráfica) - Grande y con RGB
    gpu_z = case_h/2 - 0.05
    gpu = create_obj('CUBE', "GPU_Body", (-0.02, 0, gpu_z), (0.12, 0.28, 0.04), material=mat_gpu)
    # Tira RGB en la GPU
    create_obj('CUBE', "GPU_RGB", (0.04, 0, gpu_z + 0.02), (0.005, 0.25, 0.002), material=mat_rgb_purple)
    
    # CPU Cooler (Disipador por aire)
    cooler = create_obj('CUBE', "CPU_Cooler_Block", (-case_w/2 + 0.06, 0.05, case_h/2 + 0.12), (0.08, 0.08, 0.02), material=mat_metal)
    fan_cpu = create_obj('CYLINDER', "CPU_Fan", (-case_w/2 + 0.11, 0.05, case_h/2 + 0.12), (0.09, 0.09, 0.02), (0, math.radians(90), 0), material=mat_rgb_blue)

    # RAM Sticks (2 módulos)
    for i in range(2):
        ram_y = 0.08 + (i * 0.015)
        create_obj('CUBE', f"RAM_{i}", (-case_w/2 + 0.04, ram_y, case_h/2 + 0.12), (0.005, 0.13, 0.035), material=mat_rgb_red)

    # Fuente de poder (PSU Shroud)
    shroud = create_obj('CUBE', "PSU_Shroud", (0, 0, 0.06), (case_w-0.01, case_d-0.01, 0.12), material=mat_case_black)

    # 3. Ventiladores del Gabinete (RGB Fans)
    def create_fan(name, pos, rot, color_mat):
        # Marco
        create_obj('CYLINDER', f"{name}_Frame", pos, (0.12, 0.12, 0.025), rot, material=mat_case_black)
        # Luz (Anillo interior)
        create_obj('CYLINDER', f"{name}_Light", pos, (0.10, 0.10, 0.026), rot, material=color_mat)
        # Centro
        create_obj('CYLINDER', f"{name}_Hub", pos, (0.03, 0.03, 0.03), rot, material=mat_case_black)

    # 3 Ventiladores Frontales
    for i in range(3):
        z_pos = 0.10 + (i * 0.13)
        create_fan(f"Fan_Front_{i}", (0, -case_d/2 + 0.02, z_pos), (math.radians(90), 0, 0), mat_rgb_blue)

    # 1 Ventilador Trasero
    create_fan("Fan_Rear", (0, case_d/2 - 0.02, case_h - 0.10), (math.radians(90), 0, 0), mat_rgb_purple)

    # --- ROOT OBJECT ---
    bpy.ops.object.empty_add(type='ARROWS', location=(0, 0, 0))
    root = bpy.context.active_object
    root.name = "PC_Gamer_ROOT"
    collection.objects.link(root)
    for coll in root.users_collection:
        if coll != collection:
            coll.objects.unlink(root)

    # Emparentar
    for obj in collection.objects:
        if obj != root:
            obj.parent = root

    # --- AJUSTES FINALES ---
    # Escala y posición por defecto para que quede bien sobre un escritorio
    root.scale = (2.5, 2.5, 2.5) 
    root.location = (1.5, 0, 0.75) # Un poco a la derecha y arriba (asumiendo escritorio estándar)
    
    print("PC Gamer Ultra creada exitosamente.")

if __name__ == "__main__":
    create_gamer_pc()
