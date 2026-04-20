// ── Probe ──

function runProbe() {
  const subMenu = document.getElementById('probe-instances-menu');
  subMenu.innerHTML = '<button class="running" disabled>⟳ probing...</button>';
  fetch('/audit', { method: 'POST' })
    .then(r => {
      if (!r.ok) return r.json().then(d => { throw new Error(d.error || r.statusText); });
      return r.json();
    })
    .then(data => {
      PROBE_DATA = data;
      const instances = Object.keys(data);
      subMenu.innerHTML = instances.map(name =>
        `<button data-inst="${name}" onclick="selectProbeInstance('${name}')">${name}</button>`
      ).join('') + `<button onclick="runProbe()" title="Relancer l'audit" style="margin-left:2rem; color:var(--ready); font-size:14px;">⟳ Probe</button>`;
      if (instances.length > 0) selectProbeInstance(instances[0]);
    })
    .catch(err => {
      subMenu.innerHTML = `<button style="color:var(--coral)" disabled>Erreur : ${err.message}</button>`;
    });
}

function renderProbeInstance(instName, instData) {
  const container = document.getElementById('probe-content');
  let html = '';

  if (!instData || instData.error) {
    container.innerHTML = `<p style="color:var(--coral); text-align:center; padding:2rem">${instData?.error || 'No data'}</p>`;
    return;
  }

  {
    const dummy = 0; // keep indentation consistent

    // Context sizes
    const ctxSizes = instData.context_sizes;
    if (ctxSizes && Object.keys(ctxSizes).length > 0) {
      html += '<div class="audit-section"><h2>Context size — persona + context <i class=\"info-icon\">i<span class=\"info-tip\">Total lines of persona.md + contexte.md loaded at boot. Green &lt;150L, yellow 150-250L, red &gt;250L. Large contexts get compressed in long sessions — the persona loses instructions.</span></i></h2>';
      const sorted = Object.entries(ctxSizes).sort((a,b) => b[1].total_lines - a[1].total_lines);
      const maxLines = Math.max(...sorted.map(([,d]) => d.total_lines), 1);
      html += '<div style="display:flex; flex-direction:column; gap:6px; margin-bottom:1.5rem;">';
      for (const [p, d] of sorted) {
        const pct = Math.round(d.total_lines / 400 * 100); // 400L = max bar
        const color = d.status === 'ok' ? 'var(--done)' : d.status === 'warn' ? 'var(--amber)' : 'var(--coral)';
        const icon = d.status === 'ok' ? '✓' : d.status === 'warn' ? '⚠' : '✗';
        html += `<div style="display:flex; align-items:center; gap:8px; font-family:var(--font-mono); font-size:11px;">
          <span style="width:120px; color:var(--ice)">${p}</span>
          <div style="flex:1; height:16px; background:var(--deep); border-radius:3px; overflow:hidden; border:1px solid var(--border);">
            <div style="width:${Math.min(pct,100)}%; height:100%; background:${color}; opacity:0.6;"></div>
          </div>
          <span style="width:50px; text-align:right; color:${color}">${d.total_lines}L</span>
          <span style="width:16px; color:${color}">${icon}</span>
        </div>`;
      }
      html += '</div></div>';
    }

    // Structure checks
    const struct = instData.structure;
    if (struct && struct.checks) {
      const checks = struct.checks;
      let pass = 0, warn = 0, fail = 0, info = 0;
      const icons = { pass: '✓', warn: '⚠', fail: '✗', info: 'ℹ' };

      html += '<div class="audit-section"><h2>Audit checks <i class=\"info-icon\">i<span class=\"info-tip\">Protocol (PS/PA/PF), artifact (AN/AR/AF), and instance (IS/IN/IR) conformity checks. Pass = conformant, warn = minor issue, fail = violation.</span></i></h2></div>';
      html += '<div class="checks-grid">';
      const prefixLabels = { PS: 'Protocol — Structure', PP: 'Protocol — Personas', PA: 'Protocol — Artifacts', PF: 'Protocol — Format', IS: 'Instance — Structure', IN: 'Instance — Naming', AN: 'Artifact — Notes', AR: 'Artifact — Reviews', AF: 'Artifact — Features', AD: 'Artifact — ADR', IR: 'Instance — Roadmap' };
      const prefixOrder = ['PS', 'PP', 'PA', 'PF', 'IS', 'IN', 'AN', 'AR', 'AF', 'AD', 'IR'];
      const sortedChecks = [...checks].sort((a, b) => {
        const pa = a.id.replace(/[0-9]+.*$/, '');
        const pb = b.id.replace(/[0-9]+.*$/, '');
        const ia = prefixOrder.indexOf(pa); const ib = prefixOrder.indexOf(pb);
        if (ia !== ib) return (ia === -1 ? 99 : ia) - (ib === -1 ? 99 : ib);
        return a.id.localeCompare(b.id);
      });
      window._auditChecks = sortedChecks;
      let lastPrefix = '';
      for (let ci = 0; ci < sortedChecks.length; ci++) {
        const chk = sortedChecks[ci];
        const status = chk.status || 'info';
        if (status === 'pass') pass++;
        else if (status === 'warn') warn++;
        else if (status === 'fail') fail++;
        else info++;
        const prefix = chk.id.replace(/[0-9]+.*$/, '');
        if (prefix !== lastPrefix) {
          html += `<div class="check-group-title">${prefixLabels[prefix] || prefix}</div>`;
          lastPrefix = prefix;
        }
        const clickable = (status === 'warn' || status === 'fail');
        const dataAttr = clickable ? ` data-chk-idx="${ci}"` : '';
        const arrow = clickable ? ' <span style="opacity:0.3;font-size:9px">▸</span>' : '';
        html += `<div class="check-item ${status}"${dataAttr}><span class="icon">${icons[status] || '?'}</span><span class="msg"><strong>${chk.id}</strong> — ${chk.detail || chk.message || ''}${arrow}</span></div>`;
      }
      html += '</div>';

      html += `<div class="audit-summary">
        <span class="stat pass">${pass} pass</span>
        <span class="stat warn">${warn} warn</span>
        <span class="stat fail">${fail} fail</span>
        <span class="stat info">${info} info</span>
      </div>`;
    }

    // Friction PO table
    const fpo = instData.friction_po;
    if (fpo && fpo.by_persona) {
      html += '<div class="audit-section"><h2>Orchestrator friction <i class=\"info-icon\">i<span class=\"info-tip\">Friction markers from session summaries. Breakdown by persona: markers, resolutions, initiative (persona vs PO), reportPattern triggers.</span></i></h2>';
      html += '<div class="table-card"><table><thead><tr>';
      html += '<th>Persona</th><th>Sessions</th><th>w/ friction</th>';
      html += '<th style="color:var(--done)">Sound</th><th>Contest.</th><th style="color:var(--amber)">Simpl.</th><th style="color:var(--coral)">Blind sp.</th><th style="color:var(--coral)">Refuted</th>';
      html += '<th style="color:var(--done)">Ratified</th><th style="color:var(--amber)">Contested</th><th style="color:var(--violet)">Revised</th><th style="color:var(--coral)">Rejected</th><th>No-res</th>';
      html += '<th>Init.P</th><th>Init.PO</th><th>SP</th>';
      html += '</tr></thead><tbody>';
      for (const [p, d] of Object.entries(fpo.by_persona).sort()) {
        html += `<tr>
          <td>${p}</td><td>${d.total_sessions}</td><td>${d.sessions_with_friction}</td>
          <td>${d.sound||0}</td><td>${d.contestable||0}</td><td>${d.simplification||0}</td><td>${d.blind_spot||0}</td><td>${d.refuted||0}</td>
          <td>${d.resolution_ratified||0}</td><td>${d.resolution_contested||0}</td><td>${d.resolution_revised||0}</td><td>${d.resolution_rejected||0}</td><td>${d.resolution_missing||0}</td>
          <td>${d.initiative_persona||0}</td><td>${d.initiative_po||0}</td><td>${d.signaler_pattern_count||0}</td>
        </tr>`;
      }
      html += '</tbody></table></div></div>';
    }

    // Activity
    const act = instData.activite;
    if (act && act.by_persona) {
      html += '<div class="audit-section"><h2>Activity <i class=\"info-icon\">i<span class=\"info-tip\">Number of sessions per persona. A persona with zero sessions is inactive.</span></i></h2>';
      html += '<div class="table-card"><table><thead><tr><th>Persona</th><th>Sessions</th></tr></thead><tbody>';
      const sorted = Object.entries(act.by_persona).sort((a,b) => b[1] - a[1]);
      for (const [p, count] of sorted) {
        html += `<tr><td>${p}</td><td>${count}</td></tr>`;
      }
      html += `<tr style="border-top:1px solid var(--border-hi)"><td><strong>Total</strong></td><td><strong>${act.meta?.total_sessions || '—'}</strong></td></tr>`;
      html += '</tbody></table></div></div>';
    }

    // Exchange matrix (simplified — top flows only)
    const ech = instData.echanges;
    if (ech && ech.matrix) {
      const flows = [];
      for (const [from, targets] of Object.entries(ech.matrix)) {
        for (const [to, count] of Object.entries(targets)) {
          if (count > 0 && from !== to) flows.push({ from, to, count });
        }
      }
      flows.sort((a,b) => b.count - a.count);
      if (flows.length > 0) {
        html += '<div class="audit-section"><h2>Exchange flow (top) <i class=\"info-icon\">i<span class=\"info-tip\">Top artefact flows between personas — who sends to whom, ranked by volume.</span></i></h2>';
        html += '<div class="table-card"><table><thead><tr><th>De</th><th>Pour</th><th>Artefacts</th></tr></thead><tbody>';
        for (const f of flows.slice(0, 15)) {
          html += `<tr><td>${f.from}</td><td>${f.to}</td><td>${f.count}</td></tr>`;
        }
        html += '</tbody></table></div></div>';
      }
    }

  }

  container.innerHTML = html;
}
