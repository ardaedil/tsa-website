"""Check generated pages, local assets/links, and the supplied board roster."""
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
PAGES = ['index.html', 'board.html', 'events.html', 'newsletter.html', 'join.html']


class Page(HTMLParser):
    def __init__(self, name):
        super().__init__(convert_charrefs=True)
        self.name = name
        self.ids = set()
        self.refs = []
        self.labels = []
        self.h1s = 0
        self.members = 0
        self.active = []
        self.payload = ''
        self.in_payload = False

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f'{self.name}: duplicate id {attrs["id"]}'
            self.ids.add(attrs['id'])
        for key in ('src', 'href'):
            if attrs.get(key):
                self.refs.append(attrs[key])
        if tag == 'label':
            self.labels.append(attrs.get('for'))
        if tag == 'h1':
            self.h1s += 1
        if tag == 'article' and attrs.get('class') == 'board-member':
            self.members += 1
        if attrs.get('aria-current') == 'page':
            self.active.append(attrs.get('href'))
        if tag == 'script' and attrs.get('id') == 'site-content':
            self.in_payload = True

    def handle_endtag(self, tag):
        if tag == 'script':
            self.in_payload = False

    def handle_data(self, data):
        if self.in_payload:
            self.payload += data


pages = {}
for name in PAGES:
    page = Page(name)
    page.feed((ROOT / name).read_text(encoding='utf-8'))
    assert page.h1s == 1, f'{name}: expected one main heading'
    assert page.active == [name], f'{name}: incorrect active navigation'
    assert all(label in page.ids for label in page.labels), f'{name}: unmatched form label'
    json.loads(page.payload)
    pages[name] = page

references = 0
for name, page in pages.items():
    for reference in page.refs:
        url = urlsplit(reference)
        if url.scheme or url.netloc:
            assert url.scheme in ('https', 'mailto'), f'{name}: unexpected URL scheme'
            continue
        path = unquote(url.path) or name
        assert (ROOT / path).is_file(), f'{name}: missing local target {path}'
        if url.fragment and path in pages:
            assert unquote(url.fragment) in pages[path].ids, f'{name}: missing fragment {reference}'
        references += 1

roster = json.loads((ROOT / 'data/site.json').read_text(encoding='utf-8'))['board']
assert pages['board.html'].members == 9, 'Expected all nine authorized board members'
board_html = (ROOT / 'board.html').read_text(encoding='utf-8')
for member in roster:
    assert f'mailto:{member["email"]}' in board_html, f'Missing board email: {member["name"]}'
assert [member['name'].split()[-1] for member in roster] == sorted(member['name'].split()[-1] for member in roster), 'Roster must be alphabetical by last name'
print(f'Checked {len(pages)} pages, {references} local references, form labels, issue data, and all 9 board members.')
