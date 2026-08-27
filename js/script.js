const statusMeta = {
  interested:  { color: '#4a7a96', label: 'Interested' },
  shortlisted: { color: '#c98a2c', label: 'Shortlisted' },
  applied:     { color: '#6f5aa6', label: 'Applied' },
  accepted:    { color: '#3f8a5c', label: 'Accepted' },
  rejected:    { color: '#b0473f', label: 'Rejected' }
};

// --- Map setup ---
const map = L.map('map', { worldCopyJump: true }).setView([20, 10], 2);

L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; CartoDB'
}).addTo(map);

// --- Legend (HIDDEN) ---
function buildLegend() {
  const legend = document.getElementById('legend');
  legend.style.display = 'none';
  legend.innerHTML = '';
}

function makeIcon(status) {
  const color = (statusMeta[status] && statusMeta[status].color) || statusMeta.interested.color;
  return L.divIcon({
    className: '',
    html: `<div style="background:${color};width:16px;height:16px;border-radius:50%;border:2px solid #fff;box-shadow:0 0 4px rgba(0,0,0,0.45);"></div>`,
    iconSize: [16, 16],
    iconAnchor: [8, 8]
  });
}

function listSection(title, items) {
  if (!items || items.length === 0) {
    return `<h3>${title}</h3><p class="empty-note">Nothing added yet</p>`;
  }
  const lis = items.map(i => {
    let text = `<strong>${escapeHtml(i.name)}</strong>`;
    if (i.link && i.link !== "") {
      text += ` — <a href="${escapeHtml(i.link)}" target="_blank" rel="noopener">🔗 Link</a>`;
    }
    if (i.note && i.note !== "") {
      text += ` (${escapeHtml(i.note)})`;
    }
    return `<li>${text}</li>`;
  }).join('');
  return `<h3>${title}</h3><ul>${lis}</ul>`;
}

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

function showSidebar(uni) {
  const sidebar = document.getElementById('sidebar');
  const content = document.getElementById('sidebar-content');
  const meta = statusMeta[uni.status] || statusMeta.interested;

  content.innerHTML = `
    <span class="badge status-${uni.status || 'interested'}">${meta.label}</span>
    <h2>${escapeHtml(uni.name)}</h2>
    <p class="country">${escapeHtml(uni.country || '')}</p>
    ${uni.website ? `<p><a href="${uni.website}" target="_blank" rel="noopener">Visit website ↗</a></p>` : ''}
    ${uni.notes ? `<div class="notes">${escapeHtml(uni.notes)}</div>` : ''}
    ${listSection('Professors / Collaborators', uni.professors)}
    ${listSection('Papers', uni.papers)}
    ${listSection('Conferences', uni.conferences)}
    ${listSection('Scholarships', uni.scholarships)}
  `;
  sidebar.classList.remove('hidden');
}

document.getElementById('close-sidebar').addEventListener('click', () => {
  document.getElementById('sidebar').classList.add('hidden');
});

buildLegend();

fetch('data/universities.json')
  .then(res => res.json())
  .then(universities => {
    universities.forEach(uni => {
      const marker = L.marker([uni.lat, uni.lng], { icon: makeIcon(uni.status) }).addTo(map);
      marker.bindTooltip(uni.name, { direction: 'top', offset: [0, -8] });
      marker.on('click', () => showSidebar(uni));
    });
  })
  .catch(err => {
    console.error('Could not load data/universities.json', err);
    alert('Could not load university data. Make sure data/universities.json exists and is valid JSON.');
  });