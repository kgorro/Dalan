// Fast retrieval router. Same logic is mirrored in backend/router.py.
// Scores KB entries with IDF-weighted field matching plus keyword-phrase hits.
(function (root) {
  const STOP = new Set("a an the is are am i me my we you your to of in on at for and or do does did can could how what where when which who why it this that there be with from go get to near about any some please tell know want like ba ang sa ug ni nga ko mo".split(" "));

  function norm(s) {
    return s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "")
      .replace(/[^a-z0-9\s-]/g, " ").replace(/\s+/g, " ").trim();
  }
  function stem(t) {
    if (t.length > 4 && t.endsWith("es")) return t.slice(0, -2);
    if (t.length > 3 && t.endsWith("s")) return t.slice(0, -1);
    return t;
  }
  function toks(s) {
    return norm(s).split(/[\s-]+/).filter(t => t && !STOP.has(t)).map(stem);
  }

  function build(kb) {
    const docs = kb.entries.filter(e => e.id !== "fallback").map(e => ({
      e,
      title: new Set(toks(e.title)),
      kw: new Set(e.keywords.flatMap(toks)),
      q: new Set(e.questions.flatMap(toks)),
      phrases: e.keywords.map(norm).filter(k => k.includes(" ") || k.length >= 4),
    }));
    const df = new Map();
    docs.forEach(d => new Set([...d.title, ...d.kw, ...d.q]).forEach(t => df.set(t, (df.get(t) || 0) + 1)));
    const N = docs.length;
    const idf = t => Math.log(1 + N / (df.get(t) || N));
    const fallback = kb.entries.find(e => e.id === "fallback");
    return { docs, idf, fallback };
  }

  function score(index, query) {
    const qn = " " + norm(query) + " ";
    const qt = [...new Set(toks(query))];
    const wantsNorth = /\bnorth|amihanan\b/.test(qn), wantsSouth = /\bsouth|habagatan\b/.test(qn);
    const out = index.docs.map(d => {
      let s = 0;
      for (const t of qt) {
        const w = index.idf(t);
        if (d.kw.has(t)) s += 3 * w;
        else if (d.title.has(t)) s += 2 * w;
        else if (d.q.has(t)) s += 1 * w;
      }
      for (const p of d.phrases) if (p.includes(" ") && qn.includes(" " + p + " ")) s += 4;
      if (wantsNorth && d.e.region === "north") s += 1.5;
      if (wantsSouth && d.e.region === "south") s += 1.5;
      if (d.e.region === "north" && wantsSouth && !wantsNorth) s -= 2;
      if (d.e.region === "south" && wantsNorth && !wantsSouth) s -= 2;
      return { entry: d.e, score: s };
    }).sort((a, b) => b.score - a.score);
    return out;
  }

  // Routes: "kb" (confident, answer instantly), "llm" (some signal, a local LLM would compose
  // an answer from the top chunks), "fallback" (nothing relevant).
  function route(index, query, opts = {}) {
    const hi = opts.hi ?? 6, lo = opts.lo ?? 2.5;
    const ranked = score(index, query);
    const top = ranked[0];
    const second = ranked[1];
    const related = ranked.slice(1, 4).filter(r => r.score >= lo).map(r => r.entry);
    if (!top || top.score < lo) return { route: "fallback", entry: index.fallback, score: top ? top.score : 0, related: [] };
    const margin = second ? top.score - second.score : top.score;
    const routeName = top.score >= hi || margin >= 3 ? "kb" : "llm";
    return { route: routeName, entry: top.entry, score: top.score, related, context: ranked.slice(0, 3).map(r => r.entry) };
  }

  root.SugboRouter = { build, route, score, norm };
  if (typeof module !== "undefined") module.exports = root.SugboRouter;
})(typeof window !== "undefined" ? window : globalThis);
