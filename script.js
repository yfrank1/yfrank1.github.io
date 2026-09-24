function renderPublications(papers, author = 'Fan Yang') {
  if (!Array.isArray(papers) || papers.length === 0) throw new Error('No publications found.');
  const escape = value => String(value).replace(/[&<>"']/g, char =>
    ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[char]));
  const cleanName = name => name.replace(/\s*\*+$/, '');
  const isLeadAuthor = paper => cleanName(paper.authors[0]) === author ||
    (paper.equalContribution || []).includes(author);
  const link = (url, text, className) => {
    if (!/^https?:\/\//.test(url)) throw new Error('Invalid publication URL.');
    return '<a href="' + escape(url) + '" target="_blank" rel="noopener noreferrer" class="' +
      className + '">' + escape(text) + '</a>';
  };
  const grouped = new Map();
  for (const paper of papers) {
    if ((paper.year !== null && !Number.isInteger(paper.year)) || !paper.title ||
        (paper.venue !== null && typeof paper.venue !== 'string') ||
        !Array.isArray(paper.authors) || !paper.authors.length ||
        !paper.authors.every(name => typeof name === 'string')) {
      throw new Error('Invalid publication record.');
    }
    if (!grouped.has(paper.year)) grouped.set(paper.year, []);
    grouped.get(paper.year).push(paper);
  }

  return [...grouped.keys()].sort((a, b) => a === null ? -1 : b === null ? 1 : b - a).map(year => {
    const items = [...grouped.get(year)]
      .sort((a, b) => Number(isLeadAuthor(b)) - Number(isLeadAuthor(a)))
      .map(paper => {
        const tag = paper.short ? '<strong class="paper-venue-tag">[' + escape(paper.short) + ']</strong>' : '';
        const title = paper.link
          ? link(paper.link, paper.title, 'paper-title')
          : '<span class="paper-title">' + escape(paper.title) + '</span>';
        const pdf = paper.pdf ? ' ' + link(paper.pdf, '[PDF]', 'blue-tag') : '';
        const code = paper.code ? ' ' + link(paper.code, '[Code]', 'blue-tag') : '';
        const authors = paper.authors.map(name => cleanName(name) === author
          ? '<strong class="highlight">' + escape(name) + '</strong>' : escape(name)).join(', ');
        const awardInline = paper.award && paper.award.length < 30
          ? ' (<strong class="award-inline"><em>' + escape(paper.award) + '</em></strong>)' : '';
        const awardBlock = paper.award && paper.award.length >= 30
          ? '<br><strong class="award"><em>' + escape(paper.award) + '</em></strong>' : '';
        const note = paper.note ? '<br><span class="paper-note">' + escape(paper.note) + '</span>' : '';
        return '<li><span class="paper-heading">' + tag + title + pdf + code + '</span>' +
          '<span class="authors">' + authors + '</span><br>' +
          '<span class="venue-full">' + escape([paper.venue, paper.year].filter(value => value !== null && value !== undefined).join(', ')) + awardInline + '</span>' +
          awardBlock + note + '</li>';
      }).join('\n');
    return '<h3>' + (year === null ? 'Accepted / Forthcoming' : year) + '</h3>\n<ul>\n' + items + '\n</ul>';
  }).join('\n');
}

// Use this same renderer in the browser and during the static build.
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { renderPublications };
  if (require.main === module) {
    const fs = require('node:fs');
    const path = require('node:path');
    const input = process.argv[2] || path.join(__dirname, 'papers/publications.json');
    process.stdout.write(renderPublications(JSON.parse(fs.readFileSync(input, 'utf8'))));
  }
} else if (typeof document !== 'undefined') {
  document.addEventListener('DOMContentLoaded', async () => {
    const container = document.getElementById('paper-list');
    if (!container) return;
    try {
      const response = await fetch('papers/publications.json');
      if (!response.ok) throw new Error('Publication data could not be loaded.');
      const papers = await response.json();
      container.innerHTML = renderPublications(papers);
      container.dataset.state = 'ready';
      container.dataset.count = String(papers.length);
    } catch (error) {
      console.error('Failed to load publications:', error);
      container.innerHTML = '<p class="paper-list-error">Publications are temporarily unavailable. ' +
        '<a href="https://storage.cs.tsinghua.edu.cn/~yf/" class="blue-tag">View my Tsinghua profile.</a></p>';
      container.dataset.state = 'error';
    }
  });
}
