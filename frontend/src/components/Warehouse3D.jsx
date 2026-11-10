import { useEffect, useRef } from 'react';

const TONE_HEX = {
  teal: 0x2dd4bf,
  amber: 0xf59e0b,
  red: 0xef4444,
  stone: 0x94a3b8,
};

function disposeScene(THREE, scene, renderer) {
  scene.traverse((object) => {
    if (object.geometry) object.geometry.dispose();

    const materials = object.material
      ? Array.isArray(object.material)
        ? object.material
        : [object.material]
      : [];

    materials.forEach((material) => {
      Object.values(material).forEach((value) => {
        if (value && value.isTexture) value.dispose();
      });
      material.dispose();
    });
  });

  renderer.dispose();
  renderer.forceContextLoss?.();
}

/**
 * Isometric 3D view of inventory crates. Each crate's height and colour reflect
 * a product's stock level and health, so the dashboard gets a live 3D snapshot.
 */
export default function Warehouse3D({ items = [], className = '' }) {
  const hostRef = useRef(null);
  const itemsRef = useRef(items);
  itemsRef.current = items;

  const signature = items
    .map((item) => `${item.id ?? item.label}:${item.value}:${item.tone}`)
    .join('|');

  useEffect(() => {
    const host = hostRef.current;
    if (!host) return undefined;

    let disposed = false;
    let cleanup = () => {};

    import('three')
      .then((THREE) => {
        if (disposed) return;

        let renderer;
        try {
          renderer = new THREE.WebGLRenderer({
            antialias: true,
            alpha: true,
            powerPreference: 'high-performance',
          });
        } catch {
          host.dataset.webgl = 'unsupported';
          return;
        }

        const reduceMotion =
          typeof window.matchMedia === 'function' &&
          window.matchMedia('(prefers-reduced-motion: reduce)').matches;

        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(38, 1, 0.1, 120);

        renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        renderer.domElement.style.width = '100%';
        renderer.domElement.style.height = '100%';
        renderer.domElement.style.display = 'block';
        renderer.domElement.style.outline = 'none';
        host.appendChild(renderer.domElement);

        scene.add(new THREE.HemisphereLight(0xc8f5ee, 0x0d1a19, 1.15));

        const keyLight = new THREE.DirectionalLight(0xffffff, 2.4);
        keyLight.position.set(7, 11, 7);
        keyLight.castShadow = true;
        keyLight.shadow.mapSize.set(1024, 1024);
        keyLight.shadow.camera.near = 1;
        keyLight.shadow.camera.far = 40;
        keyLight.shadow.camera.left = -10;
        keyLight.shadow.camera.right = 10;
        keyLight.shadow.camera.top = 10;
        keyLight.shadow.camera.bottom = -10;
        keyLight.shadow.bias = -0.0006;
        scene.add(keyLight);

        const rimLight = new THREE.DirectionalLight(0x2dd4bf, 1.4);
        rimLight.position.set(-8, 5, -7);
        scene.add(rimLight);

        const ground = new THREE.Mesh(
          new THREE.CircleGeometry(9, 72),
          new THREE.MeshStandardMaterial({
            color: 0x0c1717,
            roughness: 0.94,
            metalness: 0.06,
          }),
        );
        ground.rotation.x = -Math.PI / 2;
        ground.position.y = -0.03;
        ground.receiveShadow = true;
        scene.add(ground);

        const grid = new THREE.GridHelper(18, 36, 0x2dd4bf, 0x1e3b37);
        grid.position.y = 0.001;
        grid.material.transparent = true;
        grid.material.opacity = 0.18;
        scene.add(grid);

        const world = new THREE.Group();
        scene.add(world);

        const list = itemsRef.current.slice(0, 12);
        const placeholders = [
          { label: 'Empty', value: 3, tone: 'stone' },
          { label: 'Empty', value: 5, tone: 'stone' },
          { label: 'Empty', value: 2, tone: 'stone' },
          { label: 'Empty', value: 4, tone: 'stone' },
          { label: 'Empty', value: 6, tone: 'stone' },
          { label: 'Empty', value: 3, tone: 'stone' },
        ];
        const source = list.length > 0 ? list : placeholders;
        const values = source.map((item) => Math.max(Number(item.value) || 0, 0));
        const maxValue = Math.max(...values, 1);
        const cols = Math.max(Math.ceil(Math.sqrt(source.length)), 1);
        const rows = Math.ceil(source.length / cols);
        const spacing = 1.45;
        const crates = [];

        source.forEach((item, index) => {
          const column = index % cols;
          const row = Math.floor(index / cols);
          const height = 0.42 + (values[index] / maxValue) * 2.15;
          const color = TONE_HEX[item.tone] ?? TONE_HEX.stone;
          const isPlaceholder = list.length === 0;

          const crate = new THREE.Group();
          crate.position.set(
            (column - (cols - 1) / 2) * spacing,
            0,
            (row - (rows - 1) / 2) * spacing,
          );

          const geometry = new THREE.BoxGeometry(0.92, height, 0.92);
          const material = new THREE.MeshStandardMaterial({
            color,
            roughness: 0.32,
            metalness: 0.18,
            emissive: color,
            emissiveIntensity: isPlaceholder ? 0.04 : 0.16,
            transparent: isPlaceholder,
            opacity: isPlaceholder ? 0.45 : 1,
          });

          const mesh = new THREE.Mesh(geometry, material);
          mesh.position.y = height / 2;
          mesh.castShadow = true;
          mesh.receiveShadow = true;
          crate.add(mesh);

          const edges = new THREE.LineSegments(
            new THREE.EdgesGeometry(geometry),
            new THREE.LineBasicMaterial({
              color: 0xe7fffb,
              transparent: true,
              opacity: 0.22,
            }),
          );
          edges.position.copy(mesh.position);
          crate.add(edges);

          const pallet = new THREE.Mesh(
            new THREE.BoxGeometry(1.04, 0.09, 1.04),
            new THREE.MeshStandardMaterial({
              color: 0x1c2b29,
              roughness: 0.85,
              metalness: 0.05,
            }),
          );
          pallet.position.y = 0.045;
          pallet.castShadow = true;
          pallet.receiveShadow = true;
          crate.add(pallet);

          crate.userData.phase = index * 0.8;
          world.add(crate);
          crates.push(crate);
        });

        const frameDistance = 5.6 + Math.max(cols, rows) * 0.72;
        const baseCamera = new THREE.Vector3(
          frameDistance * 0.72,
          frameDistance * 0.58,
          frameDistance * 0.86,
        );
        const lookAt = new THREE.Vector3(0, 1.0, 0);
        camera.position.copy(baseCamera);
        camera.lookAt(lookAt);

        const pointer = { x: 0, y: 0 };
        const parallax = { x: 0, y: 0 };

        function handlePointerMove(event) {
          const bounds = host.getBoundingClientRect();
          if (!bounds.width || !bounds.height) return;
          pointer.x = ((event.clientX - bounds.left) / bounds.width) * 2 - 1;
          pointer.y = ((event.clientY - bounds.top) / bounds.height) * 2 - 1;
        }

        function handlePointerLeave() {
          pointer.x = 0;
          pointer.y = 0;
        }

        host.addEventListener('pointermove', handlePointerMove);
        host.addEventListener('pointerleave', handlePointerLeave);

        const resize = () => {
          const width = host.clientWidth;
          const height = host.clientHeight;
          if (!width || !height) return;
          renderer.setSize(width, height, false);
          camera.aspect = width / height;
          camera.updateProjectionMatrix();
        };

        const observer = new ResizeObserver(resize);
        observer.observe(host);
        resize();

        const clock = new THREE.Clock();
        let frameId = 0;

        const animate = () => {
          frameId = requestAnimationFrame(animate);
          const elapsed = clock.getElapsedTime();

          if (!reduceMotion) {
            world.rotation.y = 0.3 + Math.sin(elapsed * 0.22) * 0.14;

            crates.forEach((crate) => {
              crate.position.y = Math.sin(elapsed * 0.85 + crate.userData.phase) * 0.035;
            });

            parallax.x += (pointer.x * 0.55 - parallax.x) * 0.045;
            parallax.y += (pointer.y * 0.35 - parallax.y) * 0.045;
            camera.position.x = baseCamera.x + parallax.x;
            camera.position.y = baseCamera.y - parallax.y;
            camera.lookAt(lookAt);
          }

          renderer.render(scene, camera);
        };

        animate();

        cleanup = () => {
          cancelAnimationFrame(frameId);
          observer.disconnect();
          host.removeEventListener('pointermove', handlePointerMove);
          host.removeEventListener('pointerleave', handlePointerLeave);
          disposeScene(THREE, scene, renderer);
          if (renderer.domElement.parentNode === host) {
            host.removeChild(renderer.domElement);
          }
        };
      })
      .catch(() => {
        if (host) host.dataset.webgl = 'unsupported';
      });

    return () => {
      disposed = true;
      cleanup();
    };
  }, [signature]);

  return (
    <div
      ref={hostRef}
      className={`relative h-full w-full ${className}`}
      role="img"
      aria-label="3D inventory view: each crate height and colour reflects current stock level and health."
      data-webgl="pending"
    />
  );
}
