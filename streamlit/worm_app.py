import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="3D Worm", layout="wide", page_icon="🐛")

st.markdown("""
<style>
body { background: #060612; }
.block-container { padding: 1rem 1rem 0 1rem; }
h1 { color: #7fff9a; font-family: monospace; letter-spacing: 4px; }
p  { color: #445; font-family: monospace; }
</style>
""", unsafe_allow_html=True)

st.title("⬡ 3D WORM")
st.markdown("Move your mouse — the worm crawls toward it in full 3D with giant scuttling legs.")

components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body {
  background: #060612;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
}
canvas { display:block; cursor:none; }
#label {
  position:absolute;
  bottom:10px; left:50%;
  transform:translateX(-50%);
  color:#1a3a2a;
  font:11px monospace;
  letter-spacing:3px;
  pointer-events:none;
}
</style>
</head>
<body>
<div id="label">MOVE MOUSE · WORM FOLLOWS</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
// ════════════════════════════════════════
//   SCENE SETUP
// ════════════════════════════════════════
const W = window.innerWidth, H = window.innerHeight;
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setSize(W, H);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.setPixelRatio(window.devicePixelRatio);
document.body.appendChild(renderer.domElement);

const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(0x060612, 0.018);

const camera = new THREE.PerspectiveCamera(55, W / H, 0.1, 500);
camera.position.set(0, 38, 62);
camera.lookAt(0, 0, 0);

// ── LIGHTS ──────────────────────────────
const ambient = new THREE.AmbientLight(0x112233, 0.7);
scene.add(ambient);

const sun = new THREE.DirectionalLight(0x88ffcc, 1.4);
sun.position.set(30, 60, 20);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
scene.add(sun);

const rimLight = new THREE.PointLight(0xff6633, 1.8, 120);
rimLight.position.set(-40, 20, -20);
scene.add(rimLight);

const headLight = new THREE.PointLight(0x00ffaa, 2.5, 40);
scene.add(headLight); // will follow head

// ── GROUND ──────────────────────────────
const groundGeo = new THREE.PlaneGeometry(300, 300, 60, 60);
const groundMat = new THREE.MeshStandardMaterial({
  color: 0x0a1a12,
  roughness: 0.95,
  metalness: 0.0,
  wireframe: false
});
// add subtle vertex displacement for organic ground feel
const pos = groundGeo.attributes.position;
for (let i = 0; i < pos.count; i++) {
  pos.setZ(i, (Math.random() - 0.5) * 0.6);
}
groundGeo.computeVertexNormals();
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.position.y = -8;
ground.receiveShadow = true;
scene.add(ground);

// grid on ground
const gridHelper = new THREE.GridHelper(200, 50, 0x0d2d1a, 0x0d2d1a);
gridHelper.position.y = -7.95;
scene.add(gridHelper);

// ════════════════════════════════════════
//   WORM CONFIG
// ════════════════════════════════════════
const SEGS     = 20;        // body segments
const SEG_DIST = 4.2;       // distance between segments
const BODY_R   = [2.1,2.0,1.95,1.9,1.85,1.82,1.78,1.75,1.7,1.65,
                  1.6, 1.55,1.5, 1.45,1.4, 1.35,1.3, 1.2, 1.1, 0.9];
const LEG_PAIRS = 3;        // leg pairs per segment
const LEG_LEN   = 5.5;      // leg length (bigger than body)
const LEG_THICK = 0.45;

// ── MATERIALS ────────────────────────────
const bodyMat = new THREE.MeshStandardMaterial({
  color: 0x22cc77,
  roughness: 0.35,
  metalness: 0.15,
  emissive: 0x003311,
  emissiveIntensity: 0.4,
});
const legMat = new THREE.MeshStandardMaterial({
  color: 0x44ff99,
  roughness: 0.4,
  metalness: 0.2,
  emissive: 0x002208,
  emissiveIntensity: 0.3,
});
const jointMat = new THREE.MeshStandardMaterial({
  color: 0xffaa33,
  roughness: 0.3,
  metalness: 0.5,
  emissive: 0x331100,
  emissiveIntensity: 0.5,
});
const eyeMat = new THREE.MeshStandardMaterial({
  color: 0xffffff,
  emissive: 0xffffff,
  emissiveIntensity: 1.0,
  roughness: 0.1,
});
const pupilMat = new THREE.MeshStandardMaterial({
  color: 0x000000,
  roughness: 0.2,
});

