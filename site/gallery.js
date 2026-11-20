const gallery = document.querySelector('.gallery-nav');
const tabs = [...gallery.querySelectorAll('[data-view]')];
const image = document.querySelector('#gallery-image');
const pictureButton = document.querySelector('.gallery-image');
const title = document.querySelector('#view-title');
const note = document.querySelector('#view-note');
const dialog = document.querySelector('#capture-dialog');

function show(tab) {
  const label = tab.dataset.title;
  for (const option of tabs) {
    if (option === tab) option.setAttribute('aria-current', 'true');
    else option.removeAttribute('aria-current');
  }
  image.src = tab.href;
  pictureButton.href = tab.href;
  image.alt = 'SIGNAL ' + label + ' workspace populated with fictional examples.';
  pictureButton.setAttribute('aria-label', 'Enlarge ' + label + ' screenshot');
  title.textContent = label;
  note.textContent = tab.dataset.note;
}

for (const tab of tabs) {
  tab.addEventListener('click', event => {
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    show(tab);
  });
}

pictureButton.addEventListener('click', event => {
  if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || !dialog.showModal) return;
  event.preventDefault();
  const enlarged = dialog.querySelector('img');
  enlarged.src = image.src;
  enlarged.alt = image.alt;
  dialog.querySelector('#capture-title').textContent = title.textContent + ' screenshot';
  dialog.showModal();
  dialog.querySelector('button').focus();
});
dialog.querySelector('#close-capture').addEventListener('click', () => dialog.close());
dialog.addEventListener('close', () => pictureButton.focus());
