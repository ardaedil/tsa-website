"""Build the five static pages from data/site.json. Python standard library only."""
from html import escape
import json
from pathlib import Path
from urllib.parse import quote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / 'data/site.json').read_text(encoding='utf-8'))
NAV = [('index.html', 'Home'), ('board.html', 'Board'), ('events.html', 'Events'),
       ('newsletter.html', 'Newsletter'), ('join.html', 'Join & Contact')]


def e(value):
    return escape(str(value), quote=True)


def asset(source):
    """Allow local project assets and HTTPS images, never executable URL schemes."""
    parsed = urlsplit(source)
    if parsed.scheme:
        if parsed.scheme != 'https':
            raise ValueError(f'Images must use HTTPS or a local asset: {source}')
    elif parsed.netloc or source.startswith('/') or '..' in Path(source).parts:
        raise ValueError(f'Image must stay within the project: {source}')
    elif not (ROOT / source).is_file():
        raise ValueError(f'Missing image asset: {source}')
    return e(source)


def photo(source=None, label='Community photograph', extra=''):
    if source:
        return f'<img class="photo {extra}" src="{asset(source)}" alt="{e(label)}" loading="lazy">'
    return f'''<div class="photo-placeholder {extra}" role="img" aria-label="{e(label)} placeholder">
        <span class="photo-symbol" aria-hidden="true">＋</span><span class="photo-label">{e(label)}<br>Photo coming soon</span></div>'''


def button(href, text, light=False):
    return f'<a class="button{" button-light" if light else ""}" href="{e(href)}">{e(text)} <span aria-hidden="true">↗</span></a>'


def hero(kicker, title, description):
    return f'''<section class="hero"><div class="wrap hero-grid"><div><div class="eyebrow">{e(kicker)}</div>
    <h1>{title}</h1><div class="red-rule"></div></div><p>{e(description)}</p></div></section>'''


def signup():
    return f'''<section class="signup" aria-labelledby="signup-title"><div><h2 id="signup-title">Keep a little TSA close.</h2>
    <p>Request the weekly newsletter by email.</p></div><form id="newsletter-form" action="mailto:{e(DATA['contactEmail'])}" method="post" enctype="text/plain"><label for="newsletter-email">Email address</label>
    <div class="signup-fields"><input type="email" id="newsletter-email" name="email" placeholder="you@example.com" autocomplete="email" required>
    <button class="button" type="submit">Request signup <span aria-hidden="true">↗</span></button></div>
    <p class="help">Opens an email draft to the board. Send the draft to request signup.</p><p id="newsletter-status" class="help" role="status"></p>
    <noscript><p class="help"><a href="mailto:{e(DATA['contactEmail'])}?subject=TSA%20newsletter%20signup">Email the board to request signup.</a></p></noscript></form></section>'''


def event_card(event):
    sample = '<div class="sample-label">Sample event</div>' if event['sample'] else ''
    return f'''<article class="event-card">{photo(event['cover'], event['title'])}{sample}<h3>{e(event['title'])}</h3>
    <div class="meta">{e(event['date'])}</div><p>{e(event['summary'])}</p>
    <button class="text-link" type="button" data-album="{e(event['id'])}">Open photo album <span aria-hidden="true">↗</span></button></article>'''


def home():
    image = (f'<img class="home-photo" src="{asset(DATA["heroPhoto"])}" alt="The TSA community at Michigan">'
             if DATA['heroPhoto'] else '''<div class="home-poster"><div class="eyebrow">People make the place.</div>
             <div class="poster-type">Your<br>people.<br>Your<br>place.</div><span class="photo-caption">Community photograph coming soon</span></div>''')
    latest = DATA['newsletters'][0]
    return f'''<section class="hero home-hero"><div class="wrap home-grid"><div><div class="eyebrow">A little closer to home.</div>
    <h1>Rooted<br>in Türkiye.<br>Together<br>at Michigan.</h1><p>Culture travels with us. Connect with the Turkish Student Association at the University of Michigan.</p>
    {button('join.html', 'Find your community')}</div>{image}</div></section>
    <section class="section"><div class="wrap"><div class="eyebrow">Turkish roots. Michigan community.</div>
    <div class="home-paths"><article class="home-path"><h2>Meet the people.</h2><p>Get to know the nine members of our board.</p><a class="text-link" href="board.html">Meet your board ↗</a></article>
    <article class="home-path"><h2>Come together.</h2><p>Explore upcoming gatherings and moments from past events.</p><a class="text-link" href="events.html">Explore events ↗</a></article>
    <article class="home-path"><h2>Stay connected.</h2><p>Read the weekly newsletter and keep up with our community.</p><a class="text-link" href="newsletter.html">Read the weekly ↗</a></article></div></div></section>
    <section class="section tinted"><div class="wrap home-feature">{photo(None, 'Community gathering', 'on-tint')}<div><div class="eyebrow">The TSA Weekly</div>
    <h2>{e(latest['title'])}.</h2><div class="sample-label">Sample newsletter</div><p>{e(latest['summary'])}</p>{button('newsletter.html', 'Explore the newsletter')}</div></div></section>'''


