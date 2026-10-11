const assert = require('node:assert/strict');
const test = require('node:test');
const { renderPublications } = require('../script.js');

const paper = overrides => ({
  title: 'A paper', authors: ['Fan Yang'], venue: 'A venue', year: 2026,
  ...overrides,
});

test('resource links identify their destination and do not duplicate a PDF', () => {
  for (const [url, label] of [
    ['https://example.com/paper', 'Paper'],
    ['https://doi.org/10.1234/example', 'DOI'],
    ['https://example.com/paper.pdf', 'PDF'],
  ]) {
    const html = renderPublications([paper({ link: url })]);
    assert.ok(html.includes(`aria-label="${label}: A paper">[${label}]</a>`));
  }
  const html = renderPublications([paper({
    link: 'https://example.com/paper.pdf', pdf: 'https://example.com/paper.pdf',
  })]);
  assert.equal((html.match(/class="blue-tag paper-resource"/g) || []).length, 1);
});

test('papers without a public URL have no fabricated resource links', () => {
  const html = renderPublications([paper({ link: null })]);
  assert.ok(html.includes('<span class="paper-title">A paper</span>'));
  assert.ok(!html.includes('<a '));
});

test('new source links and accessible labels are escaped and reject unsafe URLs', () => {
  const html = renderPublications([paper({
    title: 'A "quoted" <paper>', link: 'https://example.com/?x=1&y=2',
    ccfLabel: 'CCF-A', ccfSource: 'https://example.com/ratings',
  })]);
  assert.ok(html.includes('aria-label="Paper: A &quot;quoted&quot; &lt;paper&gt;"'));
  assert.ok(html.includes('href="https://example.com/?x=1&amp;y=2"'));
  assert.ok(html.includes('href="https://example.com/ratings"'));
  assert.throws(() => renderPublications([paper({
    ccfLabel: 'CCF-A', ccfSource: 'javascript:alert(1)',
  })]), /Invalid publication URL/);
});
