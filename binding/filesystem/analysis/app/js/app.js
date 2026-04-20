// ── Configuration ──
const DATA_URL = 'analysis.json';

Chart.defaults.color = '#a0d0c8';
Chart.defaults.borderColor = 'rgba(64,180,160,0.12)';
Chart.defaults.font.family = "'IBM Plex Mono', monospace";
Chart.defaults.font.size = 10;

const C = {
  sound: '#3ddc84', contestable: '#a0d0c8', simplification: '#d4a030',
  blind_spot: '#e05050', refuted: '#ff4444',
  ratified: '#3ddc84', contested: '#d4a030', revised: '#a78bfa', rejected: '#e05050',
  humain: '#40d8c0', assistant: '#a78bfa',
  a_corroborates_h: '#3ddc8480', a_contests_h: '#e0505080',
  h_corroborates_a: '#40d8c080', h_contests_a: '#d4a03080',
};
const lineOpts = (color) => ({ borderColor: color, backgroundColor: color + '20', fill: true, tension: .3 });
const gridY = { beginAtZero: true, grid: { color: 'rgba(64,180,160,0.06)' } };
const noGridX = { grid: { display: false } };
const g = (obj, key) => (obj || {})[key] || 0;

let RAW = null;        // full JSON
let charts = [];       // Chart instances for cleanup

// ── Tabs ──
let PROBE_DATA = null;
let currentProbeInstance = null;

function switchTab(tab) {
  document.querySelector('main').scrollTop = 0;
  document.querySelectorAll('.nav-links button').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
  document.getElementById('tab-' + tab).classList.add('active');
  document.querySelectorAll('.nav-links button').forEach(b => {
    if (b.getAttribute('onclick') === "switchTab('" + tab + "')") b.classList.add('active');
  });

  const subMenu = document.getElementById('probe-instances-menu');
  const filtersPanel = document.getElementById('filters-panel');
  const noSidebar = (tab === 'probe' || tab === 'map' || tab === 'legend');

  subMenu.classList.toggle('visible', tab === 'probe');
  filtersPanel.style.display = noSidebar ? 'none' : '';

  document.querySelectorAll('.tab-content').forEach(t => {
    t.style.paddingLeft = noSidebar ? '2rem' : '220px';
    if (tab === 'probe') t.style.paddingTop = '36px';
    else t.style.paddingTop = '';
  });

  if (tab === 'probe' && !PROBE_DATA) runProbe();
  if (tab === 'map') {
    const selInst = document.getElementById('sel-instance');
    const selPersona = document.getElementById('sel-persona');
    if (selInst && selInst.querySelector('option[value="all"]')) selInst.value = 'all';
    if (selPersona) selPersona.value = 'all';
    if (RAW) renderMap();
  }
  if (tab === 'mirror' && RAW) renderMirror();
  if (tab === 'legend') loadLegend();
}

function selectProbeInstance(name) {
  currentProbeInstance = name;
  document.querySelectorAll('.sub-menu button').forEach(b => b.classList.remove('active'));
  const btn = document.querySelector(`.sub-menu button[data-inst="${name}"]`);
  if (btn) btn.classList.add('active');
  if (PROBE_DATA) renderProbeInstance(name, PROBE_DATA[name]);
}

// ── Run analysis via server ──
function runAnalysis() {
  const btn = document.getElementById('btn-run');
  if (btn) { btn.classList.add('running'); btn.textContent = '⟳ ...'; }
  fetch('/run', { method: 'POST' })
    .then(r => {
      if (!r.ok) return r.json().then(d => { throw new Error(d.error || r.statusText); });
      return r.json();
    })
    .then(data => {
      RAW = data;
      renderCurrent();
      if (btn) { btn.textContent = '⟳ Analyser'; btn.classList.remove('running'); }
    })
    .catch(err => {
      if (btn) { btn.textContent = '⟳ Analyser'; btn.classList.remove('running'); }
      console.warn('Analysis error:', err.message);
    });
}

function runRefresh() {
  const btn = document.getElementById('btn-refresh');
  if (btn) { btn.textContent = '⟳ ...'; btn.disabled = true; }
  fetch('/refresh', { method: 'POST' })
    .then(r => { if (!r.ok) return r.json().then(d => { throw new Error(d.error || r.statusText); }); return r.json(); })
    .then(result => {
      fetch(DATA_URL).then(r => r.json()).then(data => { RAW = data; renderCurrent(); });
      if (result && Object.keys(result).length) { PROBE_DATA = result; if (currentProbeInstance) selectProbeInstance(currentProbeInstance); }
    })
    .catch(err => console.warn('Refresh error:', err.message))
    .finally(() => { if (btn) { btn.textContent = '⟳ Refresh'; btn.disabled = false; } });
}

// ── Filters ──
function initFilters() {
  const selInst = document.getElementById('sel-instance');
  const selPersona = document.getElementById('sel-persona');

  const instances = Object.keys(RAW.instances);
  const hasAll = !!RAW.all;
  selInst.innerHTML = '';
  if (hasAll) selInst.innerHTML += `<option value="all">All (${instances.length})</option>`;
  instances.forEach(name => selInst.innerHTML += `<option value="${name}">${name}</option>`);
  selInst.value = RAW.default || instances[0];

  selInst.addEventListener('change', () => { populatePersonas(); renderCurrent(); });
  selPersona.addEventListener('change', renderCurrent);
  document.getElementById('sel-period').addEventListener('change', renderCurrent);
  document.getElementById('sel-granularity').addEventListener('change', renderCurrent);

  populatePersonas();
}

