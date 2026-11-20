/**
 * site.ts — everything that runs in the browser, in one small module:
 * theme toggle, quest progress, copy buttons, Mermaid on demand.
 *
 * Progress uses the same localStorage key and shape as the Jekyll site's
 * assets/js/quest-progress.js, so a learner's saved progress survives the move.
 */

/* ---- Theme --------------------------------------------------------------- */

const THEME_KEY = 'it-journey-theme';
const root = document.documentElement;
const systemDark = matchMedia('(prefers-color-scheme: dark)');
const isDark = () => (root.dataset.theme ? root.dataset.theme === 'dark' : systemDark.matches);

document.querySelector('[data-theme-toggle]')?.addEventListener('click', () => {
  const next = isDark() ? 'light' : 'dark';
  root.dataset.theme = next;
  try {
    localStorage.setItem(THEME_KEY, next);
  } catch {
    // Private mode: the choice lasts for this page only.
  }
});

/* ---- Progress ------------------------------------------------------------ */

const PROGRESS_KEY = 'it-journey-quest-progress';
const LAST_QUEST_KEY = 'it-journey-last-quest';

interface QuestState {
  completed: boolean;
  completedAt: string | null;
  objectives: Record<string, boolean>;
}
type Store = Record<string, QuestState>;

function loadStore(): Store {
  try {
    return (JSON.parse(localStorage.getItem(PROGRESS_KEY) ?? '{}') as Store) ?? {};
  } catch {
    return {};
  }
}

function saveStore(store: Store): void {
  try {
    localStorage.setItem(PROGRESS_KEY, JSON.stringify(store));
  } catch {
    // Storage unavailable: progress is kept for this page view only.
  }
}

const normalize = (permalink: string) => (permalink && !permalink.endsWith('/') ? `${permalink}/` : permalink);

function hydrateQuest(store: Store): void {
  const quest = document.querySelector<HTMLElement>('[data-quest-root]');
  if (!quest) return;
  const permalink = normalize(quest.dataset.questPermalink ?? '');
  if (!permalink) return;

  const state = (store[permalink] ??= { completed: false, completedAt: null, objectives: {} });
  // Every checkbox in the quest body is an objective, indexed in document order
  // (the old script's rule, so stored indices still line up).
  const boxes = [...document.querySelectorAll<HTMLInputElement>('#quest-content input[type="checkbox"]')];

  const render = () => {
    const total = boxes.length;
    const done = boxes.filter((_, index) => state.objectives[index] === true).length;
    const percent = state.completed ? 100 : total === 0 ? 0 : Math.round((done / total) * 100);
    const label = state.completed ? 'Complete' : done === 0 ? 'Not started' : `${done} of ${total} objectives`;

    quest.classList.toggle('is-complete', state.completed);
    for (const el of document.querySelectorAll<HTMLElement>('[data-progress-label]')) el.textContent = label;
    for (const el of document.querySelectorAll<HTMLElement>('[data-progress-fill]')) el.style.width = `${percent}%`;
    for (const el of document.querySelectorAll<HTMLElement>('[data-progress-toggle]')) {
      el.setAttribute('aria-pressed', String(state.completed));
      el.textContent = state.completed ? 'Completed ✓' : 'Mark complete';
    }
  };

  boxes.forEach((box, index) => {
    box.disabled = false;
    box.checked = state.objectives[index] === true;
    const text = box.closest('li')?.textContent?.trim();
    if (text) box.setAttribute('aria-label', text);
    box.addEventListener('change', () => {
      state.objectives[index] = box.checked;
      const allDone = boxes.every((_, i) => state.objectives[i] === true);
      if (allDone !== state.completed) {
        state.completed = allDone;
        state.completedAt = allDone ? new Date().toISOString() : null;
      }
      saveStore(store);
      render();
    });
  });

  for (const toggle of document.querySelectorAll<HTMLElement>('[data-progress-toggle]')) {
    toggle.addEventListener('click', () => {
      state.completed = !state.completed;
      state.completedAt = state.completed ? new Date().toISOString() : null;
      if (state.completed) {
        boxes.forEach((box, index) => {
          box.checked = true;
          state.objectives[index] = true;
        });
      }
      saveStore(store);
      render();
    });
  }

  document.querySelector('[data-progress-reset]')?.addEventListener('click', () => {
    if (!confirm('Reset your progress on this quest?')) return;
    state.completed = false;
    state.completedAt = null;
    state.objectives = {};
    for (const box of boxes) box.checked = false;
    saveStore(store);
    render();
  });

  render();

  try {
    localStorage.setItem(LAST_QUEST_KEY, JSON.stringify({ permalink, title: quest.dataset.questTitle ?? '' }));
  } catch {
    // Not essential.
  }
}

