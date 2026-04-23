// ── Mirror ──
let mirrorCharts = [];

function renderMirror() {
  mirrorCharts.forEach(c => c.destroy());
  mirrorCharts = [];

  const D = getCurrentMirrorData();
  if (!D) return;
  const personas = getFilteredPersonas(D);
  const records = D.friction_records || [];
  const N = 25; // window size for baseline/recent

  const mk = ['sound','contestable','simplification','blind_spot','refuted'];
  const W = 15; // window size for trajectory
  const fmLabels = { glissement: 'slip', usure: 'wear', ecrasement: 'crush', asymetrie: 'asymmetry', instabilite: 'instability' };

  function mkChart2(id, cfg) { const c = new Chart(document.getElementById(id), cfg); mirrorCharts.push(c); }

  // ── Bandeau KPI ──
  const nonAmendments = records.filter(r => !r.is_amendment && personas.includes(r.persona));
  const recentN = nonAmendments.slice(-N);
  const allOpen = nonAmendments.filter(r => !r.resolution);
  const recentChallenge = recentN.length > 0 ? Math.round(recentN.filter(r => r.marker !== 'sound').length / recentN.length * 100) : 0;
  const hContestsA = recentN.filter(r => r.direction === 'h_contests_a').length;
  const openCount = allOpen.length;
  const complaisant = hContestsA === 0 && openCount > 10;
  const realPersonas = D.meta.personas || personas;
  const personasWithFriction = new Set(nonAmendments.filter(r => realPersonas.includes(r.persona)).map(r => r.persona)).size;
  const totalPersonas = realPersonas.length;
  const coverage = totalPersonas > 0 ? Math.round(personasWithFriction / totalPersonas * 100) : 0;

  const complaisantLabel = complaisant ? 'complacent' : 'healthy';
  const complaisantClass = complaisant ? 'coral' : 'done';
  const healthClass = recentChallenge > 20 ? 'done' : recentChallenge > 10 ? 'amber' : 'coral';
  const coverageClass = coverage > 80 ? 'done' : coverage > 50 ? 'amber' : 'coral';

  document.getElementById('mirror-kpi').innerHTML = `
    <div class="score-card ${complaisantClass}" title="${complaisant ? 'The orchestrator no longer contests personas AND does not arbitrate submitted frictions. Both conditions together signal complacency.' : 'The orchestrator actively contests and arbitrates. No complacency signal detected.'}"><div class="value">${complaisantLabel}</div><div class="label">Orchestrator</div></div>
    <div class="score-card ${healthClass}" title="Share of recent frictions that contest, flag a simplification or a blind spot. Low challenge % = personas validate without resistance."><div class="value">${recentChallenge}%</div><div class="label">Recent challenge</div></div>
    <div class="score-card accent" title="Frictions without resolution — piloting debt. The orchestrator sees the list, arbitrates in the next session, the friction leaves the list."><div class="value">${openCount}</div><div class="label">Open frictions</div></div>
    <div class="score-card ${coverageClass}" title="A persona with no friction is invisible to the protocol. 100% coverage = all personas participate in the friction cycle."><div class="value">${coverage}%</div><div class="label">Coverage (${personasWithFriction}/${totalPersonas})</div></div>
    <div class="score-card" title="Epistemic contributions: PO (orchestrator) vs A (assistants). Balanced = co-construction."><div class="value" style="color:var(--ice); font-size:22px;"><span style="color:var(--ready)">${personas.reduce((s, p) => s + (D.personas[p]?.flux_h || 0), 0)}</span> / <span style="color:var(--violet)">${personas.reduce((s, p) => s + (D.personas[p]?.flux_a || 0), 0)}</span></div><div class="label">PO / A contrib</div></div>
  `;

  // ── Vue 0: Trajectoire instance ──
  const filteredRecords = records.filter(r => personas.includes(r.persona) && !r.is_amendment);

  const windows = [];
  for (let i = 0; i < filteredRecords.length; i += W) {
    const slice = filteredRecords.slice(i, i + W);
    if (slice.length < 3) break;
    const total = slice.length;
    const challenge = slice.filter(r => r.marker !== 'sound').length;
    const challengePct = Math.round(challenge / total * 100);
    const markerCounts = {};
    mk.forEach(m => markerCounts[m] = slice.filter(r => r.marker === m).length);
    const dateRange = `${slice[0].date} → ${slice[slice.length-1].date}`;
    windows.push({ label: `w${windows.length + 1}`, challengePct, markerCounts, dateRange, n: total });
  }

  if (windows.length > 0) {
    const wLabels = windows.map(w => w.label);

    mkChart2('chart-trajectory-line', {
      type: 'line',
      data: { labels: wLabels, datasets: [{
        label: 'Challenge %',
        data: windows.map(w => w.challengePct),
        borderColor: '#40d8c0', backgroundColor: 'rgba(64,216,192,0.1)',
        fill: true, tension: .3, borderWidth: 2, pointRadius: 3,
      }]},
      options: { responsive: true, maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: { callbacks: { afterLabel: ctx => windows[ctx.dataIndex].dateRange + ` (n=${windows[ctx.dataIndex].n})` } }
        },
        scales: { y: { beginAtZero: true, max: 100, grid: { color: 'rgba(64,180,160,0.06)' }, ticks: { callback: v => v + '%' } }, x: { grid: { display: false } } }
      }
    });

    mkChart2('chart-trajectory-bar', {
      type: 'bar',
      data: { labels: wLabels, datasets: mk.map(m => ({
        label: m.replace('_', ' '), data: windows.map(w => w.markerCounts[m]), backgroundColor: C[m],
      }))},
      options: { responsive: true, maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top', labels: { boxWidth: 10, padding: 10 } },
          tooltip: { callbacks: { afterTitle: ctx => windows[ctx[0].dataIndex].dateRange } }
        },
        scales: { x: { stacked: true, grid: { display: false } }, y: { stacked: true, beginAtZero: true, grid: { color: 'rgba(64,180,160,0.06)' } } }
      }
    });
  }

  // ── Per-persona friction records ──
  const byPersona = {};
  for (const r of records) {
    if (!byPersona[r.persona]) byPersona[r.persona] = [];
    byPersona[r.persona].push(r);
  }

  // ── Helper: compute profile from a set of records (5 axes) ──
  const radarLabels = ['Challenge %', 'A→H %', 'H→A %', 'Resolved %', 'Diversity %', 'Contribution %'];
  const radarColors = [
    '#40d8c0', '#a78bfa', '#e05050', '#d4a030', '#3ddc84',
    '#8aa8d8', '#ff9966', '#66cccc', '#cc99ff', '#ff6699',
  ];

  function computeProfile(recs) {
    if (!recs.length) return { challenge: 0, aContestsH: 0, hContestsA: 0, resolved: 0, diversity: 0 };
    const total = recs.length;
    const challenge = recs.filter(r => r.marker !== 'sound').length / total;
    const aContH = recs.filter(r => r.direction === 'a_contests_h').length / total;
    const hContA = recs.filter(r => r.direction === 'h_contests_a').length / total;
    const resolved = recs.filter(r => r.resolution).length / total;
    const resCounts = {};
    recs.forEach(r => { if (r.resolution) resCounts[r.resolution] = (resCounts[r.resolution] || 0) + 1; });
    const resTypes = Object.keys(resCounts).length;
    const diversity = resTypes / 4;
    return {
      challenge: Math.round(challenge * 100),
      aContestsH: Math.round(aContH * 100),
      hContestsA: Math.round(hContA * 100),
      resolved: Math.round(resolved * 100),
      diversity: Math.round(diversity * 100),
    };
  }
  function profileToArray(p, contribPct) { return [p.challenge, p.aContestsH, p.hContestsA, p.resolved, p.diversity, contribPct || 0]; }

  // ── Compute all profiles ──
  const deltaRows = [];
  const personaProfiles = {};

  for (const p of personas) {
    const pRecs = byPersona[p] || [];
    if (!pRecs.length) continue;
    const baseline = computeProfile(pRecs.slice(0, N));
    const recent = computeProfile(pRecs.slice(-N));

    const pd = D.personas[p] || {};
    const totalFlux = (pd.flux_h || 0) + (pd.flux_a || 0);
    const contribPct = totalFlux > 0 ? Math.round((pd.flux_a || 0) / totalFlux * 100) : 0;

    // Diagnostic from server-side failure_modes.per_persona (non-exclusive)
    const pFm = D.failure_modes?.per_persona?.[p];
    const diagModes = pFm?.modes || [];
    const dominant = pFm?.dominant || 'healthy';
    const diagClass = dominant === 'healthy' ? 'healthy' : dominant;

    personaProfiles[p] = { baseline, recent, diagModes, dominant, diagClass, contribPct };

    const deltaChall = recent.challenge - baseline.challenge;
    const arrow = deltaChall > 5 ? '↑' : deltaChall < -5 ? '↓' : '=';
    deltaRows.push({ p, baseline, recent, deltaChall, arrow, diagModes, dominant, diagClass });
  }

  // ── Vue 1a: Radar instance agrege ──
  const instanceRadarEl = document.getElementById('radar-instance');
  if (instanceRadarEl && filteredRecords.length > 0) {
    const instanceBaseline = computeProfile(filteredRecords.slice(0, N));
    const instanceRecent = computeProfile(filteredRecords.slice(-N));
    const instFluxA = personas.reduce((s, p) => s + (D.personas[p]?.flux_a || 0), 0);
    const instFluxH = personas.reduce((s, p) => s + (D.personas[p]?.flux_h || 0), 0);
    const instTotalFlux = instFluxA + instFluxH;
    const instContribPct = instTotalFlux > 0 ? Math.round(instFluxA / instTotalFlux * 100) : 0;
    mkChart2('radar-instance', {
      type: 'radar',
      data: { labels: radarLabels, datasets: [
        { label: 'Baseline', data: profileToArray(instanceBaseline, instContribPct),
          borderColor: 'rgba(160,208,200,0.5)', backgroundColor: 'rgba(160,208,200,0.08)', borderWidth: 1.5, pointRadius: 3 },
        { label: 'Recent', data: profileToArray(instanceRecent, instContribPct),
          borderColor: '#40d8c0', backgroundColor: 'rgba(64,216,192,0.12)', borderWidth: 2, pointRadius: 4 },
      ]},
      options: {
        responsive: true, maintainAspectRatio: true,
        scales: { r: { beginAtZero: true, max: 100, grid: { color: 'rgba(64,180,160,0.08)' }, ticks: { display: false }, pointLabels: { font: { size: 11 } } } },
        plugins: { legend: { position: 'bottom', labels: { boxWidth: 10, padding: 10, font: { size: 11 } } } }
      }
    });
  }

  // ── Vue 1b: Radars persona individuels ──
  const radarsDiv = document.getElementById('mirror-radars');
  radarsDiv.innerHTML = '';

  for (const p of personas) {
    const prof = personaProfiles[p];
    if (!prof) continue;

    const card = document.createElement('div');
    card.className = 'radar-card';
    const tagsHtml = prof.diagModes.length > 0
      ? prof.diagModes.map(m => `<span class="fm-tag ${m.level === 'alert' ? 'coral' : 'amber'}">${fmLabels[m.mode] || m.mode}</span>`).join(' ')
      : '<span class="fm-tag done">healthy</span>';
    card.innerHTML = `<div class="persona-name">${p}</div><canvas id="radar-${p}" width="240" height="240"></canvas><div class="diagnostic">${tagsHtml}</div>`;
    radarsDiv.appendChild(card);

    const chart = new Chart(document.getElementById('radar-' + p), {
      type: 'radar',
      data: {
        labels: radarLabels,
        datasets: [
          { label: 'Baseline', data: profileToArray(prof.baseline, prof.contribPct),
            borderColor: 'rgba(160,208,200,0.4)', backgroundColor: 'rgba(160,208,200,0.08)', borderWidth: 1, pointRadius: 2 },
          { label: 'Recent', data: profileToArray(prof.recent, prof.contribPct),
            borderColor: '#a78bfa', backgroundColor: 'rgba(167,139,250,0.12)', borderWidth: 1.5, pointRadius: 3 },
        ]
      },
      options: {
        responsive: false, maintainAspectRatio: true,
        scales: { r: { beginAtZero: true, max: 100, grid: { color: 'rgba(64,180,160,0.08)' }, ticks: { display: false }, pointLabels: { font: { size: 8 } } } },
        plugins: { legend: { display: false } }
      }
    });
    mirrorCharts.push(chart);
  }

  // ── Tableau delta ──
  document.getElementById('table-delta').innerHTML = deltaRows.map(d =>
    `<tr><td class="name">${d.p}</td><td class="num">${d.baseline.challenge}%</td><td class="num">${d.recent.challenge}%</td><td class="num">${d.arrow}</td><td class="num">${d.baseline.aContestsH}%</td><td class="num">${d.recent.aContestsH}%</td><td>${d.diagModes.length > 0 ? d.diagModes.map(m => `<span class="fm-tag ${m.level === 'alert' ? 'coral' : 'amber'}">${fmLabels[m.mode]||m.mode}</span>`).join(' ') : '<span class="fm-tag done">healthy</span>'}</td></tr>`
  ).join('');

  // ── Failure modes panel ──
  const fmPanel = document.getElementById('failure-modes-panel');
  if (fmPanel && D.failure_modes) {
    const fm = D.failure_modes;
    const levelColor = { ok: 'done', signal: 'amber', alert: 'coral' };
    const levelIcon = { ok: '✓', signal: '~', alert: '!' };
    const modes = [
      { key: 'glissement', label: 'Slip', primary: `Non-resol. ${fm.glissement?.non_resolution_rate?.toFixed(0) ?? '—'}%`,
        secondary: [`Recurr: ${fm.glissement?.recurrence_count ?? 0}`, `Ratif: ${fm.glissement?.reflexive_ratification?.toFixed(0) ?? '—'}%`] },
      { key: 'usure', label: 'Wear', primary: `Challenge ${fm.usure?.challenge_pct_trend ?? '—'}`,
        secondary: [`Refuted: ${fm.usure?.refuted_count_recent ?? 0}`, `Delta: ${fm.usure?.delta_baseline_recent?.toFixed(0) ?? '—'}%`] },
      { key: 'ecrasement', label: 'Crush', primary: `Reject. ${fm.ecrasement?.rejection_rate?.toFixed(0) ?? '—'}%`,
        secondary: [`Density: ${fm.ecrasement?.density_ratio?.toFixed(1) ?? '—'}x`, fm.ecrasement?.direction ?? '—'] },
      { key: 'asymetrie', label: 'Asymmetry', primary: `Dir. ${fm.asymetrie?.direction_ratio?.toFixed(0) ?? '—'}%`,
        secondary: [] },
      { key: 'instabilite', label: 'Instability', primary: `Revised ${fm.instabilite?.revised_rate_recent?.toFixed(0) ?? '—'}%`,
        secondary: [`Re-cont: ${fm.instabilite?.recontestation_chains ?? 0}`] },
    ];
    fmPanel.innerHTML = modes.map(m => {
      const lvl = fm[m.key]?.level || 'ok';
      return `<div class="fm-column ${levelColor[lvl]}">
        <div class="fm-title">${m.label}</div>
        <div class="fm-level" style="color:var(--${levelColor[lvl]})">${levelIcon[lvl]}</div>
        <div class="fm-primary">${m.primary}</div>
        ${m.secondary.map(s => `<div class="fm-secondary">${s}</div>`).join('')}
      </div>`;
    }).join('');
  }

  // ── Vue 2: Open frictions ──
  const openRecs = records.filter(r => !r.resolution);
  const filteredOpen = personas.length === Object.keys(D.personas).length
    ? openRecs : openRecs.filter(r => personas.includes(r.persona));

  document.getElementById('table-open-frictions').innerHTML = filteredOpen.length
    ? filteredOpen.map(r =>
        `<tr><td class="num">${r.date}</td><td style="font-size:10px;max-width:200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${r.source}</td><td class="name">${r.persona}</td><td>${r.marker}</td><td style="font-size:10px">${r.direction}</td><td style="font-size:11px;max-width:300px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${r.description || ''}</td></tr>`
      ).join('')
    : '<tr><td colspan="6" style="color:var(--done)">No open frictions</td></tr>';

  // ── Vue 3: Carte du silence ──
  const silencePersonas = personas;
  // ── Contribution flow ──
  const contribTypes = ['substance', 'structure', 'contestation', 'decision'];
  const contribColors = { substance: '#40d8c0', structure: '#a78bfa', contestation: '#e05050', decision: '#d4a030' };
  const contribCanvas = document.getElementById('chart-contribution-flow');
  if (contribCanvas) {
    const datasets = contribTypes.map(t => ({
      label: t, backgroundColor: contribColors[t],
      data: personas.map(p => {
        const pd = D.personas[p] || {};
        const h = (pd.flux_types_h || {})[t] || 0;
        const a = (pd.flux_types_a || {})[t] || 0;
        return h + a;
      }),
    }));
    mkChart2('chart-contribution-flow', {
      type: 'bar',
      data: { labels: personas, datasets },
      options: { responsive: true, maintainAspectRatio: false,
        plugins: { legend: { position: 'top', labels: { boxWidth: 10, padding: 10 } } },
        scales: { x: { stacked: true, grid: { display: false } }, y: { stacked: true, beginAtZero: true, grid: { color: 'rgba(64,180,160,0.06)' }, title: { display: true, text: 'contributions', font: { size: 9, family: "'IBM Plex Mono'" }, color: 'rgba(160,208,200,0.4)' } } }
      }
    });
  }

  // ── Silence map ──
  const headerRow = document.getElementById('silence-header');
  headerRow.innerHTML = '<th>Persona</th>' + mk.map(m => `<th>${m.replace('_',' ')}</th>`).join('') + '<th>Total</th>';

  document.getElementById('table-silence').innerHTML = silencePersonas.map(p => {
    const pRecs = byPersona[p] || [];
    const counts = {};
    mk.forEach(m => counts[m] = pRecs.filter(r => r.marker === m).length);
    const total = pRecs.length;
    return `<tr><td class="name">${p}</td>${mk.map(m => `<td class="num ${counts[m] === 0 ? 'zero' : ''}">${counts[m]}</td>`).join('')}<td class="num">${total}</td></tr>`;
  }).join('');
}
