const ICON_PATHS = {
  dashboard: (
    <>
      <rect x="3" y="3" width="7.5" height="7.5" rx="1.6" />
      <rect x="13.5" y="3" width="7.5" height="7.5" rx="1.6" />
      <rect x="3" y="13.5" width="7.5" height="7.5" rx="1.6" />
      <rect x="13.5" y="13.5" width="7.5" height="7.5" rx="1.6" />
    </>
  ),
  forecast: (
    <>
      <path d="M3 17.5 8.5 12l3.5 3.5L21 6.5" />
      <path d="M15.5 6.5H21v5.5" />
      <path d="M3 21h18" />
    </>
  ),
  box: (
    <>
      <path d="M21 8.2 12 3.5 3 8.2v7.6L12 20.5l9-4.7V8.2Z" />
      <path d="M3 8.2 12 13l9-4.8" />
      <path d="M12 13v7.5" />
    </>
  ),
  inventory: (
    <>
      <path d="M8 20V4" />
      <path d="m4.5 7.5 3.5-3.5 3.5 3.5" />
      <path d="M16 4v16" />
      <path d="m12.5 16.5 3.5 3.5 3.5-3.5" />
    </>
  ),
  tag: (
    <>
      <path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L3 13V3h10l7.6 7.6a2 2 0 0 1 0 2.8Z" />
      <circle cx="7.5" cy="7.5" r="1.4" />
    </>
  ),
  truck: (
    <>
      <path d="M3 6.5h11v10H3z" />
      <path d="M14 10h3.6l3.4 3.4v3.1h-7z" />
      <circle cx="7" cy="18.5" r="1.8" />
      <circle cx="17.5" cy="18.5" r="1.8" />
    </>
  ),
  cart: (
    <>
      <path d="M3 4h2.2l2.3 10.2a1.8 1.8 0 0 0 1.8 1.4h7.4a1.8 1.8 0 0 0 1.8-1.4L21 7H6" />
      <circle cx="10" cy="20" r="1.4" />
      <circle cx="18" cy="20" r="1.4" />
    </>
  ),
  clipboard: (
    <>
      <path d="M9 4.5h6V7H9z" />
      <path d="M15 5.5h2.5A2 2 0 0 1 19.5 7.5v11A2 2 0 0 1 17.5 20.5h-11A2 2 0 0 1 4.5 18.5v-11A2 2 0 0 1 6.5 5.5H9" />
      <path d="M8.5 11h7" />
      <path d="M8.5 15h4.5" />
    </>
  ),
  search: (
    <>
      <circle cx="11" cy="11" r="6.5" />
      <path d="m16 16 4.5 4.5" />
    </>
  ),
  bell: (
    <>
      <path d="M18 8.5a6 6 0 1 0-12 0c0 6-2.5 7-2.5 8.5h17C20.5 15.5 18 14.5 18 8.5Z" />
      <path d="M10.2 20.5a2.1 2.1 0 0 0 3.6 0" />
    </>
  ),
  logout: (
    <>
      <path d="M9.5 20.5H6a2 2 0 0 1-2-2v-13a2 2 0 0 1 2-2h3.5" />
      <path d="m16 16.5 4.5-4.5L16 7.5" />
      <path d="M20.5 12H9.5" />
    </>
  ),
  refresh: (
    <>
      <path d="M20.5 12a8.5 8.5 0 1 1-2.5-6" />
      <path d="M20.5 3.5V9H15" />
    </>
  ),
  menu: (
    <>
      <path d="M4 7h16" />
      <path d="M4 12h16" />
      <path d="M4 17h16" />
    </>
  ),
  close: (
    <>
      <path d="m6 6 12 12" />
      <path d="m18 6-12 12" />
    </>
  ),
  spark: (
    <>
      <path d="m12 3 1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9L12 3Z" />
      <path d="M18.5 16.5 19.3 18.7 21.5 19.5 19.3 20.3 18.5 22.5 17.7 20.3 15.5 19.5 17.7 18.7Z" />
    </>
  ),
  alert: (
    <>
      <path d="M12 4 2.8 20h18.4L12 4Z" />
      <path d="M12 9.5v4.5" />
      <path d="M12 17.2h.01" />
    </>
  ),
  check: (
    <>
      <circle cx="12" cy="12" r="8.5" />
      <path d="m8.5 12.2 2.4 2.4 4.6-4.8" />
    </>
  ),
  clock: (
    <>
      <circle cx="12" cy="12" r="8.5" />
      <path d="M12 7.5V12l3 2" />
    </>
  ),
  users: (
    <>
      <circle cx="9" cy="8" r="3.2" />
      <path d="M3.5 20c0-3.2 2.5-5.2 5.5-5.2s5.5 2 5.5 5.2" />
      <path d="M16 5.2a3 3 0 0 1 0 5.6" />
      <path d="M17.5 14.6c2 .6 3.2 2.4 3.2 5.4" />
    </>
  ),
  chip: (
    <>
      <rect x="6.5" y="6.5" width="11" height="11" rx="2" />
      <rect x="10" y="10" width="4" height="4" rx="0.8" />
      <path d="M9.5 3v3.5M14.5 3v3.5M9.5 17.5V21M14.5 17.5V21M3 9.5h3.5M3 14.5h3.5M17.5 9.5H21M17.5 14.5H21" />
    </>
  ),
  cloud: (
    <>
      <path d="M7 18.5a4.2 4.2 0 0 1-.4-8.4 5.4 5.4 0 0 1 10.3-1.3A3.9 3.9 0 0 1 17 18.5Z" />
    </>
  ),
  plus: (
    <>
      <path d="M12 5v14" />
      <path d="M5 12h14" />
    </>
  ),
  arrowRight: (
    <>
      <path d="M4 12h15" />
      <path d="m13.5 6.5 5.5 5.5-5.5 5.5" />
    </>
  ),
  layers: (
    <>
      <path d="m12 3 9 4.5-9 4.5L3 7.5 12 3Z" />
      <path d="m3 12 9 4.5 9-4.5" />
      <path d="m3 16.5 9 4.5 9-4.5" />
    </>
  ),
  eye: (
    <>
      <path d="M2.5 12S6 5.8 12 5.8 21.5 12 21.5 12 18 18.2 12 18.2 2.5 12 2.5 12Z" />
      <circle cx="12" cy="12" r="3" />
    </>
  ),
  eyeOff: (
    <>
      <path d="M4 4.5 20 20.5" />
      <path d="M9.9 6.2A9.6 9.6 0 0 1 12 5.8c6 0 9.5 6.2 9.5 6.2a17 17 0 0 1-3 3.7" />
      <path d="M6.3 8.1A17.4 17.4 0 0 0 2.5 12s3.5 6.2 9.5 6.2a9.5 9.5 0 0 0 3.8-.8" />
      <path d="M9.9 9.9a3 3 0 0 0 4.2 4.2" />
    </>
  ),
};

export function Icon({ name, size = 18, className = '', title, strokeWidth = 1.6 }) {
  const paths = ICON_PATHS[name] ?? ICON_PATHS.spark;

  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={strokeWidth}
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
      role={title ? 'img' : undefined}
      aria-hidden={title ? undefined : true}
      aria-label={title}
      focusable="false"
    >
      {title ? <title>{title}</title> : null}
      {paths}
    </svg>
  );
}

export default Icon;
