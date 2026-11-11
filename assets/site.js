const content = JSON.parse(document.getElementById('site-content').textContent);
const dialog = document.getElementById('content-dialog');
const dialogTitle = document.getElementById('dialog-title');
const dialogBody = document.getElementById('dialog-body');
const dialogLabel = document.getElementById('dialog-label');
let dialogTrigger = null;

function openDialog(trigger, title, label) {
  dialogTrigger = trigger;
  dialogTitle.textContent = title;
  dialogLabel.textContent = label;
  dialogBody.replaceChildren();
  dialog.showModal();
  document.body.classList.add('dialog-open');
}

function paragraph(text, className) {
  const element = document.createElement('p');
  element.textContent = text;
  if (className) element.className = className;
  return element;
}

document.querySelectorAll('[data-album]').forEach(button => {
  button.addEventListener('click', () => {
    const event = content.events.find(item => item.id === button.dataset.album);
    if (!event) return;
    openDialog(button, event.title, event.sample ? 'Sample photo album' : event.date);
    dialogBody.append(paragraph(event.summary, 'dialog-note'));
    const grid = document.createElement('div');
    grid.className = event.photos.length === 1 ? 'album-grid is-single' : 'album-grid';
    if (event.photos.length) {
      for (const [index, photo] of event.photos.entries()) {
        const link = document.createElement('a');
        link.href = photo.src;
        link.target = '_blank';
        link.rel = 'noopener';
        link.className = 'album-image-link';
        link.setAttribute('aria-label', `Open full photograph ${index + 1} in a new tab`);
        const image = document.createElement('img');
        image.className = 'photo';
        image.src = photo.src;
        image.alt = photo.alt;
        image.loading = 'lazy';
        link.append(image);
        grid.append(link);
      }
    } else {
      dialogBody.append(paragraph('Photographs will be added here. These frames show the planned album layout.', 'dialog-note'));
      for (let index = 1; index <= 6; index++) {
        const frame = document.createElement('div');
        frame.className = 'photo-placeholder';
        const label = document.createElement('span');
        label.className = 'photo-label';
        label.textContent = `Photo ${String(index).padStart(2, '0')} placeholder`;
        frame.append(label);
        grid.append(frame);
      }
    }
    dialogBody.append(grid);
  });
});

document.querySelectorAll('[data-issue]').forEach(button => {
  button.addEventListener('click', () => {
    const issue = content.newsletters.find(item => item.id === button.dataset.issue);
    if (!issue) return;
    openDialog(button, issue.title, issue.date);
    const reader = document.createElement('article');
    reader.className = 'reader';
    for (const text of issue.paragraphs) reader.append(paragraph(text));
    dialogBody.append(reader);
  });
});

document.getElementById('close-dialog').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', event => {
  if (event.target !== dialog) return;
  const bounds = dialog.getBoundingClientRect();
  if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) dialog.close();
});
dialog.addEventListener('close', () => {
  document.body.classList.remove('dialog-open');
  dialogTrigger?.focus();
});

const contactForm = document.getElementById('contact-form');
const topic = document.getElementById('contact-topic');
if (topic && new URLSearchParams(location.search).get('topic') === 'joining') topic.value = 'joining';

function emailDraft(subject, body) {
  location.href = `mailto:${content.contactEmail}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
}

contactForm?.addEventListener('submit', event => {
  event.preventDefault();
  if (!contactForm.reportValidity()) return;
  const fields = new FormData(contactForm);
  const topics = { joining: 'Joining TSA', question: 'A question for TSA', collaboration: 'Collaboration with TSA', other: 'Hello TSA' };
  emailDraft(topics[fields.get('topic')] || 'Hello TSA', `Name: ${fields.get('name')}\nReply email: ${fields.get('email')}\n\n${fields.get('message')}`);
  document.getElementById('contact-status').textContent = 'Email draft requested. If your email app opens, review the draft and send it there. If it does not open, use the direct email link alongside this form.';
});

document.getElementById('newsletter-form')?.addEventListener('submit', event => {
  event.preventDefault();
  const form = event.currentTarget;
  if (!form.reportValidity()) return;
  const email = new FormData(form).get('email');
  emailDraft('TSA newsletter signup request', `Merhaba TSA,\n\nI would like to receive the weekly newsletter at ${email}.\n\nThank you!`);
  document.getElementById('newsletter-status').textContent = 'Email draft requested. Send it from your email app to request newsletter signup. You are not subscribed automatically.';
});
