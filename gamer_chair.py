import bpy
import math

def create_gamer_chair():
    # Limpiar la escena (opcional, ten cuidado si tienes otras cosas)
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # Colección para la silla
    collection = bpy.data.collections.new("SillaGamer")
    bpy.context.scene.collection.children.link(collection)
    
    # Helper para crear objetos y asignarlos a la colección
    def create_cube(name, location, scale, rotation=(0,0,0)):
        bpy.ops.mesh.primitive_cube_add(size=1, location=location, rotation=rotation)
        obj = bpy.context.active_object
        obj.name = name
        obj.scale = scale
        # Mover a la colección
        for coll in obj.users_collection:
            coll.objects.unlink(obj)
        collection.objects.link(obj)
        return obj

    def create_cylinder(name, location, radius, depth, rotation=(0,0,0)):
        bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=location, rotation=rotation)
        obj = bpy.context.active_object
        obj.name = name
        # Mover a la colección
        for coll in obj.users_collection:
            coll.objects.unlink(obj)
        collection.objects.link(obj)
        return obj

    # 1. Asiento
    seat = create_cube("Asiento", (0, 0, 0.5), (0.6, 0.6, 0.1))

    # 2. Respaldo
    # Un poco inclinado hacia atrás
    backrest = create_cube("Respaldo", (0, 0.25, 1.1), (0.5, 0.1, 1.2))
    backrest.rotation_euler = (math.radians(-10), 0, 0)

    # 3. Cojín lumbar (simple)
    lumbar = create_cube("CojinLumbar", (0, 0.18, 0.7), (0.3, 0.05, 0.15))
    lumbar.rotation_euler = (math.radians(-10), 0, 0)

    # 4. Reposacabezas
    headrest = create_cube("Reposacabezas", (0, 0.32, 1.65), (0.3, 0.08, 0.2))
    headrest.rotation_euler = (math.radians(-10), 0, 0)

    # 5. Reposabrazos (Izquierdo y Derecho)
    arm_height = 0.8
    arm_offset_x = 0.35
    
    # Soportes verticales
    create_cube("SoporteBrazo_L", (-arm_offset_x, 0, 0.65), (0.05, 0.05, 0.4))
    create_cube("SoporteBrazo_R", (arm_offset_x, 0, 0.65), (0.05, 0.05, 0.4))
    
    # Parte superior
    create_cube("Reposabrazo_L", (-arm_offset_x, 0, arm_height), (0.08, 0.4, 0.05))
    create_cube("Reposabrazo_R", (arm_offset_x, 0, arm_height), (0.08, 0.4, 0.05))

    # 6. Base (Pistón y Estrella)
    # Pistón central
    create_cylinder("Piston", (0, 0, 0.25), 0.05, 0.5)

    # Estrella base (5 patas)
    for i in range(5):
        angle = math.radians(i * (360/5))
        leg_len = 0.35
        x = math.sin(angle) * (leg_len / 2)
        y = math.cos(angle) * (leg_len / 2)
        
        leg = create_cube(f"Pata_{i}", (x, y, 0.1), (0.05, leg_len, 0.05))
        leg.rotation_euler = (0, 0, -angle)
        
        # Ruedas
        wheel_x = math.sin(angle) * leg_len
        wheel_y = math.cos(angle) * leg_len
        create_cylinder(f"Rueda_{i}", (wheel_x, wheel_y, 0.05), 0.05, 0.05, (0, math.radians(90), angle))

    print("Silla Gamer creada exitosamente.")

if __name__ == "__main__":
    create_gamer_chair()
