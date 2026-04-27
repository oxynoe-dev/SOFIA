// ── Records ──

function renderRecords() {
  var D = getCurrentMirrorData();
  if (!D) return;

  var records = D.friction_records || [];
  var personas = getFilteredPersonas(D);
  var periodVal = document.getElementById('sel-period').value;

  // Filter by persona
  if (personas.length < (D.meta.personas || []).length) {
    var set = new Set(personas);
    records = records.filter(function(r) { return set.has(r.persona); });
  }

  // Filter by period
  if (periodVal !== 'all') {
    var days = parseInt(periodVal);
    var now = new Date(D.meta.date);
    var cutoff = new Date(now.getTime() - days * 86400000);
    records = records.filter(function(r) {
      return new Date(r.date) >= cutoff;
    });
  }

  // Sort
  var sortVal = document.getElementById('records-sort').value;
  records = records.slice(); // copy before sort
  if (sortVal === 'date-desc') records.sort(function(a, b) { return b.date.localeCompare(a.date); });
  else if (sortVal === 'date-asc') records.sort(function(a, b) { return a.date.localeCompare(b.date); });
  else if (sortVal === 'persona') records.sort(function(a, b) { return a.persona.localeCompare(b.persona) || b.date.localeCompare(a.date); });
  else if (sortVal === 'marker') records.sort(function(a, b) { return (a.marker || '').localeCompare(b.marker || '') || b.date.localeCompare(a.date); });
  else if (sortVal === 'resolution') records.sort(function(a, b) { return (a.resolution || 'zzz').localeCompare(b.resolution || 'zzz') || b.date.localeCompare(a.date); });

  // Count
  var el = document.getElementById('records-count');
  if (el) el.textContent = records.length + ' friction' + (records.length !== 1 ? 's' : '');

  // Render
  var markerColors = {
    sound: C.sound, contestable: C.contestable, simplification: C.simplification,
    blind_spot: C.blind_spot, refuted: C.refuted,
  };
  var resColors = {
    ratified: C.ratified, contested: C.contested, revised: C.revised, rejected: C.rejected,
  };
  var markerIcons = {
    sound: '\u2713', contestable: '~', simplification: '\u26A1',
    blind_spot: '\u25D0', refuted: '\u2717',
  };

  function esc(s) { return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }

  // Detect sanitized data (no descriptions)
  var hasDesc = records.some(function(r) { return r.description && r.description.length > 0; });

  var tbody = document.getElementById('table-records');
  var html = '';
  for (var i = 0; i < records.length; i++) {
    var r = records[i];
    var mc = markerColors[r.marker] || 'var(--ice-dim)';
    var rc = resColors[r.resolution] || 'var(--ice-muted)';
    var icon = markerIcons[r.marker] || '?';
    var initLabel = r.initiative === 'PO' ? 'H' : 'A';
    var initColor = r.initiative === 'PO' ? 'var(--ready)' : 'var(--violet)';
    html += '<tr>';
    html += '<td style="white-space:nowrap">' + r.date + '</td>';
    html += '<td class="name">' + r.persona + '</td>';
    html += '<td style="color:' + mc + '">' + icon + ' ' + (r.marker || '') + '</td>';
    html += '<td style="color:' + initColor + '">' + initLabel + '</td>';
    html += '<td style="color:' + rc + '">' + (r.resolution || '<span style="opacity:.3">—</span>') + '</td>';
    if (hasDesc) {
      html += '<td style="color:var(--ice-dim); font-family:var(--font-sans); font-size:11px">' + esc(r.description || '') + '</td>';
      var source = r.source || '';
      html += '<td style="color:var(--ice-muted); font-size:10px" title="' + esc(source) + '">' + esc(source.split('/').pop() || '') + '</td>';
    }
    html += '</tr>';
  }
  tbody.innerHTML = html;
}