def board():
    cards = []
    for member in DATA['board']:
        initials = member['name'].split()[0][0] + member['name'].split()[-1][0]
        portrait = (f'<img class="portrait" src="{asset(member["photo"])}" alt="{e(member["name"])}" loading="lazy">' if member['photo']
                    else f'<div class="portrait-placeholder" role="img" aria-label="Portrait of {e(member["name"])} coming soon"><span class="initials" aria-hidden="true">{e(initials)}</span><small>Portrait coming soon</small></div>')
        bio = f'<p class="member-bio">{e(member["bio"])}</p>' if member.get('bio') else ''
        cards.append(f'''<article class="board-member">{portrait}<h2>{e(member['name'])}</h2><div class="member-role">{e(member['role'])}</div>
        <a class="member-email" href="mailto:{e(member['email'])}">{e(member['email'])}</a>{bio}</article>''')
    return hero('The people behind TSA', 'Nine people.<br>One community.', 'Meet the board of the Turkish Student Association at the University of Michigan.') + f'''
    <section class="section"><div class="wrap"><div class="section-heading"><h2>Meet your board.</h2><p>Listed alphabetically by last name</p></div>
    <div class="board-grid">{''.join(cards)}</div><div class="bottom-note"><p>Have a question or an idea for TSA?</p>{button('join.html', 'Get in touch')}</div></div></section>'''


def events():
    upcoming = [event for event in DATA['events'] if event['upcoming']]
    past = [event for event in DATA['events'] if not event['upcoming']]
    featured = ''
    for event in upcoming:
        sample = '<span class="sample-label">Sample event · Details coming soon</span>' if event['sample'] else '<span class="sample-label">Up next</span>'
        subject = quote(f'Question about {event["title"]}')
        featured += f'''<article class="featured-event">{photo(event['cover'], event['title'])}<div>{sample}<h2>{e(event['title'])}</h2>
        <div class="meta">{e(event['date'])}<br>{e(event['location'])}</div><p>{e(event['summary'])}</p>
        {button(f'mailto:{DATA["contactEmail"]}?subject={subject}', 'Ask the board')}</div></article>'''
    if not upcoming:
        featured = '<p class="intro">New gatherings will be announced here. Check back soon.</p>'
    notice = '<p class="notice">The listings below are layout placeholders. Confirmed events, dates, and photographs will be added here.</p>' if any(item['sample'] for item in DATA['events']) else ''
    return hero('The moments that connect us', 'Come for the culture.<br>Stay for the company.', 'See what’s coming up, then look back at gatherings from our community.') + f'''
    <section class="section"><div class="wrap">{notice}{featured}<hr class="rule"><div class="section-heading"><h2>Good times, remembered.</h2><p>Past events &amp; photo albums</p></div>
    <div class="event-grid">{''.join(event_card(event) for event in past)}</div></div></section>'''


