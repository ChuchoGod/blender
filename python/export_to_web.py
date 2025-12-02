import bpy
import os

def export_scene_to_glb():
    # Ruta de destino
    export_path = r"c:\paginas_webs\blender\web_project\scene.glb"
    
    # Asegurarse de que estamos en modo objeto
    if bpy.context.active_object and bpy.context.active_object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    
    # Seleccionar todos los objetos de nuestras colecciones
    bpy.ops.object.select_all(action='DESELECT')
    
    collections_to_export = ["Gamer_Room", "SillaGamer_Pro", "PC_Gamer_Ultra", "Perifericos_Gamer"]
    
    for col_name in collections_to_export:
        if col_name in bpy.data.collections:
            for obj in bpy.data.collections[col_name].objects:
                obj.select_set(True)
    
    # Exportar a GLB (Formato estándar para web 3D)
    bpy.ops.export_scene.gltf(
        filepath=export_path,
        check_existing=False,
        use_selection=True,
        export_format='GLB',
        export_apply=True  # Aplicar modificadores
    )
    
    print(f"Escena exportada exitosamente a: {export_path}")

if __name__ == "__main__":
    export_scene_to_glb()
