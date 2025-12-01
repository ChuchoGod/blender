import bpy

def activar_vista_materiales():
    print("Activando vista de materiales...")
    found = False
    
    # Recorremos todas las áreas de la pantalla actual
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    # Cambiamos el modo de sombreado a MATERIAL
                    space.shading.type = 'MATERIAL'
                    found = True
    
    if found:
        print("¡Listo! Ahora deberías ver los colores.")
    else:
        print("No se encontró ninguna vista 3D activa.")

if __name__ == "__main__":
    activar_vista_materiales()