/** Ticks on quest links, and "n of m" on anything that groups quests. */
function hydrateLists(store: Store): void {
  const isDone = (permalink: string) => store[normalize(permalink)]?.completed === true;

  for (const el of document.querySelectorAll<HTMLElement>('[data-quest-link]')) {
    el.classList.toggle('is-complete', isDone(el.dataset.questLink ?? ''));
  }

  for (const group of document.querySelectorAll<HTMLElement>('[data-quest-group]')) {
    let quests: string[] = [];
    try {
      quests = JSON.parse(group.dataset.questGroup ?? '[]') as string[];
    } catch {
      continue;
    }
    const done = quests.filter(isDone).length;
    const label = group.querySelector<HTMLElement>('[data-group-label]');
    const fill = group.querySelector<HTMLElement>('[data-group-fill]');
    if (label) label.textContent = `${done} of ${quests.length} complete`;
    if (fill) fill.style.width = quests.length ? `${Math.round((done / quests.length) * 100)}%` : '0%';
  }

  const resume = document.querySelector<HTMLElement>('[data-resume]');
  if (resume) {
    try {
      const last = JSON.parse(localStorage.getItem(LAST_QUEST_KEY) ?? 'null') as { permalink?: string; title?: string } | null;
      const link = resume.querySelector('a');
      if (last?.permalink?.startsWith('/quests/') && link) {
        link.href = last.permalink;
        const title = resume.querySelector<HTMLElement>('[data-resume-title]');
        if (title) title.textContent = last.title || last.permalink;
        resume.hidden = false;
      }
    } catch {
      // Leave it hidden.
    }
  }
}

const store = loadStore();
hydrateQuest(store);
hydrateLists(store);
// Another tab finished a quest: refresh the ticks here too.
addEventListener('storage', (event) => {
  if (event.key === PROGRESS_KEY) hydrateLists(loadStore());
});

/* ---- Code blocks --------------------------------------------------------- */

// Two spellings in the content: a ```mermaid fence, and the older <div class="mermaid">.
const diagrams: HTMLElement[] = [...document.querySelectorAll<HTMLElement>('.prose div.mermaid')];

for (const pre of document.querySelectorAll<HTMLElement>('.prose pre')) {
  if (pre.dataset.language === 'mermaid') {
    diagrams.push(pre);
    continue;
  }
  const wrap = document.createElement('div');
  wrap.className = 'code-block';
  pre.replaceWith(wrap);
  wrap.append(pre);

  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'code-copy';
  button.textContent = 'Copy';
  button.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(pre.innerText);
      button.textContent = 'Copied';
    } catch {
      button.textContent = 'Press ⌘/Ctrl+C';
    }
    setTimeout(() => (button.textContent = 'Copy'), 1600);
  });
  wrap.append(button);
}

/* ---- Mermaid: loaded only on pages that have a diagram ------------------- */

if (diagrams.length) {
  void import('mermaid').then(async ({ default: mermaid }) => {
    mermaid.initialize({ startOnLoad: false, securityLevel: 'strict', theme: isDark() ? 'dark' : 'default' });
    let count = 0;
    for (const source of diagrams) {
      try {
        const { svg } = await mermaid.render(`diagram-${(count += 1)}`, (source.textContent ?? '').trim());
        const figure = document.createElement('figure');
        figure.className = 'diagram';
        figure.innerHTML = svg;
        source.replaceWith(figure);
      } catch {
        // Leave the source visible; a broken diagram should not hide its text.
        source.dataset.diagramError = 'true';
        // Mermaid leaves its scratch element (`d` + the render id) behind on a parse error.
        document.getElementById(`ddiagram-${count}`)?.remove();
      }
    }
  });
}
