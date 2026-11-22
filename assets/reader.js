(() => {
  const menu = document.querySelector('#menu');
  menu?.addEventListener('click', () => {
    const open = document.querySelector('aside').classList.toggle('open');
    menu.setAttribute('aria-expanded', String(open));
  });
  document.querySelector('#print')?.addEventListener('click', () => window.print());
  let printState = [];
  window.addEventListener('beforeprint', () => {
    printState = [...document.querySelectorAll('details')].map(panel => [panel, panel.open]);
    printState.forEach(([panel]) => {panel.open = true;});
  });
  window.addEventListener('afterprint', () => printState.forEach(([panel, open]) => {panel.open = open;}));
  document.querySelector('#solutions')?.addEventListener('click', (event) => {
    const panels = [...document.querySelectorAll('article details')];
    const open = panels.some(panel => !panel.open);
    panels.forEach(panel => {panel.open = open;});
    event.target.textContent = open ? 'Close solutions and code' : 'Open solutions and code';
  });
  document.querySelectorAll('.copybtn').forEach(button => button.addEventListener('click', async () => {
    const source = button.parentElement.querySelector('code').textContent;
    let copied = false;
    try {await navigator.clipboard.writeText(source); copied = true;} catch (_) {
      const field = document.createElement('textarea');
      field.value = source; document.body.append(field); field.select();
      copied = document.execCommand('copy'); field.remove();
    }
    button.textContent = copied ? 'Copied' : 'Copy failed';
    setTimeout(() => {button.textContent = 'Copy';}, 1500);
  }));
  const search = document.querySelector('#search');
  search?.addEventListener('input', () => {
    const query = search.value.toLowerCase().trim();
    const cards = [...document.querySelectorAll('.chapter-card')];
    cards.forEach(card => {card.hidden = !card.textContent.toLowerCase().includes(query);});
    document.querySelector('#search-status').textContent = `${cards.filter(card => !card.hidden).length} chapters shown`;
  });
})();
