(() => {
  const btnScout   = document.getElementById('btn-scout');
  const selIndustry = document.getElementById('industry');
  const selRegion   = document.getElementById('region');
  const statusBar  = document.getElementById('status-bar');
  const statusText = document.getElementById('status-text');
  const grid       = document.getElementById('results-grid');
  const emptyState = document.getElementById('empty-state');
  const cardTpl    = document.getElementById('card-tpl');

  let source    = null;
  let streamDone = false;

  // ── Scout button ──────────────────────────────────────────────────────
  btnScout.addEventListener('click', () => {
    if (source) {
      source.close();
      source = null;
    }

    // Reset UI
    grid.innerHTML = '';
    emptyState.classList.add('hidden');
    statusBar.classList.remove('hidden');
    statusText.textContent = 'Connecting…';
    btnScout.disabled = true;
    streamDone = false;

    const params = new URLSearchParams({
      industry: selIndustry.value,
      region:   selRegion.value,
    });

    source = new EventSource(`/search?${params}`);

    // ── Event handlers ──────────────────────────────────────────────────

    source.addEventListener('status', (e) => {
      statusText.textContent = JSON.parse(e.data).text;
    });

    source.addEventListener('company', (e) => {
      emptyState.classList.add('hidden');
      grid.appendChild(buildCard(JSON.parse(e.data)));
    });

    source.addEventListener('warning', (e) => {
      console.warn('[LeadScout]', JSON.parse(e.data).text);
    });

    source.addEventListener('error', (e) => {
      streamDone = true;
      statusText.textContent = `Error: ${JSON.parse(e.data).text}`;
      finish();
    });

    source.addEventListener('done', (e) => {
      streamDone = true;
      statusText.textContent = JSON.parse(e.data).text;
      if (grid.childElementCount === 0) emptyState.classList.remove('hidden');
      finish();
    });

    // Connection-level error (server unreachable / stream dropped)
    source.onerror = () => {
      if (streamDone) return;
      statusText.textContent = 'Stream connection lost.';
      finish();
    };
  });

  function finish() {
    if (source) { source.close(); source = null; }
    btnScout.disabled = false;
  }

  // ── Build card from template ──────────────────────────────────────────
  function buildCard(data) {
    const frag = cardTpl.content.cloneNode(true);
    const card = frag.querySelector('.card');

    // Score tier
    const score = data.score ?? 0;
    card.dataset.score = score >= 8 ? 'high' : score >= 6 ? 'mid' : 'low';

    // Company
    card.querySelector('.company-name').textContent = data.name ?? '';

    const domainEl = card.querySelector('.company-domain');
    domainEl.textContent = data.domain ?? '';
    domainEl.href = data.domain ? `https://${data.domain}` : '#';

    // Badges
    card.querySelector('.score-badge').textContent  = `${score}/10`;
    card.querySelector('.region-badge').textContent = data.region ?? '';

    // Fit reason
    card.querySelector('.fit-reason').textContent = data.fit_reason ?? '';

    // Signals
    const signalsList = card.querySelector('.signals');
    (data.signals ?? []).forEach((sig) => {
      const li = document.createElement('li');
      li.textContent = sig;
      signalsList.appendChild(li);
    });

    // Contact
    const contact = data.contact ?? {};
    card.querySelector('.contact-name').textContent = contact.name  ?? '';
    card.querySelector('.contact-role').textContent = contact.title ?? '';

    const emailEl = card.querySelector('.contact-email');
    const email   = contact.email ?? '';
    if (email.includes('linkedin.com')) {
      emailEl.textContent      = 'No direct email found';
      emailEl.removeAttribute('href');
    } else if (email) {
      emailEl.textContent = email;
      emailEl.href        = `mailto:${email}`;
    } else {
      emailEl.textContent      = '';
      emailEl.removeAttribute('href');
    }

    // Email draft
    const draft = data.email_draft ?? '';
    card.querySelector('.email-draft').textContent = draft;

    // Copy button
    const btnCopy = card.querySelector('.btn-copy');
    btnCopy.addEventListener('click', () => {
      navigator.clipboard.writeText(draft).then(() => {
        btnCopy.textContent = 'Copied ✓';
        btnCopy.classList.add('copied');
        setTimeout(() => {
          btnCopy.textContent = 'Copy';
          btnCopy.classList.remove('copied');
        }, 2000);
      });
    });

    // Dismiss button
    card.querySelector('.btn-dismiss').addEventListener('click', () => {
      card.classList.add('dismissed');
      setTimeout(() => card.remove(), 270);
    });

    return card;
  }
})();
