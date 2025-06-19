(() => {
  const DEFAULTS = {
    highlight: true,
    viewportOnly: true,
    viewportExpansion: 0,
    debug: false,
    focusIndex: -1,
  };
  const cfg = { ...DEFAULTS };

  // --- CACHING ---
  const CACHE = {
    rects: new WeakMap(),
    styles: new WeakMap(),
    clear() {
      this.rects = new WeakMap();
      this.styles = new WeakMap();
    },
  };

  function getCachedRects(el) {
    if (CACHE.rects.has(el)) return CACHE.rects.get(el);
    const rects = Array.from(el.getClientRects());
    CACHE.rects.set(el, rects);
    return rects;
  }

  function getCachedStyle(el) {
    if (CACHE.styles.has(el)) return CACHE.styles.get(el);
    const style = window.getComputedStyle(el);
    CACHE.styles.set(el, style);
    return style;
  }

  // --- XPATH ---
  const xpathCache = new WeakMap();
  function getXPath(el) {
    if (xpathCache.has(el)) return xpathCache.get(el);
    const segs = [];
    let node = el;
    while (node && node.nodeType === 1 && node !== document.body) {
      let i = 1;
      let sibling = node.previousSibling;
      while (sibling) {
        if (sibling.nodeType === 1 && sibling.tagName === node.tagName) i++;
        sibling = sibling.previousSibling;
      }
      segs.unshift(`${node.tagName.toLowerCase()}[${i}]`);
      node = node.parentNode;
    }
    const path = "/body/" + segs.join("/");
    xpathCache.set(el, path);
    return path;
  }

  // --- CONTAINER & CLEANUP ---
  const CONTAINER_ID = "autosurfer-overlay";
  window._highlightCleanup = [];
  function initContainer() {
    let c = document.getElementById(CONTAINER_ID);
    if (!c) {
      c = document.createElement("div");
      c.id = CONTAINER_ID;
      Object.assign(c.style, {
        position: "fixed",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        pointerEvents: "none",
        zIndex: 2147483640,
      });
      document.body.appendChild(c);
      window._highlightCleanup.push(() => c.remove());
    }
    c.innerHTML = "";
    return c;
  }

  function cleanupHighlights() {
    window._highlightCleanup.forEach((fn) => fn());
    window._highlightCleanup = [];
    CACHE.clear();
  }
  window.clearInteractiveHighlights = cleanupHighlights;

  // --- UTILITIES ---
  function inViewport(rects, exp) {
    return rects.some(
      (r) =>
        !(
          r.bottom < -exp ||
          r.top > innerHeight + exp ||
          r.right < -exp ||
          r.left > innerWidth + exp
        )
    );
  }

  function isInteractive(el, style) {
    const tag = el.tagName.toLowerCase();
    if (style.cursor === "pointer") return true;
    if (
      [
        "a",
        "button",
        "input",
        "select",
        "textarea",
        "summary",
        "details",
        "label",
      ].includes(tag)
    ) {
      if (el.disabled || style.pointerEvents === "none") return false;
      return true;
    }
    return el.hasAttribute("onclick") || el.getAttribute("role");
  }

  function drawBox(container, r, idx) {
    const colors = [
      "#ff5f5f",
      "#58d365",
      "#5899ff",
      "#ffa656",
      "#c158ff",
      "#00c3c3",
    ];
    const color = colors[idx % colors.length];
    const box = document.createElement("div");
    Object.assign(box.style, {
      position: "fixed",
      left: `${r.left}px`,
      top: `${r.top}px`,
      width: `${r.width}px`,
      height: `${r.height}px`,
      border: `2px solid ${color}`,
      background: `${color}1a`,
      boxSizing: "border-box",
    });
    const label = document.createElement("span");
    Object.assign(label.style, {
      position: "absolute",
      top: "2px",
      right: "2px",
      background: color,
      color: "#fff",
      font: "10px/12px sans-serif",
      padding: "0 2px",
      borderRadius: "2px",
    });
    label.textContent = idx;
    box.appendChild(label);
    container.appendChild(box);
    window._highlightCleanup.push(() => box.remove());
  }

  // --- MAIN ---
  window.collectInteractive = (opts = {}) => {
    Object.assign(cfg, opts);
    if (cfg.debug) console.log("collectInteractive config:", cfg);
    const out = [];
    const container = cfg.highlight ? initContainer() : null;
    let idx = 0;

    document.querySelectorAll("*").forEach((el) => {
      const style = getCachedStyle(el);
      if (style.visibility === "hidden" || style.display === "none") return;
      if (el.offsetWidth === 0 && el.offsetHeight === 0) return;

      const rects = getCachedRects(el);
      if (cfg.viewportOnly && !inViewport(rects, cfg.viewportExpansion)) return;
      if (!isInteractive(el, style)) return;

      rects.forEach((r) => {
        if (r.width === 0 || r.height === 0) return;
        if (cfg.focusIndex >= 0 && cfg.focusIndex !== idx) {
          idx++;
          return;
        }

        out.push({
          index: idx,
          xpath: getXPath(el),
          tag: el.tagName.toLowerCase(),
          text: (el.innerText || "").trim().slice(0, 60),
          rect: { x: r.x, y: r.y, w: r.width, h: r.height },
        });
        if (cfg.highlight) drawBox(container, r, idx);
        idx++;
      });
    });

    return out;
  };

  // --- RESIZE/SCROLL UPDATES (throttled) ---
  let ticking = false;
  function refresh() {
    if (!ticking) {
      ticking = true;
      requestAnimationFrame(() => {
        window.collectInteractive({ ...cfg });
        ticking = false;
      });
    }
  }
  window.addEventListener("scroll", refresh, true);
  window.addEventListener("resize", refresh);
})();
