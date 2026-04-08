// ── Mobile nav toggle ──
const toggle = document.querySelector('.nav-toggle');
const navLinks = document.querySelector('.nav-links');
if (toggle && navLinks) {
  toggle.addEventListener('click', () => navLinks.classList.toggle('open'));
  document.addEventListener('click', e => {
    if (!e.target.closest('.nav')) navLinks.classList.remove('open');
  });
}

// ── Scroll fade-up animations ──
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.fade-up').forEach(el => observer.observe(el));

// ── Publication filters ──
const filterBtns = document.querySelectorAll('.filter-btn');
const pubItems = document.querySelectorAll('.pub-item');

filterBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    filterBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const filter = btn.dataset.filter;

    pubItems.forEach(item => {
      if (filter === 'all') {
        item.style.display = 'flex';
        return;
      }
      const tags = (item.dataset.tags || '').toLowerCase();
      const neuro = ['motor','neural','dynamical','jpc','epilepsy','eeg','cortex','brainstem','reticular','connectivity','electrophysiology'];
      const eng = ['iot','fpga','embedded','sensor','signal','instrumentation','cybersecurity'];
      const isNeuro = neuro.some(k => tags.includes(k));
      const isEng = eng.some(k => tags.includes(k));

      if (filter === 'neuroscience') item.style.display = isNeuro ? 'flex' : 'none';
      else if (filter === 'engineering') item.style.display = isEng ? 'flex' : 'none';
    });
  });
});

// ── Smooth active nav highlighting ──
const sections = document.querySelectorAll('section[id]');
const navAnchors = document.querySelectorAll('.nav-links a[href*="#"]');

const sectionObserver = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      navAnchors.forEach(a => {
        a.style.color = a.getAttribute('href').includes(entry.target.id)
          ? 'var(--accent)' : '';
      });
    }
  });
}, { threshold: 0.4 });

sections.forEach(s => sectionObserver.observe(s));