// ── BUILD SEGMENT MESH ───────────────────
function makeSegment(i) {
  const r = BODY_R[i];
  const geo = new THREE.SphereGeometry(r, 14, 10);
  const mesh = new THREE.Mesh(geo, bodyMat.clone());
  mesh.castShadow = true;
  mesh.receiveShadow = true;

  // per-segment color shift (head bright, tail duller)
  const t = i / SEGS;
  mesh.material.color.setHSL(0.38 - t * 0.12, 0.85, 0.5 - t * 0.15);
  mesh.material.emissive.setHSL(0.38 - t * 0.12, 1.0, 0.07);
  return mesh;
}

// ── BUILD LEG ────────────────────────────
function makeLeg() {
  const group = new THREE.Group();

  // upper limb
  const upperGeo = new THREE.CylinderGeometry(LEG_THICK, LEG_THICK * 0.7, LEG_LEN * 0.55, 8);
  const upper    = new THREE.Mesh(upperGeo, legMat.clone());
  upper.position.y = -LEG_LEN * 0.275;
  group.add(upper);

  // knee joint sphere
  const kneeGeo = new THREE.SphereGeometry(LEG_THICK * 1.5, 8, 8);
  const knee    = new THREE.Mesh(kneeGeo, jointMat.clone());
  knee.position.y = -LEG_LEN * 0.55;
  group.add(knee);

  // lower limb
  const lowerGeo = new THREE.CylinderGeometry(LEG_THICK * 0.7, LEG_THICK * 0.4, LEG_LEN * 0.55, 8);
  const lower    = new THREE.Mesh(lowerGeo, legMat.clone());
  lower.position.y = -LEG_LEN * 0.55 - LEG_LEN * 0.275;
  group.add(lower);

  // foot sphere
  const footGeo = new THREE.SphereGeometry(LEG_THICK * 1.1, 8, 8);
  const foot    = new THREE.Mesh(footGeo, jointMat.clone());
  foot.position.y = -LEG_LEN * 1.1;
  group.add(foot);

  group.traverse(m => { if (m.isMesh) { m.castShadow = true; } });
  return group;
}

// ── WORM BODY ────────────────────────────
const segments  = [];
const legGroups = []; // legGroups[i] = array of leg group objects for segment i
const wormRoot  = new THREE.Group();
scene.add(wormRoot);

// body positions (world space, flat snake-chain)
const segPos = [];
for (let i = 0; i < SEGS; i++) {
  segPos.push(new THREE.Vector3(-i * SEG_DIST, 0, 0));
}

for (let i = 0; i < SEGS; i++) {
  const mesh = makeSegment(i);
  wormRoot.add(mesh);
  segments.push(mesh);

  const legsForSeg = [];
  // 3 leg pairs per segment (left + right per pair = 6 legs per segment)
  for (let p = 0; p < LEG_PAIRS; p++) {
    for (const side of [-1, 1]) {
      const lg = makeLeg();
      wormRoot.add(lg);
      legsForSeg.push({ group: lg, side, pairIdx: p });
    }
  }
  legGroups.push(legsForSeg);
}

// ── HEAD FEATURES (eyes + antenna) ───────
const headGroup = new THREE.Group();
wormRoot.add(headGroup);

