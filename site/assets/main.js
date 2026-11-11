// Mobile menu
const toggle = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navigation');
toggle.addEventListener('click', () => {
  const expanded = toggle.getAttribute('aria-expanded') !== 'true';
  toggle.setAttribute('aria-expanded', String(expanded));
  navigation.classList.toggle('is-open', expanded);
});
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
    toggle.setAttribute('aria-expanded', 'false');
    navigation.classList.remove('is-open');
    toggle.focus();
  }
});

// Light / dark switch. The choice is remembered in this browser.
const root = document.documentElement;
const themeButton = document.querySelector('.theme-toggle');
const showTheme = () => {
  const other = root.dataset.theme === 'light' ? 'Dark' : 'Light';
  themeButton.textContent = other;
  themeButton.setAttribute('aria-label', `Switch to ${other.toLowerCase()} theme`);
};
themeButton.hidden = false;
showTheme();
themeButton.addEventListener('click', () => {
  root.dataset.theme = root.dataset.theme === 'light' ? 'dark' : 'light';
  try { localStorage.setItem('theme', root.dataset.theme); } catch (e) {}
  showTheme();
});
