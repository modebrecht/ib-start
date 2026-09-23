from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")

css = r"""
    .html-runner {
      margin-top: 22px;
      padding: 16px;
      border: 1px solid color-mix(in srgb, var(--orange) 30%, var(--line));
      border-radius: 16px;
      background: color-mix(in srgb, var(--orange) 6%, var(--panel-bg));
    }
    .html-runner-head {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      flex-wrap: wrap;
      margin-bottom: 10px;
      color: var(--slide-title);
    }
    .html-runner-head span { color: var(--muted); font-size: .9em; font-weight: 650; }
    .html-runner textarea {
      min-height: 180px;
      font-family: Consolas, "Courier New", monospace;
      font-size: .9em;
      line-height: 1.4;
    }
    .html-runner-actions {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
      margin-top: 12px;
    }
    .html-runner-start {
      min-height: 46px;
      border: 0;
      border-radius: 999px;
      background: var(--orange);
      color: #fff;
      font: inherit;
      font-weight: 850;
      padding: 0 18px;
      cursor: pointer;
    }
    .html-runner-status { color: var(--muted); font-weight: 750; }
    body.presentation-open { overflow: hidden; }
    .presentation-stage[hidden] { display: none !important; }
    .presentation-stage {
      position: fixed;
      inset: 0;
      z-index: 1000000;
      width: 100vw;
      height: 100dvh;
      background: #000;
      overflow: hidden;
    }
    .presentation-frame {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      border: 0;
      background: #fff;
    }
    .presentation-back {
      position: fixed;
      top: max(12px, env(safe-area-inset-top));
      left: max(12px, env(safe-area-inset-left));
      z-index: 1000001;
      width: 48px;
      height: 48px;
      display: grid;
      place-items: center;
      padding: 0 0 3px;
      border: 1px solid rgba(255,255,255,.4);
      border-radius: 50%;
      background: rgba(15,23,42,.72);
      color: #fff;
      font: inherit;
      font-size: 1.75rem;
      font-weight: 900;
      cursor: pointer;
      opacity: .5;
      backdrop-filter: blur(8px);
    }
    .presentation-back:hover,
    .presentation-back:focus-visible { opacity: .92; }
    @media print {
      .html-runner, .presentation-stage { display: none !important; }
    }

"""

runner_html = r"""
            <div class="html-runner">
              <div class="html-runner-head">
                <strong>HTML-Präsentation testen</strong>
                <span>Esc zurück · ← vorherige · → / ↓ / Leertaste nächste</span>
              </div>
              <label>HTML-Code hier einfügen
                <textarea data-html-runner-input data-no-store data-ignore-completion spellcheck="false" placeholder="&lt;!doctype html&gt; ..."></textarea>
              </label>
              <div class="html-runner-actions">
                <button class="html-runner-start" type="button" data-html-runner-start>▶ Fullscreen starten</button>
                <span class="html-runner-status" data-html-runner-status aria-live="polite"></span>
              </div>
            </div>
"""

overlay_html = r"""
  <div class="presentation-stage" data-presentation-stage hidden>
    <button class="presentation-back" type="button" data-presentation-back aria-label="Zurück zum IB-Startcheck" title="Zurück (Esc)">←</button>
    <iframe class="presentation-frame" data-presentation-frame title="HTML-Präsentation" sandbox="allow-scripts allow-forms allow-modals allow-pointer-lock allow-presentation" allow="fullscreen; autoplay"></iframe>
  </div>
"""