def newsletter():
    latest, *archive = DATA['newsletters']
    rows = []
    for index, issue in enumerate(archive):
        rows.append(f'''<article class="archive-row"><span class="archive-no" aria-hidden="true">{len(archive) - index:02d}</span><div><h3>{e(issue['title'])}</h3>
        <div class="meta">{e(issue['date'])}</div></div><button class="text-link" type="button" data-issue="{e(issue['id'])}" aria-label="Read {e(issue['title'])}">Read ↗</button></article>''')
    notice = '<p class="notice">These are sample editions. Published weekly newsletters will replace them.</p>' if any(item['sample'] for item in DATA['newsletters']) else ''
    return hero('The TSA Weekly', 'A little TSA.<br>Every week.', 'Upcoming gatherings, community updates, and a note from the board.') + f'''
    <section class="section"><div class="wrap">{notice}<article class="newsletter-feature"><div><div class="eyebrow">The featured letter</div><h2>{e(latest['title'])}.</h2>
    <div class="meta">{e(latest['date'])}</div><p>{e(latest['summary'])}</p><button class="button" type="button" data-issue="{e(latest['id'])}">Read the letter <span aria-hidden="true">↗</span></button></div>
    <div class="issue-poster"><div class="eyebrow">The TSA Weekly</div><div class="poster-type">From us.<br>To you.</div><small>Turkish roots.<br>Michigan community.</small></div></article>
    <hr class="rule"><div class="section-heading"><h2>Previously, in your inbox.</h2><p>The issue archive</p></div>{''.join(rows)}{signup()}</div></section>'''


def join():
    channels = f'<a href="mailto:{e(DATA["contactEmail"])}">{e(DATA["contactEmail"])}</a><p>{e(DATA["contactName"])} · President</p>'
    for key, label in [('instagramUrl', 'Instagram'), ('communityUrl', 'Community chat')]:
        if DATA.get(key):
            if not DATA[key].startswith('https://'):
                raise ValueError(f'{key} must use HTTPS')
            channels += f'<p><a href="{e(DATA[key])}" target="_blank" rel="noopener">{label} ↗</a></p>'
    return hero('Join & Contact', 'A new connection<br>starts with merhaba.', 'Looking for community at Michigan? Curious about Turkish culture? We’d love to hear from you.') + f'''
    <section class="section"><div class="wrap"><div class="section-heading"><h2>Find your way in.</h2><p>Meet people. Get involved. Stay connected.</p></div>
    <div class="join-paths"><article class="join-path"><div class="eyebrow">01 / Get involved</div><h2>Join the community.</h2><p>Introduce yourself to the board and ask about getting involved.</p><a class="text-link" href="join.html?topic=joining#contact-form">I'm interested in joining ↗</a></article>
    <article class="join-path"><div class="eyebrow">02 / Come say hello</div><h2>Meet us in person.</h2><p>Explore the gatherings that bring our community together.</p><a class="text-link" href="events.html">Explore events ↗</a></article>
    <article class="join-path"><div class="eyebrow">03 / Keep in touch</div><h2>Get the weekly.</h2><p>Catch up on community news and request the newsletter.</p><a class="text-link" href="newsletter.html#signup-title">Explore the newsletter ↗</a></article></div>
    <div class="contact-layout"><section><div class="sample-label">Say merhaba</div><h2>Let's start a conversation.</h2><p>Joining TSA, planning a collaboration, or have a question? Write a note to the board.</p>
    <form class="contact-form" id="contact-form" action="mailto:{e(DATA['contactEmail'])}" method="post" enctype="text/plain"><div class="field-row"><div class="field"><label for="contact-name">Your name</label><input id="contact-name" type="text" name="name" autocomplete="name" required maxlength="120"></div>
    <div class="field"><label for="contact-email">Email address</label><input id="contact-email" type="email" name="email" autocomplete="email" required maxlength="254"></div></div>
    <div class="field"><label for="contact-topic">What brings you here?</label><select id="contact-topic" name="topic"><option value="joining">I'd like to join TSA</option><option value="question" selected>I have a question</option><option value="collaboration">I'd like to collaborate</option><option value="other">Something else</option></select></div>
    <div class="field"><label for="contact-message">Your message</label><textarea id="contact-message" name="message" placeholder="Tell us a little about yourself or what you have in mind." required maxlength="1800"></textarea></div>
    <button class="button" type="submit">Open email draft <span aria-hidden="true">↗</span></button><p class="help">Opens your email app. Review and send the draft there to deliver your message.</p>
    <p class="help" id="contact-status" role="status"></p><noscript><p class="help">Please email <a href="mailto:{e(DATA['contactEmail'])}">{e(DATA['contactEmail'])}</a> directly.</p></noscript></form></section>
    <aside class="contact-aside"><h3>A good place to start.</h3><p>A few ways we can help you connect with TSA.</p>
    <details><summary>I'm interested in joining.</summary><p>Choose “I'd like to join TSA” in the form and introduce yourself. The board can share membership information and next steps.</p></details>
    <details><summary>I'd like to collaborate.</summary><p>Tell us about your organization, your idea, and any dates you have in mind.</p></details>
    <details><summary>I have an event question.</summary><p>Include the event name and your question so the board can point you in the right direction.</p></details>
    <div class="contact-channels"><div class="eyebrow">Prefer email?</div><p>Contact the board through:</p>{channels}</div></aside></div></div></section>'''


