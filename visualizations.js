// Assignment 3: two static visualizations of the SAME data (data.js, made by prepare_data.py).
// Both answer "Do aces win matches?". One is ethical, one is deceptive; the page shows them only as A and B.
// Change this one line to swap which letter is which.
const PANELS = { A: "deceptive", B: "ethical" };

const W = 620, H = 570;
const M = { left: 150, right: 70 };               // shared layout so neither chart looks more finished
const ROW = { top: 156, h: 52, pitch: 72 };
const FONT = "Inter, system-ui, -apple-system, 'Segoe UI', sans-serif";
const INK = "#1f2328", MUTED = "#5b626b", GRID = "#c9ccd0";
const f1 = d3.format(".1f"), f0 = d3.format(",");
const LABEL = { "1-2": "1–2 aces", "3-5": "3–5 aces", "6-9": "6–9 aces", "10+": "10+ aces" };

function frame(svg) {
  svg.attr("viewBox", [0, 0, W, H]).attr("width", W).attr("height", H).attr("font-family", FONT).attr("role", "img");
  svg.append("rect").attr("width", W).attr("height", H).attr("fill", "#fff").attr("stroke", "#d9dde1");
  return svg;
}
const text = (g, x, y, s, o = {}) => g.append("text").attr("x", x).attr("y", y)
  .attr("font-size", o.size || 14).attr("font-weight", o.weight || 400).attr("fill", o.fill || INK)
  .attr("text-anchor", o.anchor || "start").text(s);

// Axis, grid and bars are drawn the same way in both charts; only the choices below differ.
function axis(g, x, ticks, y, title) {
  g.append("line").attr("x1", x(ticks[0])).attr("x2", x(ticks.at(-1))).attr("y1", y).attr("y2", y).attr("stroke", GRID);
  ticks.forEach(t => {
    g.append("line").attr("x1", x(t)).attr("x2", x(t)).attr("y1", y).attr("y2", y + 6).attr("stroke", GRID);
    text(g, x(t), y + 24, t + "%", { size: 13, fill: MUTED, anchor: "middle" });
  });
  text(g, (x(ticks[0]) + x(ticks.at(-1))) / 2, y + 46, title, { size: 13, fill: MUTED, anchor: "middle" });
}

// ---------------------------------------------------------------- ETHICAL
function drawEthical(svg) {
  const g = frame(svg);
  const x = d3.scaleLinear([0, 100], [M.left, W - M.right]);
  text(g, 30, 44, "Do aces win matches?", { size: 26, weight: 800 });
  text(g, 30, 72, "Share of ATP matches won by the player who hit more aces,", { fill: MUTED });
  text(g, 30, 92, "grouped by how many more aces they hit. 2015–2024.", { fill: MUTED });
  text(g, 30, 140, "Extra aces hit", { size: 13, weight: 700, fill: MUTED });
  text(g, x(50), 140, "50% = coin flip", { size: 13, fill: MUTED, anchor: "middle" });

  DATA.bins.forEach((d, i) => {
    const y = ROW.top + i * ROW.pitch;
    text(g, 30, y + 22, LABEL[d.bin], { size: 17, weight: 700 });
    text(g, 30, y + 42, "n = " + f0(d.n), { size: 13, fill: MUTED });
    g.append("rect").attr("x", x(0)).attr("y", y).attr("width", x(d.pct) - x(0)).attr("height", ROW.h).attr("rx", 3).attr("fill", "#2f6f8f");
    text(g, x(d.pct) + 10, y + 33, f1(d.pct) + "%", { size: 21, weight: 800 });
  });
  const end = ROW.top + 3 * ROW.pitch + ROW.h;
  g.append("line").attr("x1", x(50)).attr("x2", x(50)).attr("y1", 148).attr("y2", end).attr("stroke", "#fff").attr("stroke-width", 5).attr("opacity", .9);
  g.append("line").attr("x1", x(50)).attr("x2", x(50)).attr("y1", 148).attr("y2", end).attr("stroke", INK).attr("stroke-width", 1.5).attr("stroke-dasharray", "5 4");
  axis(g, x, [0, 25, 50, 75, 100], end + 16, "Share of matches won by the player with more aces (%)");

  const a = DATA.audit;
  text(g, 30, 506, "This shows association, not cause: stronger servers both hit more aces and win more.", { size: 12, fill: MUTED });
  text(g, 30, 522, `${f0(a.analyzed)} of ${f0(a.total)} matches analyzed. Excluded: other surfaces (${a.other_surface}),`, { size: 12, fill: MUTED });
  text(g, 30, 538, `unfinished matches (${a.unfinished}), missing ace counts (${a.missing_aces}), tied ace counts (${f0(a.tied_aces)}).`, { size: 12, fill: MUTED });
  text(g, 30, 554, "Source: Jeff Sackmann, Tennis Abstract (CC BY-NC-SA 4.0).", { size: 12, fill: MUTED });
}

// ---------------------------------------------------------------- DECEPTIVE
// Every statement and label below is true. The misleading choices are:
//  1. The x-axis starts at 50% (labelled honestly), so bar LENGTH no longer matches win rate: 56.8% vs 72.3%
//     looks like a 3x difference instead of 1.3x.
//  2. A sequential colour ramp piles a second "it gets stronger" cue onto the same variable.
//  3. A skewed title and a relative-change callout ("27% more likely") that is true but inflates a 15-point gap.
//  4. Omitted: sample sizes, exclusions, the association-not-cause caution, and any 50% reference line.
function drawDeceptive(svg) {
  const g = frame(svg);
  const x = d3.scaleLinear([50, 75], [M.left, W - M.right]);
  const ramp = ["#a9d3c0", "#6fb89a", "#3f9a78", "#1d7a57"];
  text(g, 30, 44, "Do aces win matches? Hit more, win more.", { size: 26, weight: 800 });
  text(g, 30, 72, "Share of ATP matches won by the player who hit more aces,", { fill: MUTED });
  text(g, 30, 92, "grouped by how many more aces they hit. 2015–2024.", { fill: MUTED });
  text(g, 30, 140, "Extra aces hit", { size: 13, weight: 700, fill: MUTED });

  DATA.bins.forEach((d, i) => {
    const y = ROW.top + i * ROW.pitch;
    text(g, 30, y + 33, LABEL[d.bin], { size: 17, weight: 700 });
    g.append("rect").attr("x", x(50)).attr("y", y).attr("width", x(d.pct) - x(50)).attr("height", ROW.h).attr("rx", 3).attr("fill", ramp[i]);
    text(g, x(d.pct) + 10, y + 33, f1(d.pct) + "%", { size: 21, weight: 800 });
  });
  const end = ROW.top + 3 * ROW.pitch + ROW.h;
  axis(g, x, [50, 55, 60, 65, 70, 75], end + 16, "Share of matches won by the player with more aces (%)");

  const lo = DATA.bins[0].pct, hi = DATA.bins.at(-1).pct;
  text(g, 30, 514, `With 10+ extra aces, a player is ${Math.round(100 * (hi / lo - 1))}% more likely to win than with 1–2.`, { size: 14, weight: 700 });
  text(g, 30, 532, "More aces, more wins, on every court.", { size: 12, fill: MUTED });
  text(g, 30, 548, "Source: Jeff Sackmann, Tennis Abstract ATP match data, 2015–2024.", { size: 12, fill: MUTED });
}

const draw = { ethical: drawEthical, deceptive: drawDeceptive };
Object.entries(PANELS).forEach(([letter, kind]) => draw[kind](d3.select("#viz" + letter)));