runner_js = r"""
      const htmlRunnerInput = document.querySelector("[data-html-runner-input]");
      const htmlRunnerStart = document.querySelector("[data-html-runner-start]");
      const htmlRunnerStatus = document.querySelector("[data-html-runner-status]");
      const presentationStage = document.querySelector("[data-presentation-stage]");
      const presentationFrame = document.querySelector("[data-presentation-frame]");
      const presentationBack = document.querySelector("[data-presentation-back]");
      let presentationActive = false;
      let nativePresentationFullscreen = false;

      const runnerStatus = (text, error = false) => {
        if (!htmlRunnerStatus) return;
        htmlRunnerStatus.textContent = text;
        htmlRunnerStatus.style.color = error ? "var(--red)" : "";
      };

      const cleanPastedHtml = (value) => {
        const html = value.trim();
        if (!html.startsWith("```")) return html;
        return html.replace(/^```(?:html)?\s*/i, "").replace(/\s*```\s*$/, "").trim();
      };

      const presentationBridge = `<script>
(() => {
  window.addEventListener("keydown", (event) => {
    const editing = event.target && (
      event.target.matches?.("input, textarea, select") || event.target.isContentEditable
    );
    if (event.key === "Escape") {
      event.preventDefault();
      event.stopImmediatePropagation();
      parent.postMessage({ type: "ib-presentation-exit" }, "*");
      return;
    }
    if (editing) return;
    if (event.key === "ArrowDown" || event.key === " " || event.code === "Space") {
      event.preventDefault();
      event.stopImmediatePropagation();
      window.dispatchEvent(new KeyboardEvent("keydown", {
        key: "ArrowRight", code: "ArrowRight", bubbles: true, cancelable: true
      }));
    }
  }, true);

  window.addEventListener("message", (event) => {
    if (event.data?.type !== "ib-presentation-key") return;
    const key = event.data.key;
    window.dispatchEvent(new KeyboardEvent("keydown", {
      key, code: key === " " ? "Space" : key, bubbles: true, cancelable: true
    }));
  });
})();
<\/script>`;

      const withPresentationBridge = (html) => {
        const head = /<head(?:\s[^>]*)?>/i;
        return head.test(html)
          ? html.replace(head, (match) => `${match}${presentationBridge}`)
          : `${presentationBridge}${html}`;
      };

      const closePresentation = (skipNativeExit = false) => {
        if (!presentationActive) return;
        presentationActive = false;
        document.body.classList.remove("presentation-open");
        if (presentationStage) presentationStage.hidden = true;
        if (presentationFrame) presentationFrame.srcdoc = "";
        if (!skipNativeExit && document.fullscreenElement === presentationStage) {
          document.exitFullscreen?.().catch(() => {});
        }
        nativePresentationFullscreen = false;
        runnerStatus("Präsentation beendet.");
        htmlRunnerStart?.focus();
      };

      const startPresentation = () => {
        if (!htmlRunnerInput || !presentationStage || !presentationFrame) return;
        const html = cleanPastedHtml(htmlRunnerInput.value);
        if (!html) {
          runnerStatus("Bitte zuerst den HTML-Code einfügen.", true);
          htmlRunnerInput.focus();
          return;
        }

        runnerStatus("");
        presentationFrame.srcdoc = withPresentationBridge(html);
        presentationStage.hidden = false;
        document.body.classList.add("presentation-open");
        presentationActive = true;
        nativePresentationFullscreen = false;
        presentationFrame.addEventListener("load", () => presentationFrame.focus(), { once: true });

        if (presentationStage.requestFullscreen) {
          presentationStage.requestFullscreen()
            .then(() => { nativePresentationFullscreen = true; })
            .catch(() => presentationFrame.focus());
        } else {
          presentationFrame.focus();
        }
      };

      htmlRunnerStart?.addEventListener("click", startPresentation);
      presentationBack?.addEventListener("click", () => closePresentation());

      window.addEventListener("message", (event) => {
        if (event.data?.type === "ib-presentation-exit") closePresentation();
      });

      document.addEventListener("fullscreenchange", () => {
        if (presentationActive && nativePresentationFullscreen && !document.fullscreenElement) {
          closePresentation(true);
        }
      });

      document.addEventListener("keydown", (event) => {
        if (!presentationActive) return;
        if (event.key === "Escape") {
          event.preventDefault();
          closePresentation();
          return;
        }
        if (event.target === presentationBack && (event.key === " " || event.key === "Enter")) return;
        if (["ArrowLeft", "ArrowRight", "ArrowDown", " "].includes(event.key)) {
          event.preventDefault();
          presentationFrame?.contentWindow?.postMessage({
            type: "ib-presentation-key",
            key: event.key
          }, "*");
        }
      }, true);

"""

def replace_once(old, new, label):
    global text
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected once, found {count}")
    text = text.replace(old, new, 1)

replace_once("    .slide-controls {", css + "    .slide-controls {", "CSS marker")
replace_once(
    'button:not(.match-item):not(.task-tile):not(.round-nav):not(.print-final):not(.copy-prompt):not(.check-button):not(.read-button):not(.settings-button):not(.admin-unlock) {',
    'button:not(.match-item):not(.task-tile):not(.round-nav):not(.print-final):not(.copy-prompt):not(.check-button):not(.read-button):not(.settings-button):not(.admin-unlock):not(.html-runner-start):not(.presentation-back) {',
    "generic button selector"
)

task2_start = text.index('<section class="section" data-task="task-2"')
task3_start = text.index('<section class="section" data-task="task-3"', task2_start)
task2 = text[task2_start:task3_start]
task2_tail = "          </div>\n        </div>\n      </section>"
tail_pos = task2.rfind(task2_tail)
if tail_pos == -1:
    raise SystemExit("task 02 closing marker not found")
task2 = task2[:tail_pos] + runner_html + task2[tail_pos:]
text = text[:task2_start] + task2 + text[task3_start:]

replace_once(
    "- Navigation mit Pfeiltasten und Buttons.",
    "- Navigation: Pfeiltaste rechts, Pfeiltaste runter oder Leertaste = nächste Folie; Pfeiltaste links = vorherige Folie; zusätzlich sichtbare Buttons.",
    "prompt navigation"
)
replace_once("  </form>\n  <script>", "  </form>" + overlay_html + "  <script>", "form/script marker")
replace_once(
    '''const fields = form ? [...form.querySelectorAll('input:not([data-theme-toggle]):not([type="password"]):not([type="range"]), textarea')] : [];''',
    '''const fields = form ? [...form.querySelectorAll('input:not([data-theme-toggle]):not([type="password"]):not([type="range"]):not([data-no-store]), textarea:not([data-no-store])')] : [];''',
    "stored fields selector"
)
replace_once(
    '''const textFields = [...task.querySelectorAll('input[type="text"], input[type="date"], textarea')];''',
    '''const textFields = [...task.querySelectorAll('input[type="text"]:not([data-ignore-completion]), input[type="date"]:not([data-ignore-completion]), textarea:not([data-ignore-completion])')];''',
    "completion selector"
)
replace_once("      const fieldKey = (field, index) => {", runner_js + "      const fieldKey = (field, index) => {", "fieldKey marker")

for needle in (
    "data-html-runner-input",
    "data-presentation-stage",
    "ib-presentation-exit",
    "textarea:not([data-no-store])",
    "textarea:not([data-ignore-completion])",
    "Pfeiltaste runter oder Leertaste = nächste Folie"
):
    if needle not in text:
        raise SystemExit(f"Missing expected content: {needle}")

path.write_text(text, encoding="utf-8")
