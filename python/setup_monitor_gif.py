import bpy
import os

def setup_monitor_debug():
    # 1. Lista de posibles archivos a buscar
    possible_files = ["monitor.gif", "monitor.mp4", "monitor.png", "monitor.jpg"]
    found_file = None
    
    # Carpetas donde buscar:
    # 1. Carpeta del archivo .blend actual (si está guardado)
    # 2. c:\paginas_webs\blender\
    search_folders = [r"c:\paginas_webs\blender"]
    if bpy.data.is_saved:
        search_folders.insert(0, os.path.dirname(bpy.data.filepath))
        
    print(f"Buscando archivos en: {search_folders}")

    for folder in search_folders:
        if not os.path.exists(folder): continue
        for fname in possible_files:
            full_path = os.path.join(folder, fname)
            if os.path.exists(full_path):
                found_file = full_path
                break
        if found_file: break
    
    # --- OBTENER MATERIAL ---
    mat_name = "Peri_Screen_Glow"
    mat = bpy.data.materials.get(mat_name)
    
    if not mat:
        print(f"ERROR CRÍTICO: No existe el material '{mat_name}'.")
        return

    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (600, 0)
    
    emission = nodes.new('ShaderNodeEmission')
    emission.location = (300, 0)
    
    # --- LÓGICA DE VISUALIZACIÓN DE ESTADO ---
    
    if not found_file:
        # ESTADO: ERROR (ROJO)
        print(">>> NO SE ENCONTRÓ NINGÚN ARCHIVO (monitor.gif/mp4/png/jpg) <<<")
        emission.inputs['Color'].default_value = (1.0, 0.0, 0.0, 1.0) # ROJO
        emission.inputs['Strength'].default_value = 5.0
        
        # Crear texto de aviso en 3D
        bpy.ops.object.text_add(location=(0, -1, 2))
        text_obj = bpy.context.active_object
        text_obj.data.body = "ERROR: FALTA ARCHIVO\nmonitor.gif / .mp4"
        text_obj.scale = (0.5, 0.5, 0.5)
        text_obj.rotation_euler = (1.57, 0, 0)
        
    else:
        # ESTADO: ÉXITO (INTENTAR CARGAR)
        print(f">>> ARCHIVO ENCONTRADO: {found_file} <<<")
        
        try:
            tex_image = nodes.new('ShaderNodeTexImage')
            tex_image.location = (0, 0)
            
            img = bpy.data.images.load(found_file, check_existing=True)
            tex_image.image = img
            
            # Configuración si es video/gif
            if found_file.endswith(('.gif', '.mp4', '.avi')):
                img.source = 'MOVIE'
                tex_image.image_user.use_auto_refresh = True
                tex_image.image_user.frame_duration = 250
                tex_image.image_user.frame_start = 1
                tex_image.extension = 'CLIP'
            
            # Mapeo
            tex_coord = nodes.new('ShaderNodeTexCoord')
            tex_coord.location = (-400, 0)
            mapping = nodes.new('ShaderNodeMapping')
            mapping.location = (-200, 0)
            mapping.inputs['Rotation'].default_value = (0, 0, 1.5708) # 90 grados
            
            links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])
            links.new(mapping.outputs['Vector'], tex_image.inputs['Vector'])
            links.new(tex_image.outputs['Color'], emission.inputs['Color'])
            
            emission.inputs['Strength'].default_value = 2.0
            
        except Exception as e:
            print(f"Error cargando imagen: {e}")
            # ESTADO: ERROR DE CARGA (AMARILLO)
            emission.inputs['Color'].default_value = (1.0, 1.0, 0.0, 1.0) # AMARILLO

    links.new(emission.outputs['Emission'], output.inputs['Surface'])

if __name__ == "__main__":
    setup_monitor_debug()