def document(filename, title, description, body):
    navigation = ''.join(f'<a href="{path}"' + (' aria-current="page"' if filename == path else '') + f'>{e(label)}</a>' for path, label in NAV)
    footer_nav = ''.join(f'<a href="{path}">{e(label)}</a>' for path, label in NAV)
    payload = json.dumps({'contactEmail': DATA['contactEmail'], 'events': DATA['events'], 'newsletters': DATA['newsletters']}, ensure_ascii=False).replace('<', '\\u003c')
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} | TSA at Michigan</title><meta name="description" content="{e(description)}"><meta name="theme-color" content="#00274c">
<meta property="og:title" content="{e(title)} | TSA at Michigan"><meta property="og:description" content="{e(description)}"><meta property="og:type" content="website">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/styles.css"><script src="assets/site.js" defer></script></head>
<body><a class="skip-link" href="#main">Skip to content</a><header class="site-header"><div class="wrap header-inner">
<a class="brand" href="index.html" aria-label="TSA at Michigan home"><span class="wordmark">TSA.</span><span class="brand-caption">Turkish Student Association<br>University of Michigan</span></a>
<button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-navigation">Menu</button><nav id="site-navigation" class="site-nav" aria-label="Main navigation">{navigation}</nav></div></header>
<main id="main">{body}</main><footer class="site-footer"><div class="wrap footer-inner"><div class="footer-brand"><span class="wordmark">TSA.</span><p>A home away from home.</p></div>
<div><nav class="footer-links" aria-label="Footer navigation">{footer_nav}<a href="constitution.pdf">Constitution (PDF)</a></nav><p class="footer-university">Turkish Student Association<br>University of Michigan · Ann Arbor</p></div></div></footer>
<dialog class="dialog" id="content-dialog" aria-labelledby="dialog-title"><div class="dialog-inner"><div class="dialog-header"><div><div id="dialog-label" class="sample-label"></div><h2 id="dialog-title"></h2></div><button class="close-button" id="close-dialog" type="button" autofocus>Close</button></div><div id="dialog-body"></div></div></dialog>
<noscript><p class="no-script wrap">JavaScript enables photo albums, newsletter readers, and email draft forms. You can still browse every page and email <a href="mailto:{e(DATA['contactEmail'])}">{e(DATA['contactEmail'])}</a> directly.</p></noscript>
<script type="application/json" id="site-content">{payload}</script></body></html>
'''


def validate_data():
    if len(DATA['board']) != len({member['email'] for member in DATA['board']}):
        raise ValueError('Duplicate board email')
    for member in DATA['board']:
        if not member['email'].endswith('@umich.edu'):
            raise ValueError('Check board email: ' + member['email'])
    for key in ('events', 'newsletters'):
        ids = [item['id'] for item in DATA[key]]
        if len(ids) != len(set(ids)):
            raise ValueError(f'Duplicate {key} identifier')
    if not DATA['newsletters']:
        raise ValueError('Add at least one newsletter or sample edition')


if __name__ == '__main__':
    validate_data()
    pages = [
        ('index.html', 'Turkish Student Association', 'Turkish roots. Michigan community. Connect with the Turkish Student Association at the University of Michigan.', home),
        ('board.html', 'Our Board', 'Meet the nine members of the Turkish Student Association board at the University of Michigan.', board),
        ('events.html', 'Events', 'Upcoming gatherings and past-event photo albums from the Turkish Student Association at Michigan.', events),
        ('newsletter.html', 'The TSA Weekly', 'Read the TSA weekly newsletter and request updates from our community.', newsletter),
        ('join.html', 'Join & Contact', 'Get involved with TSA, ask a question, or contact the Turkish Student Association board at Michigan.', join),
    ]
    for filename, title, description, render in pages:
        (ROOT / filename).write_text(document(filename, title, description, render()), encoding='utf-8')
    print(f'Built {len(pages)} pages with {len(DATA["board"])} board members.')
