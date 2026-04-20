// ── Map ──
const instanceColors = ['#40d8c0', '#a78bfa', '#d4a030', '#e05050', '#3ddc84', '#8aa8d8'];

function svgOxynoeBackground(svgEl) {
  const ns = 'http://www.w3.org/2000/svg';
  const defs = document.createElementNS(ns, 'defs');
  const grad = document.createElementNS(ns, 'radialGradient');
  grad.setAttribute('id', 'svgBg-' + svgEl.id); grad.setAttribute('cx', '50%'); grad.setAttribute('cy', '40%'); grad.setAttribute('r', '70%');
  const s1 = document.createElementNS(ns, 'stop'); s1.setAttribute('offset', '0%'); s1.setAttribute('stop-color', '#0a4858');
  const s2 = document.createElementNS(ns, 'stop'); s2.setAttribute('offset', '100%'); s2.setAttribute('stop-color', '#041c24');
  grad.appendChild(s1); grad.appendChild(s2); defs.appendChild(grad); svgEl.appendChild(defs);
  const rect = document.createElementNS(ns, 'rect');
  rect.setAttribute('width', '100%'); rect.setAttribute('height', '100%');
  rect.setAttribute('fill', `url(#svgBg-${svgEl.id})`); rect.setAttribute('rx', '6');
  svgEl.appendChild(rect);
  // Subtle grid
  const grid = document.createElementNS(ns, 'g'); grid.setAttribute('stroke', 'rgba(0,200,220,0.04)'); grid.setAttribute('stroke-width', '0.5');
  const vb = svgEl.getAttribute('viewBox')?.split(' ') || [0,0,800,500];
  const w = parseInt(vb[2]) || 800, h = parseInt(vb[3]) || 500;
  for (let y = 0; y < h; y += 40) { const l = document.createElementNS(ns, 'line'); l.setAttribute('x1',0); l.setAttribute('x2',w); l.setAttribute('y1',y); l.setAttribute('y2',y); grid.appendChild(l); }
  for (let x = 0; x < w; x += 40) { const l = document.createElementNS(ns, 'line'); l.setAttribute('x1',x); l.setAttribute('x2',x); l.setAttribute('y1',0); l.setAttribute('y2',h); grid.appendChild(l); }
  svgEl.appendChild(grid);
}

