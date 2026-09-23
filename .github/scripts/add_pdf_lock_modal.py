from pathlib import Path

path = Path('index.html')
s = path.read_text(encoding='utf-8')

css_anchor = '''    .print-status ul {
      margin: 6px 0 0;
      padding-left: 1.2rem;
    }
'''
css = '''

    body.pdf-modal-open {
      overflow: hidden;
    }

    .pdf-lock-modal[hidden] {
      display: none !important;
    }

    .pdf-lock-modal {
      position: fixed;
      inset: 0;
      z-index: 2000000;
      display: grid;
      place-items: center;
      padding: 20px;
    }

    .pdf-lock-backdrop {
      position: absolute;
      inset: 0;
      background: rgba(15, 23, 42, .58);
      backdrop-filter: blur(7px);
      -webkit-backdrop-filter: blur(7px);
    }

    .pdf-lock-dialog {
      position: relative;
      width: min(520px, 100%);
      max-height: calc(100dvh - 40px);
      overflow: auto;
      padding: 30px;
      border: 1px solid color-mix(in srgb, var(--red) 24%, var(--line));
      border-radius: 24px;
      background: var(--slide-bg);
      color: var(--slide-text);
      box-shadow: 0 28px 90px rgba(15, 23, 42, .36);
      animation: pdf-lock-pop .18s ease-out;
    }

    .pdf-lock-close {
      position: absolute;
      top: 14px;
      right: 14px;
      width: 38px;
      height: 38px;
      display: grid;
      place-items: center;
      padding: 0;
      border: 0;
      border-radius: 50%;
      background: color-mix(in srgb, var(--slide-text) 7%, transparent);
      color: var(--slide-text);
      font: inherit;
      font-size: 1.45rem;
      line-height: 1;
      cursor: pointer;
    }

    .pdf-lock-close:hover,
    .pdf-lock-close:focus-visible {
      background: color-mix(in srgb, var(--slide-text) 13%, transparent);
      outline: 3px solid color-mix(in srgb, var(--red) 22%, transparent);
      outline-offset: 2px;
    }

    .pdf-lock-icon {
      width: 52px;
      height: 52px;
      display: grid;
      place-items: center;
      margin-bottom: 16px;
      border-radius: 16px;
      background: color-mix(in srgb, var(--red) 12%, var(--panel-bg));
      color: var(--red);
      font-size: 1.55rem;
      font-weight: 950;
    }

    .pdf-lock-dialog h2 {
      margin: 0 44px 8px 0;
      color: var(--slide-title);
      font-size: clamp(1.5rem, 4vw, 2rem);
      line-height: 1.1;
    }

    .pdf-lock-dialog p {
      margin: 0 0 18px;
      color: var(--muted);
      font-weight: 650;
    }

    .pdf-lock-list {
      display: grid;
      gap: 8px;
      margin: 0 0 22px;
      padding: 0;
      list-style: none;
    }

    .pdf-lock-list li {
      padding: 11px 13px;
      border: 1px solid var(--line);
      border-radius: 12px;
      background: var(--panel-bg);
      color: var(--slide-text);
      font-weight: 800;
    }

    .pdf-lock-dismiss {
      min-height: 46px;
      padding: 0 18px;
      border: 0;
      border-radius: 999px;
      background: var(--red);
      color: #fff;
      font: inherit;
      font-weight: 850;
      cursor: pointer;
      box-shadow: 0 10px 24px color-mix(in srgb, var(--red) 24%, transparent);
    }

    .pdf-lock-dismiss:hover,
    .pdf-lock-dismiss:focus-visible {
      filter: brightness(1.05);
      outline: 3px solid color-mix(in srgb, var(--red) 22%, transparent);
      outline-offset: 2px;
    }

    @keyframes pdf-lock-pop {
      from { opacity: 0; transform: translateY(10px) scale(.98); }
      to { opacity: 1; transform: translateY(0) scale(1); }
    }
'''
if css_anchor not in s:
    raise SystemExit('CSS anchor not found')
s = s.replace(css_anchor, css_anchor + css, 1)

