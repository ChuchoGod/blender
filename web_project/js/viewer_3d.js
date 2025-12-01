import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// Configuración básica
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x050505);
// Niebla para que no se vea el fin del mundo
scene.fog = new THREE.Fog(0x050505, 5, 25);

const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 100);
camera.position.set(3, 2, 3);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap; // Sombras suaves
renderer.toneMapping = THREE.ACESFilmicToneMapping; // Mejor color
renderer.toneMappingExposure = 1.2;
document.body.appendChild(renderer.domElement);

// Luces
const ambientLight = new THREE.HemisphereLight(0xffffff, 0x444444, 0.6); // Cielo/Suelo
scene.add(ambientLight);

const dirLight = new THREE.DirectionalLight(0xffffff, 1.5);
dirLight.position.set(5, 10, 7);
dirLight.castShadow = true;
dirLight.shadow.mapSize.width = 2048; // Sombras HD
dirLight.shadow.mapSize.height = 2048;
scene.add(dirLight);

// Luz Gamer (Azul/Morada)
const gamerLight = new THREE.PointLight(0x0055ff, 5, 10);
gamerLight.position.set(0, 2, 0);
scene.add(gamerLight);

// Controles de cámara
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.target.set(0, 1, 0);

// Raycaster para detectar clicks
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

// --- LÓGICA DE STEVE ---
let steveObject = null;
let steveLimbs = {
    legL: null, legR: null,
    armL: null, armR: null
};
const keys = { w: false, a: false, s: false, d: false };
const moveSpeed = 0.05;
const rotSpeed = 0.05;
let walkTime = 0; // Para la animación

window.addEventListener('keydown', (e) => {
    const k = e.key.toLowerCase();
    if (keys.hasOwnProperty(k)) keys[k] = true;
});
window.addEventListener('keyup', (e) => {
    const k = e.key.toLowerCase();
    if (keys.hasOwnProperty(k)) keys[k] = false;
});

// Cargar Modelo
const loader = new GLTFLoader();
let monitorObject = null;

loader.load('setup_gamer.glb', function (gltf) {
    const model = gltf.scene;
    scene.add(model);

    // Buscar el objeto del monitor para hacerlo interactivo
    model.traverse((child) => {
        // Buscar a Steve y sus partes
        if (child.name === 'Steve_ROOT') {
            steveObject = child;
            console.log("¡Steve encontrado!");
        }
        // Identificar extremidades (Nombres definidos en minecraft_steve.py)
        if (child.name === 'Pierna_L') steveLimbs.legL = child;
        if (child.name === 'Pierna_R') steveLimbs.legR = child;
        if (child.name === 'Brazo_L') steveLimbs.armL = child;
        if (child.name === 'Brazo_R') steveLimbs.armR = child;

        if (child.isMesh) {
            child.castShadow = true;
            child.receiveShadow = true;
            
            // Identificar el monitor por nombre (del script de Blender)
            if (child.name.includes("Monitor_Panel") || child.name.includes("Monitor_Body")) {
                monitorObject = child;
                // Cambiar cursor al pasar por encima
                child.userData.isClickable = true;
            }
        }
    });

}, undefined, function (error) {
    console.error(error);
});

// Evento Click
window.addEventListener('click', onMouseClick, false);
window.addEventListener('mousemove', onMouseMove, false);

function onMouseMove(event) {
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(scene.children, true);

    let hoveringClickable = false;
    if (intersects.length > 0) {
        if (intersects[0].object.userData.isClickable) {
            hoveringClickable = true;
        }
    }
    document.body.style.cursor = hoveringClickable ? 'pointer' : 'default';
}

function onMouseClick(event) {
    // Calcular posición del mouse
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(scene.children, true);

    if (intersects.length > 0) {
        const clickedObj = intersects[0].object;
        
        // Si clickeamos el monitor
        if (clickedObj.userData.isClickable) {
            openComputer();
        }
    }
}

// Loop de animación
function animate() {
    requestAnimationFrame(animate);

    // Mover a Steve
    if (steveObject) {
        const isMoving = keys.w || keys.s;
        
        // 1. ROTACIÓN
        if (keys.a) steveObject.rotateY(rotSpeed); 
        if (keys.d) steveObject.rotateY(-rotSpeed);

        // 2. MOVIMIENTO (Dirección de la vista)
        // Usamos translateZ para movernos en el eje local de profundidad.
        // Probamos positivo para ir hacia "adelante" (donde mira la cara).
        if (keys.w) steveObject.translateZ(moveSpeed); 
        if (keys.s) steveObject.translateZ(-moveSpeed);

        // 3. GRAVEDAD: Mantener en el suelo
        steveObject.position.y = 0; 

        // Animación de caminar (swing)
        if (isMoving) {
            walkTime += 0.2;
            const swing = Math.sin(walkTime) * 0.5; 

            if (steveLimbs.legL) steveLimbs.legL.rotation.x = swing;
            if (steveLimbs.legR) steveLimbs.legR.rotation.x = -swing;
            if (steveLimbs.armL) steveLimbs.armL.rotation.x = -swing;
            if (steveLimbs.armR) steveLimbs.armR.rotation.x = swing;
        } else {
            if (steveLimbs.legL) steveLimbs.legL.rotation.x = 0;
            if (steveLimbs.legR) steveLimbs.legR.rotation.x = 0;
            if (steveLimbs.armL) steveLimbs.armL.rotation.x = 0;
            if (steveLimbs.armR) steveLimbs.armR.rotation.x = 0;
            walkTime = 0;
        }
    }

    controls.update();
    renderer.render(scene, camera);
}
animate();

// Ajustar al cambiar tamaño de ventana
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// Funciones globales para la UI
window.openComputer = function() {
    const screenDiv = document.getElementById('computer-screen');
    screenDiv.style.display = 'flex';
}

window.closeComputer = function() {
    document.getElementById('computer-screen').style.display = 'none';
}
