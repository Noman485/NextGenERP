function safeNumber(value) {
  const number = Number(value);
  return Number.isFinite(number) ? number : 0;
}

function compactNumber(value) {
  return new Intl.NumberFormat('en-IN', {
    notation: 'compact',
    maximumFractionDigits: 1,
  }).format(safeNumber(value));
}

function tickLabels(data, xKey, count = 6) {
  if (!data.length) return [];
  const step = Math.max(1, Math.ceil(data.length / count));
  return data
    .map((item, index) => ({ item, index }))
    .filter(({ index }) => index % step === 0 || index === data.length - 1);
}

export function LineChart({
  data = [],
  xKey = 'date',
  yKey = 'revenue',
  label,
  formatValue = compactNumber,
  formatX = (value) => value,
  height = 240,
}) {
  const width = 640;
  const padding = { top: 20, right: 16, bottom: 34, left: 52 };
  const innerWidth = width - padding.left - padding.right;
  const innerHeight = height - padding.top - padding.bottom;
  const values = data.map((item) => safeNumber(item[yKey]));
  const maxValue = Math.max(1, ...values);
  const xFor = (index) =>
    data.length <= 1
      ? padding.left + innerWidth / 2
      : padding.left + (index / (data.length - 1)) * innerWidth;
  const yFor = (value) =>
    padding.top + innerHeight - (safeNumber(value) / maxValue) * innerHeight;

  const points = data.map((item, index) => ({
    x: xFor(index),
    y: yFor(item[yKey]),
    item,
  }));
  const linePath = points
    .map((point, index) => `${index === 0 ? 'M' : 'L'} ${point.x.toFixed(2)} ${point.y.toFixed(2)}`)
    .join(' ');
  const areaPath = points.length
    ? `${linePath} L ${points[points.length - 1].x.toFixed(2)} ${(padding.top + innerHeight).toFixed(2)} L ${points[0].x.toFixed(2)} ${(padding.top + innerHeight).toFixed(2)} Z`
    : '';
  const ticks = [0, 0.25, 0.5, 0.75, 1];

  return (
    <figure className="rounded-xl border border-stone-200 bg-white p-4">
      <svg
        viewBox={`0 0 ${width} ${height}`}
        role="img"
        aria-label={label}
        className="h-auto w-full"
      >
        <title>{label}</title>
        {ticks.map((tick) => {
          const y = padding.top + innerHeight - tick * innerHeight;
          return (
            <g key={tick}>
              <line
                x1={padding.left}
                x2={width - padding.right}
                y1={y}
                y2={y}
                stroke="#e7e5e4"
                strokeWidth="1"
              />
              <text
                x={padding.left - 8}
                y={y + 4}
                textAnchor="end"
                className="fill-stone-400 text-[9px]"
              >
                {formatValue(maxValue * tick)}
              </text>
            </g>
          );
        })}
        {areaPath && <path d={areaPath} fill="rgba(13,148,136,0.08)" />}
        {linePath && (
          <path
            d={linePath}
            fill="none"
            stroke="#0f766e"
            strokeWidth="2.5"
            strokeLinejoin="round"
            strokeLinecap="round"
          />
        )}
        {points.map((point) => (
          <circle
            key={`${point.item[xKey]}-${point.y}`}
            cx={point.x}
            cy={point.y}
            r="2.5"
            fill="#0f766e"
          >
            <title>
              {`${formatX(point.item[xKey])}: ${formatValue(point.item[yKey])}`}
            </title>
          </circle>
        ))}
        {tickLabels(data, xKey).map(({ item, index }) => (
          <text
            key={`${item[xKey]}-${index}`}
            x={xFor(index)}
            y={height - 10}
            textAnchor="middle"
            className="fill-stone-400 text-[9px]"
          >
            {formatX(item[xKey])}
          </text>
        ))}
      </svg>
      <figcaption className="sr-only">
        {label}. {data.length} data points. Maximum {formatValue(maxValue)}.
      </figcaption>
    </figure>
  );
}

export function BarChart({
  data = [],
  xKey = 'label',
  yKey = 'revenue',
  label,
  formatValue = compactNumber,
  formatX = (value) => value,
  height = 240,
  color = '#0f766e',
  colorMap = null,
  colorKey = 'label',
}) {
  const width = 640;
  const padding = { top: 20, right: 16, bottom: 38, left: 52 };
  const innerWidth = width - padding.left - padding.right;
  const innerHeight = height - padding.top - padding.bottom;
  const values = data.map((item) => safeNumber(item[yKey]));
  const maxValue = Math.max(1, ...values);
  const slot = data.length ? innerWidth / data.length : innerWidth;
  const barWidth = Math.max(4, Math.min(38, slot * 0.62));
  const ticks = [0, 0.25, 0.5, 0.75, 1];

  return (
    <figure className="rounded-xl border border-stone-200 bg-white p-4">
      <svg
        viewBox={`0 0 ${width} ${height}`}
        role="img"
        aria-label={label}
        className="h-auto w-full"
      >
        <title>{label}</title>
        {ticks.map((tick) => {
          const y = padding.top + innerHeight - tick * innerHeight;
          return (
            <g key={tick}>
              <line
                x1={padding.left}
                x2={width - padding.right}
                y1={y}
                y2={y}
                stroke="#e7e5e4"
                strokeWidth="1"
              />
              <text
                x={padding.left - 8}
                y={y + 4}
                textAnchor="end"
                className="fill-stone-400 text-[9px]"
              >
                {formatValue(maxValue * tick)}
              </text>
            </g>
          );
        })}
        {data.map((item, index) => {
          const value = safeNumber(item[yKey]);
          const barHeight = (value / maxValue) * innerHeight;
          const x = padding.left + index * slot + (slot - barWidth) / 2;
          const y = padding.top + innerHeight - barHeight;
          // Resolve the colour from the datum's real status value, never from
          // its position in the array. Unknown categories keep the default.
          const fill = colorMap?.[item[colorKey]] ?? color;
          return (
            <g key={`${item[xKey]}-${index}`}>
              <rect
                x={x}
                y={y}
                width={barWidth}
                height={Math.max(0, barHeight)}
                rx="3"
                fill={fill}
                opacity={value === 0 ? 0.2 : 0.9}
              >
                <title>{`${formatX(item[xKey])}: ${formatValue(value)}`}</title>
              </rect>
              <text
                x={x + barWidth / 2}
                y={height - 12}
                textAnchor="middle"
                className="fill-stone-400 text-[9px]"
              >
                {formatX(item[xKey])}
              </text>
            </g>
          );
        })}
      </svg>
      <figcaption className="sr-only">
        {label}. {data.length} categories. Maximum {formatValue(maxValue)}.
      </figcaption>
    </figure>
  );
}