old_selector = ':not(.html-runner-start):not(.presentation-back) {'
new_selector = ':not(.html-runner-start):not(.presentation-back):not(.pdf-lock-close):not(.pdf-lock-dismiss) {'
if old_selector not in s:
    raise SystemExit('button selector anchor not found')
s = s.replace(old_selector, new_selector, 1)

print_anchor = '      .html-runner, .presentation-stage { display: none !important; }'
if print_anchor not in s:
    raise SystemExit('print hide anchor not found')
s = s.replace(print_anchor, '      .html-runner, .presentation-stage, .pdf-lock-modal { display: none !important; }', 1)

html_anchor = '''  </form>
  <div class="presentation-stage" data-presentation-stage hidden>'''
modal_html = '''  </form>
  <div class="pdf-lock-modal" data-pdf-lock-modal hidden>
    <div class="pdf-lock-backdrop" data-pdf-lock-close aria-hidden="true"></div>
    <section class="pdf-lock-dialog" role="dialog" aria-modal="true" aria-labelledby="pdf-lock-title" aria-describedby="pdf-lock-description">
      <button class="pdf-lock-close" type="button" data-pdf-lock-close aria-label="Fenster schliessen">×</button>
      <div class="pdf-lock-icon" aria-hidden="true">!</div>
      <h2 id="pdf-lock-title">PDF noch gesperrt</h2>
      <p id="pdf-lock-description">Erledige zuerst diese Aufgaben:</p>
      <ul class="pdf-lock-list" data-pdf-lock-list></ul>
      <button class="pdf-lock-dismiss" type="button" data-pdf-lock-close>Schliessen</button>
    </section>
  </div>
  <div class="presentation-stage" data-presentation-stage hidden>'''
if html_anchor not in s:
    raise SystemExit('HTML modal anchor not found')
s = s.replace(html_anchor, modal_html, 1)

js_anchor = '''      const setPrintStatus = (html = "", mode = "idle") => {
        if (!printStatus) return;
        printStatus.innerHTML = html;
        printStatus.classList.toggle("is-error", mode === "error");
        printStatus.classList.toggle("is-admin", mode === "admin");
      };
'''
modal_js = '''

      let pdfLockReturnFocus = null;

      const closePdfLockModal = () => {
        const modal = document.querySelector("[data-pdf-lock-modal]");
        if (!modal || modal.hidden) return;
        modal.hidden = true;
        document.body.classList.remove("pdf-modal-open");
        pdfLockReturnFocus?.focus?.();
        pdfLockReturnFocus = null;
      };

      const openPdfLockModal = (missing) => {
        const modal = document.querySelector("[data-pdf-lock-modal]");
        const list = document.querySelector("[data-pdf-lock-list]");
        if (!modal || !list) return;
        list.replaceChildren(...missing.map((tile) => {
          const item = document.createElement("li");
          item.textContent = taskTileLabel(tile);
          return item;
        }));
        pdfLockReturnFocus = document.activeElement;
        modal.hidden = false;
        document.body.classList.add("pdf-modal-open");
        modal.querySelector(".pdf-lock-dismiss")?.focus();
      };

      document.querySelectorAll("[data-pdf-lock-close]").forEach((button) => {
        button.addEventListener("click", closePdfLockModal);
      });

      document.addEventListener("keydown", (event) => {
        const modal = document.querySelector("[data-pdf-lock-modal]");
        if (event.key === "Escape" && modal && !modal.hidden) {
          event.preventDefault();
          closePdfLockModal();
        }
      });
'''
if js_anchor not in s:
    raise SystemExit('JS status anchor not found')
s = s.replace(js_anchor, js_anchor + modal_js, 1)

old_lock = '''        const list = missing.map((tile) => `<li>${taskTileLabel(tile)}</li>`).join("");
        setPrintStatus(`PDF noch gesperrt. Diese Aufgaben fehlen noch:<ul>${list}</ul>`, "error");'''
new_lock = '''        setPrintStatus("");
        openPdfLockModal(missing);'''
if old_lock not in s:
    raise SystemExit('handlePrint lock block not found')
s = s.replace(old_lock, new_lock, 1)

path.write_text(s, encoding='utf-8')