function populatePersonas() {
  const D = getCurrentData();
  const selPersona = document.getElementById('sel-persona');
  const personas = (D.meta.personas || Object.keys(D.personas)).sort();
  selPersona.innerHTML = `<option value="all">All</option>`;
  personas.forEach(p => selPersona.innerHTML += `<option value="${p}">${p}</option>`);
}

function getCurrentData() {
  const inst = document.getElementById('sel-instance').value;
  if (inst === 'all') return RAW.all;
  return RAW.instances[inst];
}

function getFilteredPersonas(D) {
  const sel = document.getElementById('sel-persona').value;
  if (sel === 'all') return (D.meta.personas || Object.keys(D.personas)).sort();
  return [sel];
}

// ── Navigation ──
function navigateTo(tab, instance, persona) {
  hideCtxMenu();
  const selInst = document.getElementById('sel-instance');
  const selPersona = document.getElementById('sel-persona');
  if (selInst) {
    for (const opt of selInst.options) {
      if (opt.value === instance) { selInst.value = instance; break; }
    }
  }
  populatePersonas();
  if (selPersona && persona) {
    setTimeout(() => {
      for (const opt of selPersona.options) {
        if (opt.value === persona) { selPersona.value = persona; break; }
      }
      renderCurrent();
    }, 50);
  }
  switchTab(tab);
}

// ── Context menu ──
function showCtxMenu(e, instance, persona) {
  e.preventDefault();
  e.stopPropagation();
  document.getElementById('ctx-overlay').classList.add('visible');
  const menu = document.getElementById('ctx-menu');
  const label = persona ? `${persona} (${instance})` : instance;
  let html = `<div class="ctx-label">${label}</div>`;
  html += `<button onclick="navigateTo('mirror','${instance}','${persona || ''}')">→ Mirror</button>`;
  html += `<button onclick="navigateTo('lens','${instance}','${persona || ''}')">→ Lens</button>`;
  html += `<button onclick="navigateTo('probe','${instance}','')">→ Probe</button>`;
  menu.innerHTML = html;
  menu.style.left = e.clientX + 'px';
  menu.style.top = e.clientY + 'px';
  menu.classList.add('visible');
}

function hideCtxMenu() {
  document.getElementById('ctx-menu').classList.remove('visible');
  document.getElementById('ctx-overlay').classList.remove('visible');
}
document.addEventListener('keydown', (e) => { if (e.key === 'Escape') { hideCtxMenu(); closeCheckDetail(); } });
window.addEventListener('blur', hideCtxMenu);

// ── Check detail panel ──
const _cdPanel = document.createElement('div');
_cdPanel.className = 'check-detail-panel';
_cdPanel.innerHTML = '<div class="check-detail-header"><h3 id="cd-title"></h3><button class="check-detail-close" onclick="closeCheckDetail()">✕</button></div><div class="check-detail-body" id="cd-body"></div>';
document.body.appendChild(_cdPanel);

function openCheckDetail(chk) {
  const title = document.getElementById('cd-title');
  const body = document.getElementById('cd-body');
  const statusIcon = chk.status === 'fail' ? '✗' : '⚠';
  const statusColor = chk.status === 'fail' ? 'var(--coral)' : 'var(--amber)';
  title.innerHTML = `<span style="color:${statusColor}">${statusIcon}</span> ${chk.id}`;
  let html = `<div style="color:var(--ice-dim);margin-bottom:12px">${chk.detail || ''}</div>`;
  if (chk.files && chk.files.length > 0) {
    html += `<div class="file-count">${chk.files.length} file${chk.files.length > 1 ? 's' : ''}</div>`;
    for (const f of chk.files) {
      html += `<div class="file-item">${f}</div>`;
    }
  }
  body.innerHTML = html;
  _cdPanel.classList.add('open');
}

function closeCheckDetail() {
  _cdPanel.classList.remove('open');
}

_cdPanel.addEventListener('click', (e) => { if (e.target === _cdPanel) closeCheckDetail(); });

document.addEventListener('click', (e) => {
  const item = e.target.closest('[data-chk-idx]');
  if (!item || !window._auditChecks) return;
  const idx = parseInt(item.getAttribute('data-chk-idx'), 10);
  const chk = window._auditChecks[idx];
  if (chk) openCheckDetail(chk);
});

// ── Init ──
// Wrap all cards content in fig-inner
document.querySelectorAll('.chart-card, .table-card, .score-card, .instance-card, .persona-mini').forEach(card => {
  const inner = document.createElement('div');
  inner.className = 'fig-inner';
  while (card.firstChild) inner.appendChild(card.firstChild);
  card.appendChild(inner);
});

fetch(DATA_URL).then(r => r.json()).then(data => {
  RAW = data;
  initFilters();
  // Map is default — hide sidebar, render
  document.getElementById('filters-panel').style.display = 'none';
  document.querySelectorAll('.tab-content').forEach(t => t.style.paddingLeft = '2rem');
  renderMap();
  renderCurrent();
}).catch(() => {
  document.getElementById('scores').innerHTML =
    `<div class="score-card" style="grid-column:1/-1"><div class="label" style="color:var(--coral)">Loading error ${DATA_URL} — run: python3 analysis.py &lt;instance&gt;</div></div>`;
});
