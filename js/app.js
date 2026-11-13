/* GoldSilverRate.pk – rate engine, hydration, calculator */
(function () {
  "use strict";

  var TOLA = 11.664;
  var R = null;

  function r0(x) { return Math.floor(x + 0.5); }
  function fmt(x) { return Math.round(x).toLocaleString("en-US"); }

  /* Metric engine – mirrors the build-time formulas exactly */
  function MET(key) {
    if (!R) return 0;
    var g = R.gold, s = R.silver;
    switch (key) {
      /* gold 24K */
      case "g24_s_t": return g["24k_tola_sell"];
      case "g24_b_t": return g["24k_tola_buy"];
      case "g24_s_g": return g["24k_tola_sell"] / TOLA;
      case "g24_s_10g": return g["24k_tola_sell"] / TOLA * 10;
      case "g24_b_g": return g["24k_tola_buy"] / TOLA;
      case "g24_b_10g": return g["24k_tola_buy"] / TOLA * 10;
      /* gold 22K / 21K / 18K */
      case "g22_s_t": return g["22k_tola_sell"];
      case "g22_s_g": return g["22k_tola_sell"] / TOLA;
      case "g22_s_10g": return g["22k_tola_sell"] / TOLA * 10;
      case "g22_b_t": return r0(g["24k_tola_buy"] * 22 / 24);
      case "g22_b_g": return g["24k_tola_buy"] * 22 / 24 / TOLA;
      case "g22_b_10g": return g["24k_tola_buy"] * 22 / 24 / TOLA * 10;
      case "g21_s_t": return g["21k_tola_sell"];
      case "g21_s_g": return g["21k_tola_sell"] / TOLA;
      case "g21_s_10g": return g["21k_tola_sell"] / TOLA * 10;
      case "g21_b_t": return r0(g["24k_tola_buy"] * 21 / 24);
      case "g21_b_g": return g["24k_tola_buy"] * 21 / 24 / TOLA;
      case "g21_b_10g": return g["24k_tola_buy"] * 21 / 24 / TOLA * 10;
      case "g18_s_t": return r0(g["24k_tola_sell"] * 18 / 24);
      case "g18_s_g": return g["24k_tola_sell"] * 18 / 24 / TOLA;
      case "g18_s_10g": return g["24k_tola_sell"] * 18 / 24 / TOLA * 10;
      case "g18_b_t": return r0(g["24k_tola_buy"] * 18 / 24);
      /* silver PSL 999 fine */
      case "psl_s_t": return s.psl_tola_sell;
      case "psl_b_t": return s.psl_tola_buy;
      case "psl_s_g": return s.psl_tola_sell / TOLA;
      case "psl_s_10g": return s.psl_tola_sell / TOLA * 10;
      case "psl_b_g": return s.psl_tola_buy / TOLA;
      case "psl_b_10g": return s.psl_tola_buy / TOLA * 10;
      case "psl_s_t05": return s.psl_tola_sell / 2;
      case "psl_b_t05": return s.psl_tola_buy / 2;
      case "psl_s_bar5": return s.psl_tola_sell * 5;
      case "psl_b_bar5": return s.psl_tola_buy * 5;
      case "psl_s_bar10": return s.psl_tola_sell * 10;
      case "psl_b_bar10": return s.psl_tola_buy * 10;
      case "psl_s_1kg": return s.psl_tola_sell / TOLA * 1000;
      case "psl_b_1kg": return s.psl_tola_buy / TOLA * 1000;
      case "psl_bulk52_s": return s.psl_tola_sell * 52;
      case "psl_bulk52_b": return s.psl_tola_buy * 52;
      case "psl_spread10": return (s.psl_tola_sell - s.psl_tola_buy) * 10;
      case "psl_rawa_gap": return s.psl_tola_sell - s.rawa_tola_sell;
      /* silver rawa */
      case "rawa_s_t": return s.rawa_tola_sell;
      case "rawa_b_t": return s.rawa_tola_buy;
      case "rawa_s_g": return s.rawa_tola_sell / TOLA;
      case "rawa_s_10g": return s.rawa_tola_sell / TOLA * 10;
      case "rawa_b_g": return s.rawa_tola_buy / TOLA;
      case "rawa_b_10g": return s.rawa_tola_buy / TOLA * 10;
      case "rawa_s_1kg": return s.rawa_tola_sell / TOLA * 1000;
      case "rawa_b_1kg": return s.rawa_tola_buy / TOLA * 1000;
      case "rawa_bulk50_s": return s.rawa_tola_sell * 50;
      case "rawa_bulk50_b": return s.rawa_tola_buy * 50;
      case "rawa_bulk52_s": return s.rawa_tola_sell * 52;
      case "rawa_bulk52_b": return s.rawa_tola_buy * 52;
      case "rawa_bulk525_s": return s.rawa_tola_sell * 52.5;
      case "rawa_bulk525_b": return s.rawa_tola_buy * 52.5;
      case "rawa_bulk55_s": return s.rawa_tola_sell * 55;
      case "rawa_bulk55_b": return s.rawa_tola_buy * 55;
      /* 925 sterling (from Rawa line) */
      case "ster_s_g": return s.rawa_tola_sell / TOLA * 0.925;
      case "ster_s_10g": return s.rawa_tola_sell / TOLA * 0.925 * 10;
      case "ster_s_t": return r0(s.rawa_tola_sell * 0.925);
      default: return 0;
    }
  }

  /* Per gram value for calculator metal selector */
  function metalPerGram(m) {
    switch (m) {
      case "g24": return MET("g24_s_g");
      case "g22": return MET("g22_s_g");
      case "g21": return MET("g21_s_g");
      case "g18": return MET("g18_s_g");
      case "psl": return MET("psl_s_g");
      case "rawa": return MET("rawa_s_g");
      case "ster": return MET("ster_s_g");
      default: return 0;
    }
  }

  var GRAMS_PER = {
    tola: 11.664,
    gram: 1,
    masha: 11.664 / 12,   /* 1 tola = 12 masha */
    ratti: 11.664 / 12 / 8 /* 1 masha = 8 ratti */
  };

  function hydrate() {
    var nodes = document.querySelectorAll(".v[data-f]");
    for (var i = 0; i < nodes.length; i++) {
      var v = MET(nodes[i].getAttribute("data-f"));
      if (v > 0) nodes[i].textContent = fmt(v);
    }
    var ups = document.querySelectorAll("[data-updated]");
    for (var j = 0; j < ups.length; j++) ups[j].textContent = R.last_updated;

        /* WhatsApp CTA – activates only when whatsapp_number is set in data/rates.json */
    var num = (R.whatsapp_number || "").replace(/[^0-9]/g, "");
    var blocks = document.querySelectorAll(".wa-cta");
    for (var k = 0; k < blocks.length; k++) {
      if (num) {
        blocks[k].hidden = false;
        var link = blocks[k].querySelector("#wa-link");
        if (link) {
          link.href = "https://wa.me/" + num +
            "?text=" + encodeURIComponent("Hello, I am interested in sealed silver bars. My city is: ");
        }
      } else {
        blocks[k].hidden = true;
      }
    }
  }

  /* ---------------- calculator ---------------- */
  function wireCalc() {
    var go = document.getElementById("calc-go");
    var w = document.getElementById("calc-w");
    if (!go || !w) return;

    function run() {
      var val = parseFloat(w.value);
      if (!val || val <= 0) return;
      var unit = document.getElementById("calc-u").value;
      var metal = document.getElementById("calc-m").value;
      var grams = val * GRAMS_PER[unit];
      var tolas = grams / TOLA;
      var value = grams * metalPerGram(metal);
      var name = document.getElementById("calc-m").options[document.getElementById("calc-m").selectedIndex].text;

      document.getElementById("calc-value").textContent = "Rs " + fmt(value);
      document.getElementById("calc-line1").textContent =
        val + " " + unit + " = " + grams.toFixed(2) + " grams = " + tolas.toFixed(3) + " tola";
      document.getElementById("calc-line2").textContent =
        name + " at the board rate on this page. Making charges are extra on jewellery.";
      document.getElementById("calc-out").hidden = false;

      /* kaat estimator if present */
      var kaatEl = document.getElementById("kaat-p");
      if (kaatEl) runKaat();
    }

    function runKaat() {
      var val = parseFloat(w.value);
      if (!val || val <= 0) return;
      var unit = document.getElementById("calc-u").value;
      var metal = document.getElementById("calc-m").value;
      var pct = parseFloat(document.getElementById("kaat-p").value) || 0;
      var grams = val * GRAMS_PER[unit];
      var metalValue = grams * metalPerGram(metal);
      var charges = metalValue * pct / 100;
      document.getElementById("kaat-total").textContent = "Rs " + fmt(metalValue + charges);
      document.getElementById("kaat-line1").textContent =
        "Metal value: Rs " + fmt(metalValue) + " + kaat " + pct + "%: Rs " + fmt(charges);
      document.getElementById("kaat-line2").textContent =
        "Estimated counter total including making charges. Shops may quote differently.";
      document.getElementById("kaat-out").hidden = false;
    }

    go.addEventListener("click", run);
    [w, document.getElementById("calc-u"), document.getElementById("calc-m")].forEach(function (el) {
      if (!el) return;
      el.addEventListener("input", run);
      el.addEventListener("change", run);
    });
    var kaatBtn = document.getElementById("kaat-go");
    if (kaatBtn) {
      kaatBtn.addEventListener("click", runKaat);
      document.getElementById("kaat-p").addEventListener("input", runKaat);
    }
  }

  /* -------- WhatsApp share: copy today's rates to clipboard -------- */
  function monthYear() {
    var m = ((R && R.last_updated) || "").match(/\d{1,2}\s+[A-Za-z]{3}\s+\d{4}/);
    return m ? m[0].replace(/^\d{1,2}\s+/, "") : "today";
  }

  function shareText() {
    var u = location.origin + location.pathname.replace(/\.html$/, "");
    var t = "*Today's Silver & Gold Rate in Pakistan (" + monthYear() + "):*\n";
    t += "\uD83E\uDE99 1 Tola PSL Silver Bar (999 fine): Rs. " + fmt(MET("psl_s_t")) + "\n";
    t += "\uD83E\uDE99 10 Tola PSL Silver Bar: Rs. " + fmt(MET("psl_s_bar10")) + "\n";
    t += "\uD83E\uDE99 24K Pure Gold (Per Tola): Rs. " + fmt(MET("g24_s_t")) + "\n";
    t += "Live updates & calculator: " + u;
    return t;
  }

  function wireShare() {
    var btn = document.getElementById("wa-copy-btn");
    if (!btn) return;
    btn.addEventListener("click", function () {
      function done() {
        btn.textContent = "Copied - paste it in your WhatsApp groups";
        btn.classList.add("copied");
        setTimeout(function () {
          btn.textContent = "\uD83D\uDCCB Copy Today's Rate for WhatsApp";
          btn.classList.remove("copied");
        }, 3000);
      }
      function fallback() {
        var ta = document.createElement("textarea");
        ta.value = shareText();
        ta.style.position = "fixed"; ta.style.opacity = "0";
        document.body.appendChild(ta); ta.select();
        try { document.execCommand("copy"); done(); } catch (e) { /* no-op */ }
        document.body.removeChild(ta);
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(shareText()).then(done, fallback);
      } else {
        fallback();
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      wireCalc();
      fetch("data/rates.json?ver=" + Date.now()).then(function (r) { return r.json(); })
        .then(function (j) { R = j; hydrate(); wireShare(); })
        .catch(function () { /* baked values already in HTML */ });
    });
  } else {
    wireCalc();
    fetch("data/rates.json?ver=" + Date.now()).then(function (r) { return r.json(); })
      .then(function (j) { R = j; hydrate(); wireShare(); })
      .catch(function () { });
  }
})();
