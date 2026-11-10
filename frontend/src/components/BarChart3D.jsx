import { useEffect, useRef, useState } from 'react';

const BAR_COLORS = [0x2dd4bf, 0x34d3c2, 0x3cc9c6, 0x45bfca, 0x4db5cd, 0x55aacf, 0x5d9fd0];

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

function formatValue(value) {
  const number = Number(value);
  if (!Number.isFinite(number)) return '—';
  return Math.round(number).toLocaleString('en-IN');
}

/**
 * 3D bar chart for the demand forecast. Bars are hoverable; the hovered day's
 * label and predicted units are shown in the corner panel.
 */
export default function BarChart3D({ data = [], className = '' }) {
  const hostRef = useRef(null);
  const dataRef = useRef(data);
  dataRef.current = data;

  const [activeIndex, setActiveIndex] = useState(null);

  const signature = data.map((entry) => `${entry.label}:${entry.value}`).join('|');

  useEffect(() => {
    const host = hostRef.current;
    if (!host) return undefined;

    let disposed = false;
    let cleanup = () => {};

    setActiveIndex(null);

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
        const camera = new THREE.PerspectiveCamera(34, 1, 0.1, 120);

        renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        renderer.domElement.style.width = '100%';
        renderer.domElement.style.height = '100%';
        renderer.domElement.style.display = 'block';
        renderer.domElement.style.outline = 'none';
        host.appendChild(renderer.domElement);

        scene.add(new THREE.HemisphereLight(0xc8f5ee, 0x0a1615, 1.2));

        const keyLight = new THREE.DirectionalLight(0xffffff, 2.3);
        keyLight.position.set(6, 10, 7);
        keyLight.castShadow = true;
        keyLight.shadow.mapSize.set(1024, 1024);
        keyLight.shadow.camera.near = 1;
        keyLight.shadow.camera.far = 40;
        keyLight.shadow.camera.left = -9;
        keyLight.shadow.camera.right = 9;
        keyLight.shadow.camera.top = 9;
        keyLight.shadow.camera.bottom = -9;
        keyLight.shadow.bias = -0.0006;
        scene.add(keyLight);

        const rimLight = new THREE.DirectionalLight(0x22d3ee, 1.2);
        rimLight.position.set(-7, 5, -6);
        scene.add(rimLight);

        const world = new THREE.Group();
        scene.add(world);

        const platform = new THREE.Mesh(
          new THREE.BoxGeometry(9.4, 0.16, 3.1),
          new THREE.MeshStandardMaterial({
            color: 0x10201f,
            roughness: 0.9,
            metalness: 0.1,
          }),
        );
        platform.position.y = -0.08;
        platform.receiveShadow = true;
        world.add(platform);

        const platformEdge = new THREE.LineSegments(
          new THREE.EdgesGeometry(platform.geometry),
          new THREE.LineBasicMaterial({ color: 0x2dd4bf, transparent: true, opacity: 0.28 }),
        );
        platformEdge.position.copy(platform.position);
        world.add(platformEdge);

        const list = dataRef.current.slice(0, 7);
        const values = list.map((entry) => Math.max(Number(entry.value) || 0, 0));
        const maxValue = Math.max(...values, 1);
        const count = Math.max(list.length, 1);
        const spacing = 1.14;
        const bars = [];
        const materials = [];

        list.forEach((entry, index) => {
          const height = 0.28 + (values[index] / maxValue) * 2.7;
          const color = BAR_COLORS[index % BAR_COLORS.length];
          const geometry = new THREE.BoxGeometry(0.62, height, 0.62);
          const material = new THREE.MeshStandardMaterial({
            color,
            roughness: 0.28,
            metalness: 0.24,
            emissive: color,
            emissiveIntensity: 0.18,
          });

          const bar = new THREE.Mesh(geometry, material);
          bar.position.set((index - (count - 1) / 2) * spacing, height / 2 + 0.02, 0);
          bar.castShadow = true;
          bar.receiveShadow = true;
          bar.userData.index = index;
          world.add(bar);

          const cap = new THREE.Mesh(
            new THREE.BoxGeometry(0.68, 0.06, 0.68),
            new THREE.MeshStandardMaterial({
              color: 0xe6fffb,
              roughness: 0.4,
              metalness: 0.1,
              emissive: 0x2dd4bf,
              emissiveIntensity: 0.35,
            }),
          );
          cap.position.set(bar.position.x, height + 0.05, 0);
          world.add(cap);

          bars.push(bar);
          materials.push(material);
        });

        camera.position.set(4.6, 4.3, 7.6);
        const lookAt = new THREE.Vector3(0, 0.95, 0);
        camera.lookAt(lookAt);

        const raycaster = new THREE.Raycaster();
        const pointer = new THREE.Vector2(-10, -10);
        let hovered = null;
        let pointerInside = false;

        function handlePointerMove(event) {
          const bounds = host.getBoundingClientRect();
          if (!bounds.width || !bounds.height) return;
          pointer.x = ((event.clientX - bounds.left) / bounds.width) * 2 - 1;
          pointer.y = -((event.clientY - bounds.top) / bounds.height) * 2 + 1;
          pointerInside = true;
        }

        function handlePointerLeave() {
          pointerInside = false;
          pointer.x = -10;
          pointer.y = -10;
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
            world.rotation.y = Math.sin(elapsed * 0.26) * 0.12;
          }

          let nextHovered = null;
          if (pointerInside) {
            raycaster.setFromCamera(pointer, camera);
            const hits = raycaster.intersectObjects(bars, false);
            if (hits.length > 0) nextHovered = hits[0].object.userData.index;
          }

          if (nextHovered !== hovered) {
            hovered = nextHovered;
            materials.forEach((material, index) => {
              material.emissiveIntensity = index === hovered ? 0.75 : 0.18;
            });
            setActiveIndex(hovered);
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

  const total = data.reduce((sum, entry) => sum + (Number(entry.value) || 0), 0);
  const active = activeIndex != null ? data[activeIndex] : null;

  return (
    <div className={`relative ${className}`}>
      <div
        ref={hostRef}
        className="h-full w-full"
        role="img"
        aria-label={`3D forecast chart: ${data
          .map((entry) => `${entry.label} ${formatValue(entry.value)} units`)
          .join(', ')}`}
        data-webgl="pending"
      />

      <div className="pointer-events-none absolute right-0 top-0 rounded-xl border border-white/10 bg-black/30 px-3 py-2 text-right backdrop-blur-sm">
        <p className="text-[9px] font-semibold uppercase tracking-[0.22em] text-teal-200/70">
          {active ? active.label : 'Horizon total'}
        </p>
        <p className="mt-0.5 text-lg font-semibold leading-none text-white tabular-nums">
          {formatValue(active ? active.value : total)}
        </p>
        <p className="mt-1 text-[10px] text-white/45">
          {active ? 'predicted units' : 'units · 7 days'}
        </p>
      </div>

      <div className="pointer-events-none absolute inset-x-0 bottom-0 flex justify-center gap-1.5 px-2">
        {data.map((entry) => (
          <span
            key={entry.label}
            className="flex-1 truncate text-center text-[9px] uppercase tracking-[0.12em] text-white/40"
          >
            {entry.short ?? entry.label}
          </span>
        ))}
      </div>
    </div>
  );
}
