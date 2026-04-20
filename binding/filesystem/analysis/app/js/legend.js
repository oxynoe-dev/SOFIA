// ── Legend ──

function legendScroll(e) {
  e.preventDefault();
  const id = e.target.getAttribute('href').slice(1);
  const el = document.getElementById(id);
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

let legendLoaded = false;
function loadLegend() {
  if (legendLoaded) return;
  fetch('legend.html').then(r => {
    if (!r.ok) throw new Error(r.status);
    return r.text();
  }).then(html => {
    document.getElementById('legend-content').innerHTML = html;
    legendLoaded = true;
  }).catch(() => {
    document.getElementById('legend-content').innerHTML = '<p style="color:var(--coral)">Could not load legend.html — run: python3 data/build_legend.py</p>';
  });
}

function renderMarkdown(md) {
  const lines = md.split('\n');
  let html = '';
  let inTable = false;
  let inList = false;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const trimmed = line.trim();

    if (trimmed === '---' && i < 5) continue;

    if (trimmed.startsWith('# ')) {
      if (inTable) { html += '</tbody></table>'; inTable = false; }
      if (inList) { html += '</ul>'; inList = false; }
      html += '<h1 style="font-family:var(--font-display); font-size:28px; font-weight:300; color:var(--ice); margin:2rem 0 1rem;">' + trimmed.slice(2) + '</h1>';
    } else if (trimmed.startsWith('## ')) {
      if (inTable) { html += '</tbody></table>'; inTable = false; }
      if (inList) { html += '</ul>'; inList = false; }
      html += '<h2 id="' + trimmed.slice(3).toLowerCase().replace(/[^a-z0-9]+/g,'-') + '">' + trimmed.slice(3) + '</h2>';
    } else if (trimmed.startsWith('### ')) {
      if (inTable) { html += '</tbody></table>'; inTable = false; }
      if (inList) { html += '</ul>'; inList = false; }
      html += '<h3>' + trimmed.slice(4) + '</h3>';
    }
    else if (trimmed.startsWith('|')) {
      const cells = trimmed.split('|').slice(1, -1).map(c => c.trim());
      if (cells.every(c => /^[-:]+$/.test(c))) continue;
      if (!inTable) {
        if (inList) { html += '</ul>'; inList = false; }
        html += '<table style="margin:1rem 0; font-size:13px;"><thead><tr>';
        cells.forEach(c => html += '<th>' + inlineFormat(c) + '</th>');
        html += '</tr></thead><tbody>';
        inTable = true;
      } else {
        html += '<tr>';
        cells.forEach(c => html += '<td>' + inlineFormat(c) + '</td>');
        html += '</tr>';
      }
    }
    else if (trimmed.startsWith('- ')) {
      if (inTable) { html += '</tbody></table>'; inTable = false; }
      if (!inList) { html += '<ul style="margin:.5rem 0 .5rem 1.5rem;">'; inList = true; }
      html += '<li>' + inlineFormat(trimmed.slice(2)) + '</li>';
    }
    else if (trimmed === '') {
      if (inTable) { html += '</tbody></table>'; inTable = false; }
      if (inList) { html += '</ul>'; inList = false; }
    }
    else {
      if (inTable) { html += '</tbody></table>'; inTable = false; }
      if (inList) { html += '</ul>'; inList = false; }
      html += '<p style="margin:.5rem 0;">' + inlineFormat(trimmed) + '</p>';
    }
  }
  if (inTable) html += '</tbody></table>';
  if (inList) html += '</ul>';
  return html;
}

function inlineFormat(s) {
  return s
    .replace(/\*\*(.+?)\*\*/g, '<strong style="color:var(--ice)">$1</strong>')
    .replace(/`(.+?)`/g, '<code style="font-family:var(--font-mono); font-size:12px; background:rgba(64,180,160,0.06); padding:1px 4px; border-radius:2px;">$1</code>');
}
