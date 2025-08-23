(function () {
  function qs(id) {
    return document.getElementById(id);
  }

  function setup() {
    const root = qs('profile-root');
    if (!root) return;

    const btnUsername = qs('btn-username');
    const btnPassword = qs('btn-password');
    const btnLogout = qs('btn-logout')
    const panelUsername = qs('panel-username');
    const panelPassword = qs('panel-password');
    const panelLogout = qs('panel-logout');

    if (!btnUsername || !btnPassword || !panelUsername || !panelPassword) return;

    function showPanel(name) {
      const isUser = name === 'username';
      panelUsername.classList.toggle('active', isUser);
      panelPassword.classList.toggle('active', !isUser && !(name === 'logout'));
      panelLogout.classList.toggle('active', (name === 'logout'));
      const input = (isUser ? panelUsername : panelPassword).querySelector('input');
      if (input) setTimeout(() => input.focus(), 0);
    }

    btnUsername.addEventListener('click', () => showPanel('username'));
    btnPassword.addEventListener('click', () => showPanel('password'));
    btnLogout.addEventListener('click', () => showPanel('logout'));

    const active = (root.dataset && root.dataset.active) ? root.dataset.active : '';
    if (active === 'username') showPanel('username');
    else if (active === 'password') showPanel('password');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setup);
  } else {
    setup();
  }
})();