// ── Configuration ──

Chart.defaults.color = '#a0d0c8';
Chart.defaults.borderColor = 'rgba(64,180,160,0.12)';
Chart.defaults.font.family = "'IBM Plex Mono', monospace";
Chart.defaults.font.size = 10;

var C = {
  sound: '#3ddc84', contestable: '#a0d0c8', simplification: '#d4a030',
  blind_spot: '#e05050', refuted: '#ff4444',
  ratified: '#3ddc84', contested: '#d4a030', revised: '#a78bfa', rejected: '#e05050',
  humain: '#40d8c0', assistant: '#a78bfa',
  a_corroborates_h: '#3ddc8480', a_contests_h: '#e0505080',
  h_corroborates_a: '#40d8c080', h_contests_a: '#d4a03080',
};
var lineOpts = (color) => ({ borderColor: color, backgroundColor: color + '20', fill: true, tension: .3 });
var gridY = { beginAtZero: true, grid: { color: 'rgba(64,180,160,0.06)' } };
var noGridX = { grid: { display: false } };
var g = (obj, key) => (obj || {})[key] || 0;

var charts = [];       // Chart instances for cleanup

// ── Per-view data ──
var LENS_DATA = null;   // from /lens
var MIRROR_DATA = null;  // from /mirror
var PROBE_DATA = null;   // from /audit
var currentProbeInstance = null;

// ── Data loading ──
function loadLensData() {
  if (LENS_DATA) return Promise.resolve(LENS_DATA);
  return fetch('/lens').then(r => r.json()).then(data => { LENS_DATA = data; return data; });
}

function loadMirrorData() {
  if (MIRROR_DATA) return Promise.resolve(MIRROR_DATA);
  return fetch('/mirror').then(r => r.json()).then(data => { MIRROR_DATA = data; return data; });
}

// ── Tabs ──
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
    loadMirrorData().then(() => renderMap());
  }
  if (tab === 'mirror') loadMirrorData().then(() => renderMirror());
  if (tab === 'lens') loadLensData().then(() => renderCurrent());
  if (tab === 'legend') loadLegend();
}

function selectProbeInstance(name) {
  currentProbeInstance = name;
  document.querySelectorAll('.sub-menu button').forEach(b => b.classList.remove('active'));
  const btn = document.querySelector(`.sub-menu button[data-inst="${name}"]`);
  if (btn) btn.classList.add('active');
  if (PROBE_DATA) renderProbeInstance(name, PROBE_DATA[name]);
}

// ── Refresh ──
function runRefresh() {
  const btn = document.getElementById('btn-refresh');
  if (btn) { btn.textContent = '⟳ ...'; btn.disabled = true; }
  fetch('/refresh', { method: 'POST' })
    .then(r => { if (!r.ok) return r.json().then(d => { throw new Error(d.error || r.statusText); }); return r.json(); })
    .then(result => {
      // Invalidate caches — next view switch will reload
      LENS_DATA = null;
      MIRROR_DATA = null;
      // Reload active view
      const activeTab = document.querySelector('.tab-content.active');
      if (activeTab) {
        const tabId = activeTab.id.replace('tab-', '');
        if (tabId === 'lens') loadLensData().then(() => renderCurrent());
        if (tabId === 'mirror') loadMirrorData().then(() => renderMirror());
        if (tabId === 'map') loadMirrorData().then(() => renderMap());
      }
      if (result && Object.keys(result).length) { PROBE_DATA = result; if (currentProbeInstance) selectProbeInstance(currentProbeInstance); }
    })
    .catch(err => console.warn('Refresh error:', err.message))
    .finally(() => { if (btn) { btn.textContent = '⟳ Refresh'; btn.disabled = false; } });
}

// ── Filters ──
function initFilters(data) {
  const selInst = document.getElementById('sel-instance');
  const selPersona = document.getElementById('sel-persona');

  const instances = Object.keys(data.instances);
  selInst.innerHTML = '';
  instances.forEach(name => selInst.innerHTML += `<option value="${name}">${name}</option>`);
  selInst.value = data.default || instances[0];

  selInst.addEventListener('change', () => {
    populatePersonas();
    // Re-render active view
    const activeTab = document.querySelector('.tab-content.active');
    if (activeTab) {
      const tabId = activeTab.id.replace('tab-', '');
      if (tabId === 'lens' && LENS_DATA) renderCurrent();
      if (tabId === 'mirror' && MIRROR_DATA) renderMirror();
    }
  });
  selPersona.addEventListener('change', () => {
    const activeTab = document.querySelector('.tab-content.active');
    if (activeTab) {
      const tabId = activeTab.id.replace('tab-', '');
      if (tabId === 'lens' && LENS_DATA) renderCurrent();
      if (tabId === 'mirror' && MIRROR_DATA) renderMirror();
    }
  });
  document.getElementById('sel-period').addEventListener('change', () => { if (LENS_DATA) renderCurrent(); });
  document.getElementById('sel-granularity').addEventListener('change', () => { if (LENS_DATA) renderCurrent(); });

  populatePersonas();
}

function populatePersonas() {
  // Use whichever data is available (both share the same instance/persona structure)
  const data = LENS_DATA || MIRROR_DATA;
  if (!data) return;
  const D = _getInstanceData(data);
  if (!D) return;
  const selPersona = document.getElementById('sel-persona');
  const personas = (D.meta.personas || Object.keys(D.personas || {})).sort();
  selPersona.innerHTML = `<option value="all">All</option>`;
  personas.forEach(p => selPersona.innerHTML += `<option value="${p}">${p}</option>`);
}

function _getInstanceData(data) {
  const inst = document.getElementById('sel-instance').value;
  return data.instances[inst];
}

function getCurrentLensData() {
  if (!LENS_DATA) return null;
  return _getInstanceData(LENS_DATA);
}

function getCurrentMirrorData() {
  if (!MIRROR_DATA) return null;
  return _getInstanceData(MIRROR_DATA);
}

function getFilteredPersonas(D) {
  const sel = document.getElementById('sel-persona').value;
  if (sel === 'all') return (D.meta.personas || Object.keys(D.personas || {})).sort();
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

// Boot: load mirror data (for Map default view), init filters, render
loadMirrorData().then(data => {
  initFilters(data);
  // Map is default — hide sidebar, render
  document.getElementById('filters-panel').style.display = 'none';
  document.querySelectorAll('.tab-content').forEach(t => t.style.paddingLeft = '2rem');
  renderMap();
}).catch(err => {
  console.warn('Boot error:', err.message);
  document.getElementById('map-topology').innerHTML =
    `<div class="score-card" style="grid-column:1/-1"><div class="label" style="color:var(--coral)">Loading error — run: python3 analysis.py &lt;instance&gt;</div></div>`;
});