for (const side of [-1, 1]) {
  const eyeGeo = new THREE.SphereGeometry(0.55, 10, 10);
  const eye    = new THREE.Mesh(eyeGeo, eyeMat);
  eye.position.set(side * 1.1, 1.0, 1.6);
  headGroup.add(eye);

  const pupilGeo = new THREE.SphereGeometry(0.28, 8, 8);
  const pupil    = new THREE.Mesh(pupilGeo, pupilMat);
  pupil.position.set(side * 1.1, 1.0, 2.1);
  headGroup.add(pupil);

  // antenna
  const antGeo  = new THREE.CylinderGeometry(0.1, 0.05, 3.5, 6);
  const ant     = new THREE.Mesh(antGeo, legMat);
  ant.position.set(side * 0.9, 2.5, 1.2);
  ant.rotation.z = side * 0.4;
  ant.rotation.x = -0.5;
  headGroup.add(ant);

  const antBallGeo = new THREE.SphereGeometry(0.3, 8, 8);
  const antBall    = new THREE.Mesh(antBallGeo, jointMat);
  antBall.position.set(
    side * (0.9 + Math.sin(0.4) * 1.75),
    2.5 + 1.75 * Math.cos(0.4),
    1.2 - Math.sin(0.5) * 1.75
  );
  headGroup.add(antBall);
}

// ════════════════════════════════════════
//   MOUSE → WORLD PROJECTION
// ════════════════════════════════════════
const mouse3D = new THREE.Vector3(0, 0, 0);
const raycaster = new THREE.Raycaster();
const mousePlane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0); // y=0 plane
const mouseNDC = new THREE.Vector2();

window.addEventListener('mousemove', e => {
  mouseNDC.x =  (e.clientX / W) * 2 - 1;
  mouseNDC.y = -(e.clientY / H) * 2 + 1;
  raycaster.setFromCamera(mouseNDC, camera);
  const hit = new THREE.Vector3();
  raycaster.ray.intersectPlane(mousePlane, hit);
  if (hit) {
    mouse3D.x = hit.x;
    mouse3D.z = hit.z;
    mouse3D.y = 0;
  }
});

// ════════════════════════════════════════
//   ANIMATION STATE
// ════════════════════════════════════════
let time = 0;
const segVel = segPos.map(() => new THREE.Vector3());

// ── UPDATE CHAIN ─────────────────────────
function updateChain() {
  // head moves toward mouse
  const head = segPos[0];
  const toMouse = new THREE.Vector3().subVectors(mouse3D, head);
  const d = toMouse.length();
  if (d > 1) {
    const speed = Math.min(d * 0.08, 4.5);
    head.addScaledVector(toMouse.normalize(), speed);
  }
  head.y = 0;

  // each segment follows previous (inverse kinematics chain)
  for (let i = 1; i < SEGS; i++) {
    const prev = segPos[i - 1];
    const curr = segPos[i];
    const diff = new THREE.Vector3().subVectors(curr, prev);
    const dist = diff.length();
    if (dist > SEG_DIST) {
      diff.multiplyScalar(SEG_DIST / dist);
      curr.copy(prev).add(diff);
    }
    curr.y = 0;
  }
}

// ── UPDATE LEGS ──────────────────────────
function updateLegs() {
  for (let i = 0; i < SEGS; i++) {
    const mesh = segments[i];
    const pos  = segPos[i];
    const r    = BODY_R[i];

    // direction of movement (forward = toward previous segment)
    let forwardDir = new THREE.Vector3(1, 0, 0);
    if (i > 0) {
      forwardDir.subVectors(segPos[i - 1], pos).normalize();
    }

    const legList = legGroups[i];
    for (const legData of legList) {
      const { group, side, pairIdx } = legData;

      // spread legs outward perpendicular to body direction
      const perp = new THREE.Vector3(-forwardDir.z, 0, forwardDir.x);

      // offset along body for each pair
      const pairOffset = (pairIdx - (LEG_PAIRS - 1) / 2) * (r * 1.1);

      // leg root position (on body surface)
      const rootX = pos.x + perp.x * r * side + forwardDir.x * pairOffset;
      const rootZ = pos.z + perp.z * r * side + forwardDir.z * pairOffset;
      const rootY = pos.y + r * 0.3;

      group.position.set(rootX, rootY, rootZ);

      // splay outward
      const splayAngle = side * (Math.PI * 0.38);

      // wave animation — offset by segment and pair
      const phase = time * 2.2 + i * 0.45 + pairIdx * 0.7 + (side > 0 ? Math.PI : 0);
      const wave  = Math.sin(phase) * 0.6;

      // tilt the leg outward and wave it
      group.rotation.set(wave * 0.5, 0, splayAngle + wave * 0.35);

      // rotate so leg faces outward
      const bodyAngle = Math.atan2(forwardDir.z, forwardDir.x);
      group.rotation.y = bodyAngle - Math.PI / 2;
    }
  }
}

