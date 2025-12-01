import bpy

def improve_wall_material():
    # Nombre del material creado en gamer_room.py
    mat_name = "Room_Wall_DarkGrey"
    mat = bpy.data.materials.get(mat_name)
    
    if not mat:
        print(f"Material '{mat_name}' no encontrado. Asegúrate de haber creado la habitación primero (gamer_room.py).")
        return

    print(f"Mejorando material: {mat_name}...")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # --- NODOS ---
    
    # Output y Shader Principal
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (800, 0)

    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (500, 0)
    bsdf.inputs['Roughness'].default_value = 0.9 # Pared mate
    
    # 1. Coordenadas y Mapeo (Para que la textura no dependa del tamaño del objeto)
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)
    
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-600, 0)
    
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])

    # 2. Textura de Ruido (Simula la irregularidad de la pintura/yeso)
    noise = nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 80.0  # Grano fino
    noise.inputs['Detail'].default_value = 16.0 # Mucho detalle
    noise.inputs['Roughness'].default_value = 0.6
    noise.location = (-400, 0)
    
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])

    # 3. Bump (Relieve) - Para que la luz interactúe con la textura
    bump = nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.1 # Relieve sutil
    bump.inputs['Distance'].default_value = 0.1
    bump.location = (200, -200)
    
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])

    # 4. Color (Variación sutil para que no se vea plano)
    # Usamos un ColorRamp para controlar el contraste del ruido
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (-100, 200)
    color_ramp.color_ramp.elements[0].position = 0.3
    color_ramp.color_ramp.elements[1].position = 0.7
    # Color oscuro (grietas/sombras micro)
    color_ramp.color_ramp.elements[0].color = (0.08, 0.08, 0.09, 1) 
    # Color base (gris azulado oscuro)
    color_ramp.color_ramp.elements[1].color = (0.12, 0.12, 0.14, 1)
    
    links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], bsdf.inputs['Base Color'])

    # Conectar al output
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    print("¡Paredes actualizadas! Ahora tienen textura de pintura mate con relieve.")

if __name__ == "__main__":
    improve_wall_material()
