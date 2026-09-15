// ══════════════════════════════════
//   LifeDrop — main.js
// ══════════════════════════════════

// ─── HAMBURGER MENU ───
const hamburger = document.getElementById('hamburger');
const navLinks  = document.getElementById('navLinks');
if (hamburger && navLinks) {
  hamburger.addEventListener('click', () => {
    navLinks.classList.toggle('open');
  });
}

// ─── SCROLL REVEAL ───
function revealOnScroll() {
  const els = document.querySelectorAll('.reveal');
  const windowH = window.innerHeight;
  els.forEach(el => {
    const rect = el.getBoundingClientRect();
    if (rect.top < windowH - 60) {
      el.classList.add('visible');
    }
  });
}
window.addEventListener('scroll', revealOnScroll);
window.addEventListener('load', revealOnScroll);

// ─── ANIMATED COUNTERS ───
function animateCounter(el, target, duration = 1800) {
  let start = 0;
  const step = target / (duration / 16);
  const timer = setInterval(() => {
    start += step;
    if (start >= target) {
      el.textContent = target.toLocaleString();
      clearInterval(timer);
    } else {
      el.textContent = Math.floor(start).toLocaleString();
    }
  }, 16);
}

function initCounters() {
  const counters = document.querySelectorAll('.stat-num[data-target]');
  counters.forEach(el => {
    const target = parseInt(el.getAttribute('data-target'), 10);
    if (!isNaN(target)) {
      animateCounter(el, target);
    }
  });
}

// Trigger counters when hero is visible
const heroStats = document.querySelector('.hero-stats');
if (heroStats) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        initCounters();
        observer.disconnect();
      }
    });
  }, { threshold: 0.3 });
  observer.observe(heroStats);
}

// ─── AUTO-DISMISS FLASH MESSAGES ───
setTimeout(() => {
  document.querySelectorAll('.flash').forEach(el => {
    el.style.transition = 'opacity 0.5s';
    el.style.opacity = '0';
    setTimeout(() => el.remove(), 500);
  });
}, 4000);

// ─── SMOOTH SCROLL FOR ANCHOR LINKS ───
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

// ─── FORM VALIDATION FEEDBACK ───
document.querySelectorAll('.donor-form input, .donor-form select, .donor-form textarea').forEach(input => {
  input.addEventListener('blur', () => {
    if (input.required && !input.value.trim()) {
      input.style.borderColor = '#e53935';
    } else {
      input.style.borderColor = '';
    }
  });
  input.addEventListener('input', () => {
    if (input.value.trim()) {
      input.style.borderColor = '#43a047';
    }
  });
});