function renderMap() {
  // Map uses MIRROR_DATA — aggregated view across all instances
  if (!MIRROR_DATA) return;

  // Use 'all' aggregation if available, else build from per-instance
  let mapData, allRecords;
  if (MIRROR_DATA.all && MIRROR_DATA.all.map && MIRROR_DATA.all.map.instances) {
    mapData = MIRROR_DATA.all.map.instances;
    allRecords = MIRROR_DATA.all.friction_records || [];
  } else {
    mapData = {};
    allRecords = [];
    for (const [instName, instData] of Object.entries(MIRROR_DATA.instances)) {
      if (instData.map) mapData[instName] = instData.map;
      if (instData.friction_records) allRecords.push(...instData.friction_records);
    }
  }

  // ── Vue 1: Topology cards ──
  const topoDiv = document.getElementById('map-topology');
  topoDiv.innerHTML = '';

  const instNames = Object.keys(mapData);
  const instStats = {};
  instNames.forEach(instName => {
    const md = mapData[instName];
    const personaNames = Object.keys(md.persona_roles || {});
    const links = md.links || [];
    const totalFrictions = links.reduce((s, l) => s + l.total, 0);
    const personasWithFriction = new Set(links.map(l => l.persona));
    const healthPct = personaNames.length > 0 ? Math.round(personasWithFriction.size / personaNames.length * 100) : 0;
    instStats[instName] = { personaNames, links, totalFrictions, personasWithFriction, healthPct };
  });

  const topoCards = [];
  instNames.forEach((instName, instIdx) => {
    const md = mapData[instName];
    const st = instStats[instName];
    const color = instanceColors[instIdx % instanceColors.length];
    const healthColor = st.healthPct > 75 ? '#3ddc84' : st.healthPct > 50 ? '#d4a030' : '#e05050';
    const borderExtra = st.healthPct < 50 ? 'border-color: #e05050;' : '';

    let card = '<div class="instance-card" style="border-left: 3px solid ' + color + '; ' + borderExtra + '" oncontextmenu="showCtxMenu(event,\'' + instName + '\',\'\')" title="' + st.personaNames.length + ' personas, ' + st.totalFrictions + ' frictions, health ' + st.healthPct + '%">';
    card += '<div class="inst-header"><span class="health-dot" style="background:' + healthColor + '"></span><span class="inst-name">' + instName + '</span><span style="margin-left:auto; font-family:var(--font-mono); font-size:9px; color:var(--ice-muted);">' + st.totalFrictions + ' frictions</span></div>';
    if (md.description) card += '<div class="inst-desc">' + md.description.substring(0, 100).replace(/</g, '&lt;') + '</div>';
    card += '<ul class="persona-list">';
    st.personaNames.forEach(p => {
      const role = (md.persona_roles[p] || '').replace(/'/g, '&#39;');
      const hasFriction = st.personasWithFriction.has(p);
      const link = st.links.find(l => l.persona === p);
      const fCount = link ? link.total : 0;
      const dotBg = hasFriction ? color : 'var(--ice-muted)';
      card += '<li class="' + (hasFriction ? '' : 'no-friction') + '" oncontextmenu="showCtxMenu(event,\'' + instName + '\',\'' + p + '\')" title="' + role + ' - ' + fCount + ' frictions"><span class="p-dot" style="background:' + dotBg + '"></span>' + p + '<span class="p-role">' + role + '</span></li>';
    });
    card += '</ul></div>';
    topoCards.push(card);
  });
  topoDiv.innerHTML = topoCards.join('');

  // ── Trajectory — challenge % ──
  const trajCanvas = document.getElementById('map-trajectory');
  if (!trajCanvas || !allRecords.length) return;

  const mk = ['sound','contestable','simplification','blind_spot','refuted'];
  const trajW = 15;
  const filteredRecs = allRecords.filter(r => !r.is_amendment);

  const windows = [];
  for (let i = 0; i < filteredRecs.length; i += trajW) {
    const slice = filteredRecs.slice(i, i + trajW);
    if (slice.length < 3) break;
    const total = slice.length;
    const challenge = slice.filter(r => r.marker !== 'sound').length;
    const challengePct = Math.round(challenge / total * 100);
    const dateRange = slice[0].date + ' → ' + slice[slice.length-1].date;
    windows.push({ label: 'w' + (windows.length + 1), challengePct, dateRange, n: total });
  }

  if (windows.length > 0) {
    if (window._mapTrajectoryChart) window._mapTrajectoryChart.destroy();
    window._mapTrajectoryChart = new Chart(trajCanvas, {
      type: 'line',
      data: { labels: windows.map(w => w.label), datasets: [{
        label: 'Challenge %',
        data: windows.map(w => w.challengePct),
        borderColor: '#40d8c0', backgroundColor: 'rgba(64,216,192,0.1)',
        fill: true, tension: .3, borderWidth: 2, pointRadius: 3,
      }]},
      options: { responsive: true, maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: { callbacks: { afterLabel: ctx => windows[ctx.dataIndex].dateRange + ' (n=' + windows[ctx.dataIndex].n + ')' } }
        },
        scales: {
          y: { beginAtZero: true, max: 100, grid: { color: 'rgba(64,180,160,0.06)' }, ticks: { callback: v => v + '%' }, title: { display: true, text: 'challenge %', font: { size: 9, family: "'IBM Plex Mono'" }, color: 'rgba(160,208,200,0.4)' } },
          x: { grid: { display: false }, title: { display: true, text: 'friction windows', font: { size: 9, family: "'IBM Plex Mono'" }, color: 'rgba(160,208,200,0.4)' } }
        }
      }
    });
  }

  // ── Persona mini cards ──
  const cardsDiv = document.getElementById('map-persona-cards');
  if (cardsDiv) {
    const cards = [];
    instNames.forEach((instName, instIdx) => {
      const md = mapData[instName];
      const color = instanceColors[instIdx % instanceColors.length];
      const personaNames = Object.keys(md.persona_roles || {});
      const links = md.links || [];

      const ctxSizes = md.context_sizes || {};

      personaNames.forEach(p => {
        const role = (md.persona_roles[p] || '').replace(/'/g, '&#39;');
        const link = links.find(l => l.persona === p);
        const frictions = link ? link.total : 0;
        const ctx = ctxSizes[p];
        const ctxLines = ctx ? ctx.total_lines : '—';
        const ctxColor = ctx ? (ctx.status === 'ok' ? '#3ddc84' : ctx.status === 'warn' ? '#d4a030' : '#e05050') : 'var(--ice-muted)';
        const healthColor = frictions > 0 ? '#3ddc84' : '#e05050';

        cards.push('<div class="persona-mini" style="border-left:3px solid ' + color + '" oncontextmenu="showCtxMenu(event,\'' + instName + '\',\'' + p + '\')" title="' + role + ' · ' + instName + '">' +
          '<div class="pm-name">' + p + '</div>' +
          '<div class="pm-role">' + role + '</div>' +
          '<div class="pm-stats">' +
            '<div class="pm-stat"><span class="pm-val" style="color:' + healthColor + '">' + frictions + '</span><span class="pm-label">frictions</span></div>' +
            '<div class="pm-stat"><span class="pm-val" style="color:' + ctxColor + '">' + ctxLines + '</span><span class="pm-label">ctx lines</span></div>' +
          '</div>' +
        '</div>');
      });
    });
    cardsDiv.innerHTML = cards.join('');
  }
}
