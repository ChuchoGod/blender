import bpy
import math

def create_minecraft_steve():
    collection_name = "Minecraft_Steve"
    collection = bpy.data.collections.new(collection_name)
    bpy.context.scene.collection.children.link(collection)

    # --- MATERIALES (Colores Planos de Steve) ---
    def create_material(name, color):
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
            shader.inputs['Roughness'].default_value = 1.0 # Mate, como bloques
            shader.inputs['Specular IOR Level'].default_value = 0.0
            shader.location = (0, 0)
            mat.node_tree.links.new(shader.outputs[0], output.inputs['Surface'])
        return mat

    # Colores aproximados de Steve
    mat_skin = create_material("Steve_Skin", (0.7, 0.5, 0.4, 1)) # Piel bronceada
    mat_shirt_cyan = create_material("Steve_Shirt", (0.0, 0.6, 0.7, 1)) # Cyan
    mat_pants_blue = create_material("Steve_Pants", (0.15, 0.15, 0.6, 1)) # Azul oscuro
    mat_shoes_grey = create_material("Steve_Shoes", (0.2, 0.2, 0.2, 1)) # Gris oscuro
    mat_hair = create_material("Steve_Hair", (0.15, 0.1, 0.05, 1)) # Marrón oscuro
    mat_eyes_white = create_material("Steve_Eyes_White", (1.0, 1.0, 1.0, 1))
    mat_eyes_pupil = create_material("Steve_Eyes_Pupil", (0.3, 0.2, 0.6, 1)) # Violeta/Azul oscuro

    # --- HELPERS ---
    def create_block(name, loc, size, mat=None):
        # size es una tupla (x, y, z)
        bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
        obj = bpy.context.active_object
        obj.name = name
        obj.scale = size
        
        if mat:
            if obj.data.materials: obj.data.materials[0] = mat
            else: obj.data.materials.append(mat)
            
        for coll in obj.users_collection: coll.objects.unlink(obj)
        collection.objects.link(obj)
        return obj

    # --- CONSTRUCCIÓN (Escala: 1 unidad = 1 metro aprox, Steve mide ~1.8m) ---
    # Pixel size reference: 1 pixel = 0.0625m (1/16)
    px = 0.06
    
    # 1. Piernas (4x12x4 pixels cada una)
    leg_w = 4 * px
    leg_h = 12 * px
    leg_d = 4 * px
    
    # Pierna Derecha
    leg_r = create_block("Pierna_R", (leg_w/2, 0, leg_h/2), (leg_w, leg_d, leg_h), mat=mat_pants_blue)
    # Zapato R (Parte inferior de la pierna, visualmente separado o pintado)
    # Para simplificar, hacemos un bloque extra para el zapato o asumimos textura. 
    # Haremos el estilo "geometría pura":
    # Zapatos (Bottom 2 pixels)
    shoe_h = 2 * px
    # Ajustamos la pierna para que sea pantalón y creamos zapato
    leg_r.scale = (leg_w, leg_d, leg_h - shoe_h)
    leg_r.location = (leg_w/2, 0, shoe_h + (leg_h - shoe_h)/2)
    create_block("Zapato_R", (leg_w/2, 0, shoe_h/2), (leg_w, leg_d, shoe_h), mat=mat_shoes_grey)

    # Pierna Izquierda
    leg_l = create_block("Pierna_L", (-leg_w/2, 0, shoe_h + (leg_h - shoe_h)/2), (leg_w, leg_d, leg_h - shoe_h), mat=mat_pants_blue)
    create_block("Zapato_L", (-leg_w/2, 0, shoe_h/2), (leg_w, leg_d, shoe_h), mat=mat_shoes_grey)

    # 2. Cuerpo (Torso) (8x12x4 pixels)
    body_w = 8 * px
    body_h = 12 * px
    body_d = 4 * px
    body_z = leg_h + body_h/2
    
    create_block("Torso", (0, 0, body_z), (body_w, body_d, body_h), mat=mat_shirt_cyan)

    # 3. Brazos (4x12x4 pixels)
    arm_w = 4 * px
    arm_h = 12 * px
    arm_d = 4 * px
    arm_z = leg_h + body_h - arm_h/2 # Pegado al hombro
    
    # Brazo Derecho
    arm_r = create_block("Brazo_R", (body_w/2 + arm_w/2, 0, arm_z), (arm_w, arm_d, arm_h), mat=mat_skin)
    # Manga (Top 4 pixels)
    sleeve_h = 4 * px
    # Ajustamos brazo piel
    arm_r.scale = (arm_w, arm_d, arm_h - sleeve_h)
    arm_r.location = (body_w/2 + arm_w/2, 0, arm_z - sleeve_h/2)
    # Manga
    create_block("Manga_R", (body_w/2 + arm_w/2, 0, leg_h + body_h - sleeve_h/2), (arm_w + 0.005, arm_d + 0.005, sleeve_h), mat=mat_shirt_cyan)

    # Brazo Izquierdo
    arm_l = create_block("Brazo_L", (-body_w/2 - arm_w/2, 0, arm_z - sleeve_h/2), (arm_w, arm_d, arm_h - sleeve_h), mat=mat_skin)
    create_block("Manga_L", (-body_w/2 - arm_w/2, 0, leg_h + body_h - sleeve_h/2), (arm_w + 0.005, arm_d + 0.005, sleeve_h), mat=mat_shirt_cyan)

    # 4. Cabeza (8x8x8 pixels)
    head_s = 8 * px
    head_z = leg_h + body_h + head_s/2
    create_block("Cabeza", (0, 0, head_z), (head_s, head_s, head_s), mat=mat_skin)
    
    # Pelo (Top layer + sides)
    # Gorro de pelo (Top)
    create_block("Pelo_Top", (0, 0, head_z + head_s/2 + 0.005), (head_s, head_s, 0.01), mat=mat_hair)
    # Lados del pelo (Frontal, Trasero, Lados) - Simplificado
    # Flequillo
    create_block("Pelo_Front", (0, -head_s/2 - 0.005, head_z + head_s/4), (head_s, 0.01, head_s/2), mat=mat_hair)
    # Atrás
    create_block("Pelo_Back", (0, head_s/2 + 0.005, head_z), (head_s, 0.01, head_s), mat=mat_hair)
    # Lados
    create_block("Pelo_Side_R", (head_s/2 + 0.005, 0, head_z), (0.01, head_s, head_s), mat=mat_hair)
    create_block("Pelo_Side_L", (-head_s/2 - 0.005, 0, head_z), (0.01, head_s, head_s), mat=mat_hair)

    # Cara (Ojos y Boca/Barba)
    # Ojos (2x1 pixels)
    eye_w = 2 * px
    eye_h = 1 * px
    eye_y = -head_s/2 - 0.01 # Un poco salido
    eye_z = head_z # Mitad de la cara aprox
    
    # Ojo Blanco R
    create_block("Ojo_Blanco_R", (px*2, eye_y, eye_z), (px, 0.005, px), mat=mat_eyes_white)
    # Pupila R
    create_block("Pupila_R", (px*3, eye_y, eye_z), (px, 0.005, px), mat=mat_eyes_pupil)
    
    # Ojo Blanco L
    create_block("Ojo_Blanco_L", (-px*2, eye_y, eye_z), (px, 0.005, px), mat=mat_eyes_white)
    # Pupila L
    create_block("Pupila_L", (-px*3, eye_y, eye_z), (px, 0.005, px), mat=mat_eyes_pupil)
    
    # Nariz/Boca (4x1 pixels) - La famosa "barba" o sonrisa
    create_block("Boca", (0, eye_y, eye_z - px*1.5), (px*4, 0.005, px), mat=mat_hair)

    # --- ROOT OBJECT ---
    bpy.ops.object.empty_add(type='ARROWS', location=(0, 0, 0))
    root = bpy.context.active_object
    root.name = "Steve_ROOT"
    collection.objects.link(root)
    for coll in root.users_collection:
        if coll != collection: coll.objects.unlink(root)

    # Emparentar
    for obj in collection.objects:
        if obj != root:
            obj.parent = root

    # Posicionar
    root.location = (-1.0, -1.0, 0)
    root.rotation_euler = (0, 0, math.radians(-45))

    print("Minecraft Steve creado.")

if __name__ == "__main__":
    create_minecraft_steve()
