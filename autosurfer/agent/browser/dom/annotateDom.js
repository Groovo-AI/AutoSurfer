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

  // --- ENHANCED XPATH ---
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

  // --- ENHANCED ELEMENT ANALYSIS ---
  function getElementDetails(el) {
    const details = {
      tag: el.tagName.toLowerCase(),
      id: el.id || null,
      className: el.className || null,
      name: el.name || null,
      type: el.type || null,
      value: el.value || null,
      placeholder: el.placeholder || null,
      title: el.title || null,
      alt: el.alt || null,
      href: el.href || null,
      role: el.getAttribute("role") || null,
      "data-testid": el.getAttribute("data-testid") || null,
      "data-test": el.getAttribute("data-test") || null,
      "aria-label": el.getAttribute("aria-label") || null,
      "aria-labelledby": el.getAttribute("aria-labelledby") || null,
      text: (el.innerText || "").trim().slice(0, 100),
      visible: true,
      enabled: !el.disabled,
      required: el.required || false,
      checked: el.checked || false,
      selected: el.selected || false,
    };

    // Check visibility
    const style = getCachedStyle(el);
    if (
      style.visibility === "hidden" ||
      style.display === "none" ||
      style.opacity === "0"
    ) {
      details.visible = false;
    }

    return details;
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

    // Check for pointer cursor
    if (style.cursor === "pointer") return true;

    // Check for interactive tags
    const interactiveTags = [
      "a",
      "button",
      "input",
      "select",
      "textarea",
      "summary",
      "details",
      "label",
      "option",
      "optgroup",
    ];

    if (interactiveTags.includes(tag)) {
      if (el.disabled || style.pointerEvents === "none") return false;
      return true;
    }

    // Check for event handlers
    if (el.hasAttribute("onclick") || el.getAttribute("role")) return true;

    // Check for clickable elements with specific classes
    const clickableClasses = ["btn", "button", "clickable", "link", "nav-link"];
    if (el.className && typeof el.className === "string") {
      if (clickableClasses.some((cls) => el.className.includes(cls)))
        return true;
    }

    return false;
  }

  function hasTextContent(el) {
    // Check if element has meaningful text content
    const text = el.textContent ? el.textContent.trim() : "";
    return text.length > 0 && text.length < 1000; // Limit to avoid huge text blocks
  }

  function isTextElement(el, style) {
    const tag = el.tagName.toLowerCase();

    // Focus on container-level text elements, not low-level formatting
    const containerTags = [
      "h1",
      "h2",
      "h3",
      "h4",
      "h5",
      "h6", // Headings
      "p",
      "div",
      "section",
      "article",
      "main",
      "aside", // Main containers
      "li",
      "td",
      "th", // List items and table cells
      "blockquote",
      "cite",
      "figcaption", // Quotes and captions
      "nav",
      "header",
      "footer", // Navigation and structural elements
    ];

    // Only include container-level elements, skip low-level formatting
    if (!containerTags.includes(tag)) return false;

    // Check if it has meaningful text content
    if (!hasTextContent(el)) return false;

    // Skip if it's hidden or has no dimensions
    if (style.visibility === "hidden" || style.display === "none") return false;
    if (el.offsetWidth === 0 || el.offsetHeight === 0) return false;

    // Skip very small elements (likely low-level formatting)
    if (el.offsetWidth < 50 || el.offsetHeight < 20) return false;

    // Skip if it's just a wrapper with no direct text content
    if (el.children.length > 0) {
      // Check if any direct child has text
      const hasDirectText = Array.from(el.childNodes).some(
        (node) => node.nodeType === 3 && node.textContent.trim().length > 0
      );
      if (!hasDirectText) return false;
    }

    return true;
  }

  function getPriorityScore(el, details) {
    let score = 0;

    // Higher priority for elements with specific attributes
    if (details.id) score += 100;
    if (details["data-testid"]) score += 90;
    if (details["data-test"]) score += 85;
    if (details["aria-label"]) score += 80;
    if (details.name) score += 70;
    if (details.role) score += 60;

    // Priority for form elements
    if (details.tag === "input" && details.type) {
      if (
        details.type === "text" ||
        details.type === "email" ||
        details.type === "password"
      )
        score += 50;
      if (details.type === "submit" || details.type === "button") score += 40;
    }

    // Priority for buttons and links
    if (details.tag === "button" || details.tag === "a") score += 30;

    // Priority for headings (important for content structure)
    if (["h1", "h2", "h3", "h4", "h5", "h6"].includes(details.tag)) {
      score += 25;
    }

    // Priority for paragraphs and main content
    if (["p", "article", "section", "main"].includes(details.tag)) {
      score += 15;
    }

    // Priority for visible text
    if (details.text && details.text.length > 0) score += 20;

    return score;
  }

  function drawBox(container, r, idx, priority) {
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
    label.textContent = `${idx}(${priority})`;
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

    // Collect all elements first
    const elements = [];
    document.querySelectorAll("*").forEach((el) => {
      const style = getCachedStyle(el);
      if (style.visibility === "hidden" || style.display === "none") return;
      if (el.offsetWidth === 0 && el.offsetHeight === 0) return;

      const rects = getCachedRects(el);
      if (cfg.viewportOnly && !inViewport(rects, cfg.viewportExpansion)) return;

      // Include both interactive elements and text elements
      if (!isInteractive(el, style) && !isTextElement(el, style)) return;

      rects.forEach((r) => {
        if (r.width === 0 || r.height === 0) return;
        if (cfg.focusIndex >= 0 && cfg.focusIndex !== idx) {
          idx++;
          return;
        }

        const details = getElementDetails(el);
        const priority = getPriorityScore(el, details);

        elements.push({
          element: el,
          rect: r,
          details: details,
          priority: priority,
          index: idx,
        });
        idx++;
      });
    });

    // Sort by priority and add to output
    elements.sort((a, b) => b.priority - a.priority);

    elements.forEach((item) => {
      out.push({
        index: item.index,
        xpath: getXPath(item.element),
        ...item.details,
        rect: {
          x: item.rect.x,
          y: item.rect.y,
          w: item.rect.width,
          h: item.rect.height,
        },
        priority: item.priority,
      });

      if (cfg.highlight)
        drawBox(container, item.rect, item.index, item.priority);
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
