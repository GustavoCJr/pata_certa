// script.js (coloque em /static/script/script.js)
// incluir no layout com:
// <script src="{{ url_for('static', filename='script/script.js') }}" defer></script>

(async function verificarLogin() {
  const endpoint = (typeof ROUTE_API_LOGGED !== 'undefined')
    ? ROUTE_API_LOGGED
    : window.location.origin + '/api/logged';

  try {
    const res = await fetch(endpoint, { credentials: 'same-origin' });
    if (!res.ok) return console.warn('Erro ao consultar /api/logged:', res.status);

    const data = await res.json();

    const show = sel => document.querySelectorAll(sel).forEach(el => el.classList.remove('hidden'));
    const hide = sel => document.querySelectorAll(sel).forEach(el => el.classList.add('hidden'));

    if (data && data.logged) {
      show('.linksLogado');
      hide('.linksDeslogado');

      const userSpan = document.querySelector('#current-username');
      if (userSpan) userSpan.textContent = data.username || '';
    } else {
      show('.linksDeslogado');
      hide('.linksLogado');
    }
  } catch (err) {
    console.error('Erro ao verificar login:', err);
  }
})();

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("img.pet-img").forEach(img => {
    const fallback = "/static/images/silhueta.png";

    const src = img.getAttribute("src");

    if (!src || src.trim() === "") {
      img.src = fallback;
      return;
    }

    img.addEventListener("error", () => {
      if (img.src !== fallback) {
        img.src = fallback;
      }
    });
  });
});
