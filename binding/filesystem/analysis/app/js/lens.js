// ── Lens ──

function renderCurrent() {
  // Destroy previous charts
  charts.forEach(c => c.destroy());
  charts = [];

  // Also re-render pilotage if that tab is active
  if (document.getElementById('tab-mirror').classList.contains('active')) {
    renderMirror();
  }

  const D = getCurrentData();
  const t = D.totals, P = D.personas;
  const personas = getFilteredPersonas(D);
  const gran = document.getElementById('sel-granularity').value;
  const periodVal = document.getElementById('sel-period').value;
  const inst = document.getElementById('sel-instance').value;

  // Select time series: per-persona if filtered, global otherwise
  const selPersona = document.getElementById('sel-persona').value;
  const rawTs = (selPersona !== 'all' && D.personas[selPersona] && D.personas[selPersona].time_series)
    ? D.personas[selPersona].time_series[gran]
    : D.time_series[gran];
  const ts = filterByPeriod(rawTs, periodVal);
  const weeks = ts.labels;

  function filterByPeriod(series, period) {
    if (period === 'all') return series;
    const days = parseInt(period);
    const now = new Date(D.meta.date);
    const cutoff = new Date(now.getTime() - days * 86400000);

    // Convert label to date for comparison
    function labelToDate(label) {
      // YYYY-MM-DD
      if (/^\d{4}-\d{2}-\d{2}$/.test(label)) return new Date(label);
      // YYYY-WNN — approximate: week start
      const m = label.match(/^(\d{4})-W(\d{2})$/);
      if (m) {
        const jan4 = new Date(parseInt(m[1]), 0, 4);
        const weekStart = new Date(jan4.getTime() + (parseInt(m[2]) - 1) * 7 * 86400000);
        return weekStart;
      }
      return new Date(0);
    }

    const indices = [];
    series.labels.forEach((l, i) => { if (labelToDate(l) >= cutoff) indices.push(i); });

    if (indices.length === 0) return series; // fallback: show all

    const pick = (arr) => indices.map(i => arr[i]);
    const pickObj = (obj) => {
      const r = {};
      for (const [k, v] of Object.entries(obj)) r[k] = Array.isArray(v) ? pick(v) : v;
      return r;
    };

    return {
      labels: pick(series.labels),
      markers: pickObj(series.markers),
      directions: pickObj(series.directions),
      resolutions: pickObj(series.resolutions),
      frictions_per_session: pick(series.frictions_per_session || []),
      resolutions_per_session: pick(series.resolutions_per_session || []),
      flux_h: pick(series.flux_h),
      flux_a: pick(series.flux_a),
      sessions: pick(series.sessions || []),
      artefacts: pick(series.artefacts || []),
      frictions_sessions: pick(series.frictions_sessions || []),
      frictions_artefacts: pick(series.frictions_artefacts || []),
    };
  }

  // Meta
  const metaEl = document.querySelector('.meta');
  if (metaEl) metaEl.textContent = `instance: ${inst === 'all' ? 'all' : inst} · ${D.meta.date}`;

  // Compute totals from filtered time series
  const mk = ['sound','contestable','simplification','blind_spot','refuted'];
  const rk = ['ratified','contested','revised','rejected'];
  const dk = ['a_corroborates_h','a_contests_h','h_corroborates_a','h_contests_a'];

  const sum = arr => arr.reduce((a,b) => a+b, 0);
  const tsFrictions = mk.reduce((s,k) => s + sum(ts.markers[k] || []), 0);
  const tsResolved = rk.reduce((s,k) => s + sum(ts.resolutions[k] || []), 0);
  const tsResolvedPct = tsFrictions > 0 ? Math.round(tsResolved / tsFrictions * 100) : 0;
  const tsRatifie = sum(ts.resolutions.ratified || []);
  const tsConteste = sum(ts.resolutions.contested || []);
  const tsSp = t.signaler_pattern;
  const tsSessions = sum(ts.sessions || []);

  document.getElementById('scores').innerHTML = `
    <div class="score-card accent" title="Total friction markers detected in the selected period."><div class="value">${tsFrictions}</div><div class="label">Frictions</div></div>
    <div class="score-card violet" title="Percentage of frictions that received a resolution (ratified, contested, revised, rejected)."><div class="value">${tsResolvedPct}%</div><div class="label">Resolved</div></div>
    <div class="score-card done" title="Frictions where the position was accepted by the other party."><div class="value">${tsRatifie}</div><div class="label">Ratified</div></div>
    <div class="score-card amber" title="Frictions where disagreement was maintained — no change of position."><div class="value">${tsConteste}</div><div class="label">Contested</div></div>
    <div class="score-card coral" title="Number of reportPattern triggers — convergence of rejections detected by a persona."><div class="value">${tsSp}</div><div class="label">reportPattern</div></div>`;

  function mkChart(id, cfg) { const c = new Chart(document.getElementById(id), cfg); charts.push(c); }

  // Axis label helper
  const axisTitle = (text) => ({ display: true, text, font: { size: 9, family: "'IBM Plex Mono'" }, color: 'rgba(160,208,200,0.4)' });

  // 1. Friction by marker — timeline
  mkChart('chart-friction-time', {
    type: 'line', data: { labels: weeks, datasets: [
      { label: 'sound', data: ts.markers.sound, ...lineOpts(C.sound) },
      { label: 'contestable', data: ts.markers.contestable, ...lineOpts(C.contestable) },
      { label: 'simplification', data: ts.markers.simplification, ...lineOpts(C.simplification) },
      { label: 'blind spot', data: ts.markers.blind_spot, ...lineOpts(C.blind_spot) },
      { label: 'refuted', data: ts.markers.refuted, ...lineOpts(C.refuted) },
    ]},
    options: { responsive: true, maintainAspectRatio: false,
      plugins: { legend: { position: 'top', labels: { boxWidth: 10, padding: 15 } } },
      scales: { y: { ...gridY, title: axisTitle('count') }, x: { ...noGridX, title: axisTitle('period') } } }
  });

  // 2. Direction — who contests whom
  mkChart('chart-direction', {
    type: 'bar', data: { labels: personas, datasets: [
      { label: 'A corroborates H', data: personas.map(p => g(P[p].directions, 'a_corroborates_h')), backgroundColor: C.a_corroborates_h },
      { label: 'A contests H', data: personas.map(p => g(P[p].directions, 'a_contests_h')), backgroundColor: C.a_contests_h },
      { label: 'H corroborates A', data: personas.map(p => -g(P[p].directions, 'h_corroborates_a')), backgroundColor: C.h_corroborates_a },
      { label: 'H contests A', data: personas.map(p => -g(P[p].directions, 'h_contests_a')), backgroundColor: C.h_contests_a },
    ]},
    options: { responsive: true, maintainAspectRatio: false, indexAxis: 'y',
      plugins: { legend: { position: 'top', labels: { boxWidth: 10, padding: 12 } },
        tooltip: { callbacks: { label: ctx => ctx.dataset.label + ': ' + Math.abs(ctx.raw) } } },
      scales: { x: { grid: { color: 'rgba(64,180,160,0.06)' }, ticks: { callback: v => Math.abs(v) }, title: axisTitle('← H positions · A positions →') },
                y: { stacked: true, grid: { display: false } } } }
  });

  // 3. Direction — timeline
  mkChart('chart-direction-time', {
    type: 'line', data: { labels: weeks, datasets: [
      { label: 'A contests H', data: ts.directions.a_contests_h, borderColor: '#e05050', backgroundColor: '#e0505020', fill: true, tension: .3 },
      { label: 'H contests A', data: ts.directions.h_contests_a, borderColor: '#d4a030', backgroundColor: '#d4a03020', fill: true, tension: .3 },
      { label: 'A corroborates H', data: ts.directions.a_corroborates_h, borderColor: '#3ddc84', backgroundColor: '#3ddc8415', fill: true, tension: .3 },
      { label: 'H corroborates A', data: ts.directions.h_corroborates_a, borderColor: '#40d8c0', backgroundColor: '#40d8c015', fill: true, tension: .3 },
    ]},
    options: { responsive: true, maintainAspectRatio: false,
      plugins: { legend: { position: 'top', labels: { boxWidth: 10, padding: 12 } } },
      scales: { y: { ...gridY, title: axisTitle('count') }, x: { ...noGridX, title: axisTitle('period') } } }
  });

  // 4. Marqueurs par persona
  mkChart('chart-markers-persona', {
    type: 'bar', data: { labels: personas, datasets: mk.map(k => ({
      label: k.replace('_','-'), data: personas.map(p => g(P[p].markers, k)), backgroundColor: C[k]
    }))},
    options: { responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: { x: { stacked: true, ...noGridX }, y: { stacked: true, ...gridY, title: axisTitle('count') } } }
  });

  // 5. Resolutions by persona
  mkChart('chart-resolutions', {
    type: 'bar', data: { labels: personas, datasets: rk.map(k => ({
      label: k, data: personas.map(p => g(P[p].resolutions, k)), backgroundColor: C[k]
    }))},
    options: { responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: { x: { stacked: true, ...noGridX }, y: { stacked: true, ...gridY, title: axisTitle('count') } } }
  });

  // 6. Epistemic flow
  mkChart('chart-flux', {
    type: 'bar', data: { labels: personas, datasets: [
      { label: 'H (human)', data: personas.map(p => P[p].flux_h_pct), backgroundColor: C.humain },
      { label: 'A (assistant)', data: personas.map(p => P[p].flux_a_pct), backgroundColor: C.assistant },
    ]},
    options: { responsive: true, maintainAspectRatio: false, indexAxis: 'y',
      plugins: { legend: { position: 'top', labels: { boxWidth: 10, padding: 15 } } },
      scales: { x: { stacked: true, beginAtZero: true, max: 100, grid: { color: 'rgba(64,180,160,0.06)' }, ticks: { callback: v => v + '%' }, title: axisTitle('contribution %') },
                y: { stacked: true, ...noGridX } } }
  });

  // 7. Frictions per session — timeline
  mkChart('chart-ratio', {
    type: 'line', data: { labels: weeks, datasets: [
      { label: 'frictions/session', data: ts.frictions_per_session, ...lineOpts(C.humain) },
      { label: 'resolutions/session', data: ts.resolutions_per_session, ...lineOpts(C.assistant) },
    ]},
    options: { responsive: true, maintainAspectRatio: false,
      plugins: { legend: { position: 'top', labels: { boxWidth: 10, padding: 15 } } },
      scales: { y: { ...gridY, title: axisTitle('avg per session') }, x: { ...noGridX, title: axisTitle('period') } } }
  });

  // Tables
  const td = (v, cls='num') => `<td class="${cls}">${v}</td>`;
  const ratioColor = r => r > 2 ? 'var(--ready)' : r < 0.5 ? 'var(--coral)' : 'var(--ice-dim)';

  document.getElementById('table-direction').innerHTML = personas.map(p => {
    const d = P[p].directions || {};
    return `<tr><td class="name">${p}</td>${td(g(d,'a_corroborates_h'))}${td(g(d,'a_contests_h'))}${td(g(d,'h_corroborates_a'))}${td(g(d,'h_contests_a'))}<td class="num" style="color:${ratioColor(P[p].direction_ratio)}">${P[p].direction_ratio}</td></tr>`;
  }).join('');

  document.getElementById('table-detail').innerHTML = personas.map(p => {
    const d = P[p], m = d.markers || {}, r = d.resolutions || {};
    return `<tr><td class="name">${p}</td>${td(d.sessions)}${td(g(m,'sound'))}${td(g(m,'contestable'))}${td(g(m,'simplification'))}${td(g(m,'blind_spot'))}${td(g(m,'refuted'))}${td(g(r,'ratified'))}${td(g(r,'contested'))}${td(g(r,'revised'))}${td(g(r,'rejected'))}${td(d.flux_h_pct+':'+d.flux_a_pct)}${td(d.signaler_pattern_count)}</tr>`;
  }).join('');

  const spPersonas = personas.filter(p => P[p].signaler_pattern_count > 0);
  document.getElementById('table-sp').innerHTML = spPersonas.length ? spPersonas.map(p => {
    const d = P[p];
    return `<tr><td class="name">${p}</td>${td(d.signaler_pattern_count)}${td(d.signaler_pattern_erreur_llm)}${td(d.signaler_pattern_conviction)}${td(d.signaler_pattern_resistance)}</tr>`;
  }).join('') : '<tr><td colspan="5" style="color:var(--ice-muted)">No triggers</td></tr>';
}