// ── APPLY TO MESHES ──────────────────────
function applyToMeshes() {
  for (let i = 0; i < SEGS; i++) {
    const mesh = segments[i];
    const pos  = segPos[i];

    // position
    mesh.position.copy(pos);
    mesh.position.y = BODY_R[i] * 0.5; // sit on ground

    // orient toward previous segment
    if (i > 0) {
      const dir = new THREE.Vector3().subVectors(segPos[i - 1], pos);
      if (dir.length() > 0.01) {
        const target = new THREE.Vector3().addVectors(pos, dir);
        mesh.lookAt(target);
      }
    }

    // breathing / squish
    const squish = 1 + Math.sin(time * 3 + i * 0.5) * 0.04;
    mesh.scale.set(squish, 1 / squish, squish);
  }

  // head group follows segment 0
  headGroup.position.copy(segments[0].position);
  if (SEGS > 1) {
    const dir = new THREE.Vector3().subVectors(segPos[0], segPos[1]);
    if (dir.length() > 0.01) {
      const target = new THREE.Vector3().addVectors(segPos[0], dir);
      const dummy  = new THREE.Object3D();
      dummy.position.copy(segPos[0]);
      dummy.lookAt(target);
      headGroup.quaternion.copy(dummy.quaternion);
    }
  }

  // headlight follows head
  headLight.position.copy(segments[0].position);
  headLight.position.y += 4;
}

// ── SHADOW BLOBS under segments ──────────
const shadowBlobs = [];
for (let i = 0; i < SEGS; i++) {
  const geo  = new THREE.CircleGeometry(BODY_R[i] * 1.1, 12);
  const mat  = new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: 0.25 });
  const blob = new THREE.Mesh(geo, mat);
  blob.rotation.x = -Math.PI / 2;
  blob.position.y = -7.9;
  scene.add(blob);
  shadowBlobs.push(blob);
}

// ── CURSOR INDICATOR ─────────────────────
const cursorGeo  = new THREE.RingGeometry(0.6, 0.9, 16);
const cursorMat  = new THREE.MeshBasicMaterial({ color: 0x00ff99, side: THREE.DoubleSide, transparent: true, opacity: 0.7 });
const cursorMesh = new THREE.Mesh(cursorGeo, cursorMat);
cursorMesh.rotation.x = -Math.PI / 2;
cursorMesh.position.y = -7.85;
scene.add(cursorMesh);

// ════════════════════════════════════════
//   RENDER LOOP
// ════════════════════════════════════════
function animate() {
  requestAnimationFrame(animate);
  time += 0.016;

  updateChain();
  updateLegs();
  applyToMeshes();

  // shadow blobs
  for (let i = 0; i < SEGS; i++) {
    shadowBlobs[i].position.x = segPos[i].x;
    shadowBlobs[i].position.z = segPos[i].z;
    const heightAbove = segments[i].position.y + 7.9;
    shadowBlobs[i].material.opacity = Math.max(0, 0.28 - heightAbove * 0.01);
  }

  // cursor ring
  cursorMesh.position.x = mouse3D.x;
  cursorMesh.position.z = mouse3D.z;
  cursorMesh.rotation.z = time * 1.5;

  // rim light orbit
  rimLight.position.x = Math.cos(time * 0.3) * 50;
  rimLight.position.z = Math.sin(time * 0.3) * 50;

  renderer.render(scene, camera);
}

animate();

// resize
window.addEventListener('resize', () => {
  const w = window.innerWidth, h = window.innerHeight;
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
  renderer.setSize(w, h);
});
</script>
</body>
</html>
""", height=650, scrolling=False)

st.markdown("""
<p style='color:#1a3a2a;font-family:monospace;font-size:11px;text-align:center;margin-top:6px'>
3D ENGINE: Three.js r128 · WORM SEGMENTS: 20 · LEGS PER SEGMENT: 6 · IK CHAIN · REAL-TIME SHADOWS
</p>
""", unsafe_allow_html=True)