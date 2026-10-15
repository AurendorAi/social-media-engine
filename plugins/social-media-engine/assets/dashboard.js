"use strict";
const token = location.hash.slice(1) || sessionStorage.getItem("sme-token");
if (token) sessionStorage.setItem("sme-token", token);
history.replaceState(null, "", location.pathname);
let state,
  step = null,
  selectedItem = null,
  filter = "all",
  search = "";
let refreshing = false;
let resourceQuery = "",
  resourceKind = "photo",
  resourceProvider = "openverse";
const blobs = [],
  previewObservers = [];
const $ = (id) => document.getElementById(id);
const statusLabels = {
  READY: "Brand ready",
  ONBOARDING_REQUIRED: "Let's get started",
  BRAND_REVIEW: "Review your brand",
  DRAFT: "In progress",
  REVIEW: "Ready for review",
  APPROVED: "Approved",
  CHANGES_REQUESTED: "Changes requested",
  STALE: "Needs a fresh review",
  PUBLISHED: "Published",
  SCHEDULED: "Scheduled",
};
const statusOf = (i) => i.effective_status || i.status;
const readable = (s) =>
  statusLabels[s] ||
  String(s || "Unknown")
    .replaceAll("_", " ")
    .toLowerCase();
function node(tag, value, cls) {
  const n = document.createElement(tag);
  if (value !== undefined) n.textContent = value;
  if (cls) n.className = cls;
  return n;
}
function notice(message, error = false) {
  $("notice").textContent = message;
  $("notice").className = error ? "error" : "";
}
async function api(route, body) {
  const response = await fetch(route, {
    method: body ? "POST" : "GET",
    headers: {
      Authorization: "Bearer " + token,
      ...(body ? { "Content-Type": "application/json" } : {}),
    },
    ...(body ? { body: JSON.stringify(body) } : {}),
  });
  const result = await response.json();
  if (!response.ok) throw Error(result.error);
  return result;
}
function button(label, fn, secondary = false) {
  const b = node("button", label, secondary ? "secondary" : "");
  b.type = "button";
  b.onclick = async () => {
    b.disabled = true;
    try {
      await fn();
    } catch (e) {
      notice(e.message, true);
    } finally {
      b.disabled = b.canEnable ? !b.canEnable() : false;
    }
  };
  return b;
}
function action(label, fn, secondary = false) {
  return button(
    label,
    async () => {
      await fn();
      await refresh();
    },
    secondary,
  );
}
function actor() {
  return state.brand.profile?.answers.approval_owner || "workspace owner";
}
function card(title, body) {
  const c = node("article", undefined, "card");
  c.append(node("h3", title));
  if (body) c.append(node("p", body));
  return c;
}
function tab(name) {
  document.querySelectorAll(".tab").forEach((n) => (n.hidden = n.id !== name));
  document
    .querySelectorAll("nav button")
    .forEach((n) =>
      n.setAttribute("aria-current", n.dataset.tab === name ? "page" : "false"),
    );
  if (name === "library") designLibrary();
  if (["brand", "plans", "learning", "activity", "library"].includes(name))
    $("more-tools").open = true;
}
document
  .querySelectorAll("nav button")
  .forEach((n) => (n.onclick = () => tab(n.dataset.tab)));
function clearPreviews() {
  previewObservers.splice(0).forEach((o) => o.disconnect());
  blobs.splice(0).forEach(URL.revokeObjectURL);
}
async function refresh() {
  if (refreshing) return;
  refreshing = true;
  try {
    const next = await api("/api/state");
    clearPreviews();
    state = next;
    $("brand-name").textContent =
      state.brand.profile?.answers.name || "Make it unmistakably yours.";
    $("brand-name").dir = "auto";
    $("state").textContent = readable(state.brand.state);
    overview();
    brandForm();
    creativeMemory();
    styleOptions();
    content();
    plans();
    learning();
    publishing();
    results();
    activity();
    if (!$("library").hidden) designLibrary();
  } finally {
    refreshing = false;
  }
}
function dateLabel(date) {
  try {
    return new Date(date).toLocaleString(undefined, {
      timeZone: state.brand.profile?.answers.timezone,
      dateStyle: "medium",
      timeStyle: "short",
    });
  } catch {
    return date;
  }
}
function openItem(id) {
  selectedItem = id;
  filter = "all";
  search = "";
  content();
  tab("content");
}
function overview() {
  const root = $("overview");
  root.replaceChildren();
  const ready = state.brand.state === "READY";
  const review = state.items.filter(
    (i) => statusOf(i) === "REVIEW" && reviewComplete(i),
  );
  const approved = state.items.filter((i) => statusOf(i) === "APPROVED");
  const intro = card(
    !ready
      ? "A few answers. A studio that knows you."
      : review.length
        ? "Your next decision is a creative one."
        : "Make something worth stopping for.",
    !ready
      ? "Bring your existing identity, a few references, or just an idea of how you want to feel. We'll build from there."
      : review.length
        ? `${review.length} post${review.length === 1 ? " is" : "s are"} ready for a closer look. Open one, review its artwork and captions, then approve or leave a note.`
        : "Plan and create with your assistant in Codex or Claude. Your brand and feedback stay here, ready for the next conversation.",
  );
  intro.classList.add("hero");
  intro.append(
    button(
      !ready
        ? "Set up my brand"
        : review.length
          ? "Review next post"
          : "See content plans",
      () =>
        !ready
          ? tab("brand")
          : review.length
            ? openItem(review[0].id)
            : tab("plans"),
    ),
  );
  root.append(intro);
  const grid = node("div", undefined, "grid");
  [
    [state.items.length, "Posts in the studio"],
    [review.length, "Ready for your review"],
    [approved.length, "Approved for export"],
  ].forEach(([n, t]) => {
    const c = card(t);
    c.append(node("div", String(n), "number"));
    grid.append(c);
  });
  root.append(grid);
  if (ready && state.creative_memory && state.creative_memory.state !== "CALIBRATED") {
    const calibration = card(
      "Give this brand its own creative direction",
      state.creative_memory.state === "STALE"
        ? "Your brand, feedback or sample files changed. Ask your assistant to refresh your creative brief before the next batch."
        : "Ask your assistant to develop a creative brief and show you a few actual samples. Your approved choices will guide future content for this brand.",
    );
    calibration.append(button("See creative direction", () => tab("brand"), true));
    root.append(calibration);
  }
  const recent = card("On your desk");
  if (!state.items.length)
    recent.append(
      node(
        "p",
        "No posts yet. Once your brand is ready, ask your assistant for a small first batch.",
      ),
    );
  state.items
    .slice(-6)
    .reverse()
    .forEach((i) => {
      const row = node("div", undefined, "post-row");
      const text = node("div");
      text.append(
        node("strong", i.title),
        node("p", readable(statusOf(i)), "meta"),
      );
      row.append(
        text,
        button("Open post", () => openItem(i.id), true),
      );
      recent.append(row);
    });
  root.append(recent);
  const prompt = card(
    "Continue with your assistant",
    "Try: “Use Social Media Engine to plan next week from my saved brand. Give each post a clear idea, useful payoff and a distinct visual concept.”",
  );
  root.append(prompt);
}
function creativeMemory() {
  const root = $("creative-memory");
  root.replaceChildren();
  const memory = state.creative_memory;
  if (!memory) return;
  const labels = {
    MISSING: "Let's find your creative direction",
    PROPOSED: "Creative direction awaiting your review",
    APPROVED: "Creative brief approved · samples still needed",
    CALIBRATED: "Creative brief and sample references approved",
    STALE: "Creative direction needs a fresh review",
  };
  const panel = card(labels[memory.state] || "Your creative direction",
    "Work with your assistant to save the audience situation, proof, voice examples and visual principles that make this brand distinct. Review the actual samples before approving the direction.");
  const active = memory.active;
  if (active) {
    const brief = active.brief;
    const details = node("details");
    details.append(node("summary", "Read your approved creative brief"));
    [["Audience situation", brief.audience_situation], ["Brand promise", brief.brand_promise],
      ["Asset approach", brief.asset_strategy]].forEach(([label, value]) => {
      details.append(node("h4", label), node("p", value));
    });
    [["Proof", brief.proof_points], ["Visual principles", brief.visual_principles],
      ["Content pillars", brief.content_pillars], ["Avoid", brief.anti_patterns],
      ["Success criteria", brief.success_criteria], ["Sources and limits", brief.source_notes]].forEach(([label, values]) => {
      details.append(node("h4", label));
      const list = node("ul");
      values.forEach(value => list.append(node("li", value)));
      details.append(list);
    });
    for (const [category, rows] of Object.entries(brief.voice_examples)) {
      details.append(node("h4", category === "good" ? "Voice to use" : "Voice to avoid"));
      rows.forEach(row => details.append(node("blockquote", row.text), node("p", row.why)));
    }
    details.append(node("p", `${active.sample_asset_ids.length} approved sample reference(s). Each new post still needs its own review.`, "meta"));
    panel.append(details);
  }
  if (memory.state === "PROPOSED")
    panel.append(node("p", "Ask your assistant to show the proposed brief and its samples so you can review the exact version together."));
  if (memory.state === "STALE")
    panel.append(node("p", "The previous direction is kept in history but will not guide new content until a refreshed version is approved."));
  root.append(panel);
}
const fieldInfo = {
  name: ["What's your brand called?", "Your business or creator name"],
  description: [
    "What do you do, and what makes it different?",
    "Describe it as you would to a new customer",
  ],
  industry: ["What field are you in?", "Food, architecture, education…"],
  website: ["Website (optional)", "https://…"],
  offers: ["What do you offer?", "One product or service per line"],
  competitors: ["Other brands in your space (optional)", "One per line"],
  audiences: [
    "Who should this content help?",
    "Describe real people, their needs and questions",
  ],
  markets: ["Where are your customers?", "One market per line"],
  languages: ["Which languages?", "One language code per line: en, ar, ja…"],
  voice: [
    "How should you sound?",
    "Warm and plainspoken? Precise and expert? Include dialect if relevant.",
  ],
  claims_policy: [
    "What must we be careful about saying?",
    "Claims needing evidence, promises to avoid, sensitive subjects",
  ],
  preferred_terms: ["Words you like (optional)", "One per line"],
  forbidden_words: ["Words to avoid (optional)", "One per line"],
  identity_status: ["Do you have a visual identity?", ""],
  design_personality: [
    "How should your designs feel?",
    "Choose a few words and why: calm, playful, bold, refined, practical…",
  ],
  reference_notes: [
    "What do you like in your references?",
    "For each example: what to borrow, what to avoid, and why it fits your audience",
  ],
  style_direction: [
    "Chosen direction",
    "Choose a direction below, or describe your existing approved style",
  ],
  colors: ["Brand colors (optional)", "One hex code per line, such as #173C34"],
  fonts: [
    "Brand fonts (optional)",
    "Font names, languages and licensing notes",
  ],
  logo_policy: [
    "How should your name or logo appear?",
    "If you have no logo, you can choose a simple typeset name",
  ],
  visual_style: [
    "What should the design look like?",
    "Hierarchy, layout, texture and overall feeling",
  ],
  imagery_style: [
    "What kind of images fit?",
    "Real products, people, illustrations, diagrams…",
  ],
  motion_style: [
    "How should video move? (optional)",
    "Pace, sound, captions, subjects to show",
  ],
  references: [
    "Reference links or filenames (optional)",
    "One per line; add files below",
  ],
  avoid: ["Styles to avoid (optional)", "What doesn't feel like your brand?"],
  asset_notes: [
    "Notes about your files (optional)",
    "What can be used and how",
  ],
  goals: [
    "What should content help you achieve?",
    "One practical goal per line",
  ],
  platforms: [
    "Where do you want to post?",
    "One lowercase platform per line: instagram, linkedin, facebook…",
  ],
  cadence: [
    "What pace is realistic?",
    "For example, two posts and three Stories per week",
  ],
  timezone: ["Your time zone", "An IANA name, such as Europe/London"],
  approval_owner: [
    "Who reviews the finished work?",
    "Name of the person approving this brand",
  ],
};
const groupTitles = {
  business: "Your business",
  audience: "Your people",
  voice: "Your voice",
  visual: "Your visual world",
  strategy: "Your goals",
};
async function saveBrandForm() {
  const values = {};
  new FormData($("brand-form")).forEach((v, k) => {
    if (v.trim())
      values[k] = state.list_fields.includes(k)
        ? v
            .split("\n")
            .map((s) => s.trim())
            .filter(Boolean)
        : v.trim();
    else if (state.list_fields.includes(k) && !state.required.includes(k))
      values[k] = [];
  });
  if (Object.keys(values).length)
    await api("/api/brand", {
      answers: values,
      actor: values.approval_owner || actor(),
    });
}
function brandForm() {
  const form = $("brand-form");
  form.replaceChildren();
  const answers = state.brand.profile?.answers || {};
  const groups = Object.keys(state.questionnaire);
  if (step === null) step = Math.max(0, groups.indexOf(state.brand.next_group));
  step = Math.min(step, groups.length - 1);
  const group = groups[step];
  const progress = $("brand-progress");
  progress.replaceChildren(
    node(
      "p",
      `Step ${step + 1} of ${groups.length} · ${groupTitles[group]}`,
      "eyebrow",
    ),
  );
  const steps = node("div", undefined, "steps");
  groups.forEach((g, i) => {
    const b = button(
      `${i + 1}. ${groupTitles[g]}`,
      async () => {
        await saveBrandForm();
        step = i;
        await refresh();
      },
      true,
    );
    b.setAttribute("aria-current", i === step ? "step" : "false");
    steps.append(b);
  });
  progress.append(steps);
  const set = node("fieldset");
  set.append(node("legend", groupTitles[group]));
  const optional = node("details", undefined, "optional-fields");
  optional.append(node("summary", "More detail (optional)"));
  const extra = node("div", undefined, "field-grid");
  optional.append(extra);
  state.questionnaire[group].forEach((f) => {
    const [title, hint] = fieldInfo[f] || [f.replaceAll("_", " "), ""];
    const label = node(
      "label",
      title + (state.required.includes(f) ? " *" : ""),
    );
    let input;
    if (f === "identity_status") {
      input = node("select");
      [
        ["", "Choose one"],
        ["existing", "I have brand guidelines"],
        ["partial", "I have some assets or references"],
        ["new", "I'm starting from scratch"],
      ].forEach(([v, t]) => {
        const o = node("option", t);
        o.value = v;
        input.append(o);
      });
    } else {
      input = node(
        ["name", "industry", "website", "timezone", "approval_owner"].includes(
          f,
        )
          ? "input"
          : "textarea",
      );
      input.placeholder = hint;
    }
    input.name = f;
    input.value = Array.isArray(answers[f])
      ? answers[f].join("\n")
      : answers[f] || "";
    input.dir = "auto";
    label.append(input);
    if (state.list_fields.includes(f))
      label.append(node("span", "One entry per line", "hint"));
    const core =
      state.required.includes(f) ||
      [
        "identity_status",
        "design_personality",
        "reference_notes",
        "references",
      ].includes(f);
    (core ? set : extra).append(label);
  });
  form.append(set);
  if (extra.children.length) form.append(optional);
  if (group === "visual")
    form.append(
      node(
        "p",
        "No guidelines yet? Tell your assistant how you want to feel and share any references. It can prepare 2–4 directions for you below. Save what you know; you don't have to invent design terminology.",
        "help",
      ),
    );
  const actions = node("div", undefined, "actions");
  const save = node("button", "Save progress");
  save.type = "submit";
  actions.append(save);
  if (step < groups.length - 1)
    actions.append(
      button(
        "Save & continue",
        async () => {
          await saveBrandForm();
          step++;
          await refresh();
        },
        true,
      ),
    );
  form.append(actions);
  form.onsubmit = async (e) => {
    e.preventDefault();
    try {
      await saveBrandForm();
      notice("Progress saved. You can come back whenever you're ready.");
      await refresh();
    } catch (err) {
      notice(err.message, true);
    }
  };
  if (state.brand.state === "BRAND_REVIEW" || state.brand.state === "READY") {
    const brief = card(
      "Your brand, at a glance",
      "Review these saved answers before approving. Save any edits first.",
    );
    const dl = node("dl");
    Object.entries(answers).forEach(([f, v]) => {
      dl.append(
        node("dt", fieldInfo[f]?.[0] || f),
        node("dd", Array.isArray(v) ? v.join(" · ") : v),
      );
    });
    const details = node("details");
    details.append(node("summary", "Read the saved brand brief"), dl);
    brief.append(details);
    if (state.brand.state === "BRAND_REVIEW") {
      const label = node("label", undefined, "check-label");
      const check = node("input");
      check.type = "checkbox";
      label.append(
        check,
        node("span", "I have reviewed the saved brand brief."),
      );
      const approve = action("Approve this brand profile", async () => {
        await api("/api/brand-approve", {
          hash: state.brand.profile.hash,
          actor: actor(),
        });
        notice(
          "Brand approved. Ask your assistant to create your first sample.",
        );
      });
      approve.canEnable = () => check.checked;
      approve.disabled = true;
      check.onchange = () => (approve.disabled = !check.checked);
      brief.append(label, approve);
    }
    form.append(brief);
  }
  const list = $("asset-list");
  list.replaceChildren();
  state.assets
    .filter((a) => !["output", "material"].includes(a.role))
    .forEach((a) =>
      list.append(node("p", a.name + " · " + a.role + " · " + a.rights)),
    );
}
function styleOptions() {
  const root = $("style-options");
  root.replaceChildren();
  const boards = (state.styles || []).filter(
    (b) => b.brand_hash === state.brand.profile?.hash,
  );
  if (!boards.length) return;
  root.append(
    node("h2", "Find your direction"),
    node(
      "p",
      "These are creative proposals. Choosing one updates your saved brand; it still needs your review. Ask your assistant for rendered samples before a full batch.",
    ),
  );
  boards.forEach((board) => {
    const grid = node("div", undefined, "direction-grid");
    board.options.forEach((o) => {
      const c = card(o.title, o.rationale);
      const palette = node("canvas");
      palette.width = 240;
      palette.height = 40;
      palette.setAttribute("role", "img");
      palette.setAttribute(
        "aria-label",
        "Palette: " + o.profile.colors.join(", "),
      );
      const ctx = palette.getContext("2d");
      o.profile.colors.forEach((color, i) => {
        ctx.fillStyle = color;
        ctx.fillRect(
          (i * 240) / o.profile.colors.length,
          0,
          240 / o.profile.colors.length,
          40,
        );
      });
      c.append(
        palette,
        node("p", o.profile.visual_style),
        node("p", "Imagery: " + o.profile.imagery_style),
        node("p", "Fonts: " + o.profile.fonts.join(", "), "meta"),
        node("p", "Tradeoff: " + o.tradeoff, "meta"),
        action("Choose " + o.title, async () => {
          await api("/api/style-select", {
            id: board.id,
            option: o.id,
            hash: board.hash,
            actor: actor(),
          });
          notice(
            "Direction saved. Review your updated brand brief before approving.",
          );
        }),
      );
      grid.append(c);
    });
    root.append(grid);
  });
}
$("upload-form").onsubmit = async (e) => {
  e.preventDefault();
  const submit = e.target.querySelector("button");
  submit.disabled = true;
  try {
    const f = new FormData(e.target),
      file = f.get("file");
    if (!file.size) throw Error("Choose a non-empty file.");
    if (file.size > 20 * 1024 * 1024)
      throw Error(
        "Browser uploads are limited to 20 MB. Ask your assistant to import larger files.",
      );
    const bytes = new Uint8Array(await file.arrayBuffer());
    let binary = "";
    for (let i = 0; i < bytes.length; i += 8192)
      binary += String.fromCharCode(...bytes.subarray(i, i + 8192));
    await api("/api/asset", {
      name: file.name,
      base64: btoa(binary),
      role: f.get("role"),
      rights: f.get("rights"),
      note: f.get("note"),
      actor: actor(),
    });
    e.target.reset();
    notice(
      "Asset added. Ask your assistant to read it and review the updated brand.",
    );
    await refresh();
  } catch (err) {
    notice(err.message, true);
  } finally {
    submit.disabled = false;
  }
};
async function preview(asset, container, alt) {
  const ext = asset.path.split(".").pop();
  if (
    !["png", "jpg", "jpeg", "webp", "mp4", "webm"].includes(ext) &&
    !(ext === "svg" && asset.role === "material")
  ) {
    container.append(
      node("p", asset.name + " — ask your assistant to open this file."),
    );
    return;
  }
  const slot = node("div", undefined, "media-slot");
  container.append(slot);
  slot.textContent = "Loading preview…";
  try {
    const r = await fetch("/api/asset?id=" + encodeURIComponent(asset.id), {
      headers: { Authorization: "Bearer " + token },
    });
    if (!r.ok) throw Error();
    const url = URL.createObjectURL(await r.blob());
    if (!slot.isConnected) {
      URL.revokeObjectURL(url);
      return;
    }
    blobs.push(url);
    const n = node(["mp4", "webm"].includes(ext) ? "video" : "img");
    n.src = url;
    slot.replaceChildren();
    if (n.tagName === "VIDEO") {
      n.controls = true;
      n.preload = "metadata";
      slot.append(n);
    } else {
      n.alt = alt || asset.name;
      const a = node("a");
      a.href = url;
      a.target = "_blank";
      a.rel = "noopener";
      a.title = "Open original-size image";
      a.append(n);
      slot.append(a);
    }
  } catch {
    slot.textContent =
      "Preview unavailable. Ask your assistant to inspect the local file.";
  }
}
function reviewComplete(item) {
  return (
    (item.required_review_roles || []).length > 0 &&
    item.required_review_roles.every((role) =>
      state.reviews.some(
        (r) =>
          r.item_id === item.id &&
          r.item_hash === item.hash &&
          r.role === role &&
          r.decision === "pass",
      ),
    )
  );
}
function content() {
  clearPreviews();
  const root = $("content");
  root.replaceChildren(node("h2", "Give the work a closer look."));
  const toolbar = node("div", undefined, "review-toolbar");
  const label = node("label", "Show posts");
  const select = node("select");
  select.setAttribute("aria-label", "Show posts");
  [
    ["all", "All posts"],
    ["REVIEW", "Ready for review"],
    ["CHANGES_REQUESTED", "Changes requested"],
    ["APPROVED", "Approved"],
    ["DRAFT", "In progress"],
    ["STALE", "Needs a fresh review"],
  ].forEach(([v, t]) => {
    const o = node("option", t);
    o.value = v;
    select.append(o);
  });
  select.value = filter;
  select.onchange = () => {
    filter = select.value;
    selectedItem = null;
    content();
  };
  label.append(select);
  toolbar.append(label);
  const sl = node("label", "Find a post");
  const input = node("input");
  input.type = "search";
  input.value = search;
  input.placeholder = "Search titles";
  input.onchange = () => {
    search = input.value;
    selectedItem = null;
    content();
  };
  sl.append(input);
  toolbar.append(sl);
  root.append(toolbar);
  const items = state.items.filter(
    (i) =>
      (filter === "all" || statusOf(i) === filter) &&
      i.title.toLowerCase().includes(search.toLowerCase()),
  );
  if (!items.length) {
    root.append(
      node(
        "p",
        state.items.length
          ? "No posts match this view."
          : "Your first drafts will appear here after your assistant saves them.",
        "empty",
      ),
    );
    return;
  }
  if (!items.some((i) => i.id === selectedItem)) selectedItem = items[0].id;
  const layout = node("div", undefined, "review-layout");
  const list = node("div", undefined, "post-list");
  list.setAttribute("aria-label", "Posts");
  items.forEach((i) => {
    const b = button(
      i.title + " · " + readable(statusOf(i)),
      () => {
        selectedItem = i.id;
        content();
      },
      true,
    );
    b.setAttribute("aria-pressed", String(i.id === selectedItem));
    list.append(b);
  });
  layout.append(list);
  const item = items.find((i) => i.id === selectedItem);
  const c = card(item.title);
  c.classList.add("post-detail");
  c.append(
    node(
      "p",
      readable(statusOf(item)) + " · Revision " + item.revision,
      "meta",
    ),
  );
  if (item.material_ids?.length) {
    const sources = node("details");
    sources.append(node("summary", "Design materials & credits"));
    item.material_ids.forEach((id) => {
      const material = state.assets.find((a) => a.id === id);
      const p = material?.provenance;
      if (!p) return;
      sources.append(
        node("p", p.title + " · " + p.creator),
        sourceLink("Original source", p.source_url),
        node("p", p.rights_review.attribution),
      );
    });
    c.append(sources);
  }
  if (item.blocked_reason) c.append(node("p", item.blocked_reason, "help"));
  const vl = node("label", "Platform & language");
  const variants = node("select");
  variants.setAttribute("aria-label", "Platform & language");
  item.variants.forEach((v, i) => {
    const o = node(
      "option",
      v.platform + " · " + v.language + " · " + v.format,
    );
    o.value = i;
    variants.append(o);
  });
  vl.append(variants);
  c.append(vl);
  const variantRoot = node("div");
  c.append(variantRoot);
  function showVariant() {
    clearPreviews();
    variantRoot.replaceChildren();
    const v = item.variants[Number(variants.value)];
    const assets = (v.asset_ids || []).map((id) =>
      state.assets.find((a) => a.id === id),
    );
    let index = 0;
    const media = node("div", undefined, "media");
    const controls = node("div", undefined, "slide-controls");
    function showSlide() {
      media.replaceChildren();
      controls.replaceChildren();
      if (assets[index]) preview(assets[index], media, v.alt_text?.[index]);
      else if (assets.length)
        media.append(
          node("p", "Artwork is unavailable. Ask your assistant to repair it."),
        );
      if (assets.length > 1) {
        const prev = button(
          "Previous slide",
          () => {
            index--;
            showSlide();
          },
          true,
        );
        prev.disabled = index === 0;
        const next = button(
          "Next slide",
          () => {
            index++;
            showSlide();
          },
          true,
        );
        next.disabled = index === assets.length - 1;
        controls.append(
          prev,
          node("span", `${index + 1} / ${assets.length}`),
          next,
        );
      }
    }
    showSlide();
    variantRoot.append(media, controls);
    const caption = node("p", v.caption, "caption");
    caption.dir = "auto";
    variantRoot.append(node("h3", "Caption"), caption);
  }
  variants.onchange = showVariant;
  const eligible =
    reviewComplete(item) &&
    !item.blocked_reason &&
    !["STALE", "CHANGES_REQUESTED"].includes(statusOf(item));
  const approved = statusOf(item) === "APPROVED";
  const gate = node(
    "p",
    approved
      ? "This exact revision is approved."
      : eligible
        ? "Checks complete. Review the artwork and every platform caption before approving."
        : "Production review is still needed. You can leave feedback while your assistant completes it.",
    "help",
  );
  c.append(gate);
  const checkLabel = node("label", undefined, "check-label");
  const check = node("input");
  check.type = "checkbox";
  checkLabel.append(
    check,
    node(
      "span",
      "I reviewed this revision, including every slide, video and caption.",
    ),
  );
  if (!approved) c.append(checkLabel);
  const release = button(
    approved ? "Export approved package" : "Approve this revision",
    async () => {
      try {
        if (approved) {
          const r = await api("/api/export", { id: item.id });
          notice("Package exported: " + r.directory);
        } else {
          await api("/api/item-approve", {
            id: item.id,
            hash: item.hash,
            actor: actor(),
            confirmed: check.checked,
          });
          notice(
            "Revision approved. Publishing requires a separate confirmed schedule.",
          );
        }
        await refresh();
      } finally {
        if (!approved) release.disabled = !eligible || !check.checked;
      }
    },
  );
  release.canEnable = () => approved || (eligible && check.checked);
  release.disabled = !approved;
  check.onchange = () => (release.disabled = !eligible || !check.checked);
  c.append(release);
  c.append(feedbackForm(item));
  const details = node("details", undefined, "review-evidence");
  details.append(node("summary", "Review notes & previous revisions"));
  state.reviews
    .filter((r) => r.item_id === item.id && r.item_hash === item.hash)
    .forEach((r) =>
      details.append(
        node(
          "p",
          r.role + ": " + r.decision + " — " + r.observations.join(" · "),
        ),
      ),
    );
  (state.revisions || [])
    .filter((r) => r.id === item.id)
    .sort((a, b) => b.revision - a.revision)
    .forEach((r) => {
      details.append(node("strong", "Revision " + r.revision));
      r.variants.forEach((v) => {
        const old = node(
          "p",
          v.platform + " / " + v.language + ": " + v.caption,
        );
        old.dir = "auto";
        details.append(old);
      });
    });
  c.append(details);
  layout.append(c);
  root.append(layout);
  showVariant();
}
function feedbackForm(item) {
  const form = node("form");
  const label = node("label", "What should change?");
  const note = node("textarea");
  note.required = true;
  note.name = "feedback";
  note.placeholder =
    "Be specific: the idea, wording, imagery, spacing or pace…";
  label.append(note);
  form.append(label);
  const kindLabel = node("label", "Your decision");
  const kind = node("select");
  kind.name = "disposition";
  [
    ["change-request", "Request changes"],
    ["rejected", "Reject this draft"],
    ["note", "Leave a note"],
  ].forEach(([value, title]) => {
    const o = node("option", title);
    o.value = value;
    kind.append(o);
  });
  kindLabel.append(kind);
  form.append(kindLabel);
  const rl = node("label", "Rating (optional)");
  const rating = node("select");
  rating.name = "rating";
  [
    ["", "Not rated"],
    ["1", "1 / 5"],
    ["2", "2 / 5"],
    ["3", "3 / 5"],
    ["4", "4 / 5"],
    ["5", "5 / 5"],
  ].forEach(([value, title]) => {
    const o = node("option", title);
    o.value = value;
    rating.append(o);
  });
  rl.append(rating);
  form.append(rl);
  const b = node("button", "Save feedback", "secondary");
  b.type = "submit";
  form.append(b);
  form.onsubmit = async (e) => {
    e.preventDefault();
    b.disabled = true;
    try {
      await api("/api/feedback", {
        id: "feedback-" + crypto.randomUUID(),
        instruction: note.value,
        actor: actor(),
        category: "preference",
        scope: { item: item.id },
        disposition: kind.value,
        ...(rating.value ? { rating: Number(rating.value) } : {}),
      });
      notice(
        "Feedback saved for this post. Ask your assistant to revise it; broader preferences can be approved under Feedback & learning.",
      );
      await refresh();
    } catch (err) {
      notice(err.message, true);
    } finally {
      b.disabled = false;
    }
  };
  return form;
}
function plans() {
  const root = $("plans");
  root.replaceChildren(
    node("h2", "A plan with a purpose."),
    node(
      "p",
      "Create or revise plans with your assistant. Dates below are proposed editorial dates, not proof of scheduled publishing.",
    ),
  );
  if (!state.plans.length)
    root.append(
      card(
        "Start small. Make it useful.",
        "Ask: “Plan next week for my brand, within my capacity. Include the audience need, original angle, useful takeaway, evidence, format and visual idea for each post.”",
      ),
    );
  state.plans.forEach((p) => {
    const c = card(p.month, p.strategy);
    if (p.brand_hash !== state.brand.profile?.hash)
      c.append(
        node(
          "p",
          "This plan uses an older brand identity. Ask your assistant to refresh it.",
          "help",
        ),
      );
    p.items.forEach((i) => {
      const row = node("details", undefined, "entry");
      row.append(node("summary", dateLabel(i.scheduled_at) + " · " + i.title));
      row.append(
        node("p", i.objective),
        node("p", i.message),
        node(
          "p",
          `${i.format} · ${i.platforms.join(", ")} · ${i.language}`,
          "meta",
        ),
        node("p", "Next step: " + i.cta),
      );
      if (state.items.some((it) => it.id === i.id))
        row.append(button("Open draft", () => openItem(i.id), true));
      c.append(row);
    });
    root.append(c);
  });
}
function learning() {
  const root = $("learning");
  root.replaceChildren(
    node("h2", "Teach it what matters."),
    node(
      "p",
      "A note about one post stays with that post. Ask your assistant to propose a broader preference if you want future work to follow it.",
    ),
  );
  if (!state.rules.length)
    root.append(node("p", "Your feedback will appear here.", "empty"));
  state.rules.forEach((r) => {
    const c = card(r.instruction);
    c.append(
      node(
        "p",
        r.category +
          " · " +
          (Object.keys(r.scope).length
            ? Object.entries(r.scope)
                .map(([k, v]) => k + ": " + v)
                .join(" · ")
            : "All brand content") +
          " · " +
          (r.retired ? "Retired" : r.approved ? "Approved" : "Proposed"),
        "meta",
      ),
    );
    if (!r.retired) {
      const actions = node("div", undefined, "rule-actions");
      if (!r.approved)
        actions.append(
          action("Approve rule", () =>
            api("/api/rule-approve", { id: r.id, actor: actor() }),
          ),
        );
      actions.append(
        action(
          "Retire rule",
          () => api("/api/rule-retire", { id: r.id, actor: actor() }),
          true,
        ),
      );
      c.append(actions);
    }
    root.append(c);
  });
}
function publishing() {
  const root = $("publishing");
  root.replaceChildren(
    node("h2", "Ready when you are."),
    node(
      "p",
      "Export approved files for manual posting, or ask your assistant to prepare an exact schedule through your connected provider.",
    ),
  );
  const approved = state.items.filter((i) => statusOf(i) === "APPROVED");
  if (!approved.length && !state.dispatches.length)
    root.append(
      card(
        "Nothing queued yet",
        "Approve a finished post in Review posts to make its export available.",
      ),
    );
  approved.forEach((i) => {
    const c = card(
      i.title,
      "Approved files and captions, ready for manual handoff.",
    );
    c.append(
      action("Export approved package", async () => {
        const r = await api("/api/export", { id: i.id });
        notice("Package exported: " + r.directory);
      }),
    );
    root.append(c);
  });
  state.dispatches.forEach((d) => {
    const c = card(
      state.items.find((i) => i.id === d.item_id)?.title || d.item_id,
    );
    c.append(
      node("p", readable(d.status) + " · " + dateLabel(d.date)),
      node("p", d.publication_status || "No confirmed publication"),
    );
    const details = node("details");
    details.append(
      node("summary", "Delivery record"),
      node("p", d.operation + " · " + d.date),
      node("p", "Local cancellation does not cancel a provider's schedule."),
    );
    c.append(details);
    root.append(c);
  });
}
function results() {
  const root = $("results");
  root.replaceChildren(
    node("h2", "Learn from what happened."),
    node(
      "p",
      "Results are saved observations, not a live refresh. Compare the same platform and format at similar post age.",
    ),
  );
  if (!state.metrics.length)
    root.append(
      card(
        "No results imported yet",
        "Ask your assistant to import your actual platform analytics or a report. Missing numbers stay unknown.",
      ),
    );
  state.metrics
    .slice(-6)
    .reverse()
    .forEach((r) => {
      const c = card(
        r.platform +
          " · " +
          (r.synthetic ? "Practice data" : "Recorded results"),
        "Captured " + dateLabel(r.captured_at),
      );
      const dl = node("dl", undefined, "metric-list");
      Object.entries(r.metrics).forEach(([k, v]) => {
        dl.append(
          node("dt", k.replaceAll("_", " ")),
          node(
            "dd",
            v === null
              ? "Unavailable"
              : typeof v === "object"
                ? JSON.stringify(v)
                : String(v),
          ),
        );
      });
      c.append(dl);
      root.append(c);
    });
  if (state.metrics.length > 6) {
    const more = node("details");
    more.append(node("summary", "Earlier observations"));
    state.metrics
      .slice(0, -6)
      .forEach((r) =>
        more.append(
          node("p", r.platform + " · " + r.captured_at),
          node("pre", JSON.stringify(r.metrics, null, 2)),
        ),
      );
    root.append(more);
  }
}
function activity() {
  const root = $("activity");
  root.replaceChildren(node("h2", "Workspace history"));
  state.events.forEach((e) =>
    root.append(
      node(
        "p",
        dateLabel(e.created) + " · " + e.action + " · " + e.subject,
        "meta",
      ),
    ),
  );
}
$("refresh-work").onclick = async () => {
  const control = $("refresh-work");
  control.disabled = true;
  try {
    await refresh();
    notice("Loaded the latest saved work.");
  } catch (e) {
    notice(e.message, true);
  } finally {
    control.disabled = false;
  }
};
refresh().catch((e) => notice(e.message, true));

function sourceLink(label, url) {
  const a = node("a", label);
  try {
    if (new URL(url).protocol !== "https:") return node("span", label);
    a.href = url;
    a.target = "_blank";
    a.rel = "noopener noreferrer";
  } catch {
    return node("span", label);
  }
  return a;
}
function designLibrary() {
  const root = $("library");
  root.replaceChildren(
    node("h2", "Find the ingredients for your next idea."),
    node(
      "p",
      "Photography, textures, patterns, illustrations and icons. Start with a clear visual direction; your assistant helps choose and compose the right materials.",
    ),
  );
  const form = node("form", undefined, "card resource-search");
  const queryLabel = node("label", "What are you looking for?");
  const query = node("input");
  query.name = "resource-query";
  query.required = true;
  query.maxLength = 500;
  query.placeholder = "Warm paper grain, subtle texture";
  query.value = resourceQuery;
  queryLabel.append(query);
  const kindLabel = node("label", "Material type"),
    kind = node("select");
  kind.name = "resource-kind";
  kind.setAttribute("aria-label", "Material type");
  ["photo", "illustration", "icon", "texture", "pattern", "graphic"].forEach(
    (k) => {
      const o = node("option", k);
      o.value = k;
      kind.append(o);
    },
  );
  kind.value = resourceKind;
  kindLabel.append(kind);
  const providerLabel = node("label", "Search in"),
    provider = node("select");
  provider.name = "resource-provider";
  provider.setAttribute("aria-label", "Search in");
  [
    ["openverse", "Openverse"],
    ["commons", "Wikimedia Commons"],
    ["iconify", "Iconify (icons)"],
    ["met", "The Met Open Access"],
  ].forEach(([v, t]) => {
    const o = node("option", t);
    o.value = v;
    provider.append(o);
  });
  provider.value = resourceProvider;
  providerLabel.append(provider);
  provider.onchange = () => {
    if (provider.value === "iconify") kind.value = "icon";
  };
  kind.onchange = () => {
    if (kind.value !== "icon" && provider.value === "iconify")
      provider.value = "openverse";
  };
  const submit = node("button", "Search materials");
  submit.type = "submit";
  submit.disabled = !state.brand.profile;
  const help = node(
    "p",
    "Only your search words are sent to the selected public service. Avoid private information. Results are candidates; your assistant checks the source, licence and style before downloading.",
    "help",
  );
  form.append(queryLabel, kindLabel, providerLabel, help, submit);
  form.onsubmit = async (e) => {
    e.preventDefault();
    resourceQuery = query.value;
    resourceKind = kind.value;
    resourceProvider = provider.value;
    submit.disabled = true;
    submit.textContent = "Searching…";
    try {
      const result = await api("/api/resource-search", {
        query: resourceQuery,
        kind: resourceKind,
        provider: resourceProvider,
      });
      await refresh();
      notice(
        result.results.length
          ? `${result.results.length} candidates saved. Open their original sources with your assistant to choose materials.${result.skipped ? ` ${result.skipped} unsupported links skipped.` : ""}`
          : "No materials found. Try a more specific query or another library.",
      );
    } catch (e) {
      notice(e.message, true);
    } finally {
      submit.disabled = !state.brand.profile;
      submit.textContent = "Search materials";
    }
  };
  root.append(form);
  const libraries = node("details", undefined, "card");
  libraries.append(node("summary", "Find free design resources & fonts"));
  const sourceFilter = node("input");
  sourceFilter.type = "search";
  sourceFilter.placeholder = "Find a source: paper, Arabic, photography, icons…";
  sourceFilter.setAttribute("aria-label", "Filter design resource sources");
  libraries.append(sourceFilter);
  const sourceRows = [];
  (state.resource_libraries || []).forEach((l) => {
    const row = node("div", undefined, "library-row");
    row.append(
      sourceLink(l.name, l.url),
      node("span", l.kinds.join(" · "), "meta"),
      node("p", l.notes),
      node(
        "p",
        l.access === "api"
          ? "Search here or browse with your assistant."
          : "Browse with your assistant, then add the selected material to this library.",
        "help",
      ),
    );
    if (l.free_scope) row.append(node("p", `Free scope: ${l.free_scope}`, "help"));
    if (l.use_when) row.append(node("p", l.use_when));
    if (l.search_method) row.append(node("p", `Find assets: ${l.search_method}`, "help"));
    if (l.license_url) row.append(sourceLink("Source licence / terms", l.license_url));
    if (l.attribution) row.append(node("p", `Credit: ${l.attribution}`, "help"));
    if (l.restrictions) row.append(node("p", l.restrictions, "help"));
    if (l.verified_date) row.append(node("p", `Source checked ${l.verified_date}; verify the selected asset before use.`, "help"));
    sourceRows.push({row, text: [l.name, ...l.kinds, l.use_when || "", ...(l.style_terms || [])].join(" ").toLowerCase()});
    libraries.append(row);
  });
  const sourceEmpty = node("p", "No matching sources. Try another material or style term.", "help");
  sourceEmpty.hidden = true;
  libraries.append(sourceEmpty);
  sourceFilter.oninput = () => {
    const words = sourceFilter.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
    let visible = 0;
    sourceRows.forEach(({row, text}) => {
      row.hidden = !words.every((word) => text.includes(word));
      if (!row.hidden) visible++;
    });
    sourceEmpty.hidden = visible > 0;
  };
  root.append(libraries);
  const materials = state.assets.filter((a) => a.role === "material");
  root.append(node("h3", `Your materials (${materials.length})`));
  const gallery = node("div", undefined, "grid material-grid");
  materials.forEach((a) => {
    const p = a.provenance,
      c = card(p.title, p.style_fit);
    const image = node("div", undefined, "media");
    c.append(image);
    preview(a, image, p.title);
    c.append(
      sourceLink("Original source", p.source_url),
      node("p", p.rights_review.license_name, "meta"),
    );
    const credits = node("details");
    credits.append(
      node("summary", "Usage & credit"),
      node("p", p.rights_review.intended_use),
      node("p", p.rights_review.attribution),
    );
    c.append(credits);
    gallery.append(c);
  });
  root.append(gallery);
  if (!materials.length)
    root.append(
      node(
        "p",
        "Selected materials will appear here after source review and download. They stay separate from your brand identity files.",
      ),
    );
  const candidates = (state.resources || [])
    .filter((r) => r.status !== "ACQUIRED")
    .slice(-24)
    .reverse();
  root.append(node("h3", "Recent candidates"));
  if (!candidates.length)
    root.append(
      node(
        "p",
        "Search above, or ask your assistant to find materials for a specific post.",
      ),
    );
  candidates.forEach((r) => {
    const c = card(r.title, r.style_fit);
    c.append(
      node("p", `${r.provider} · ${r.kind} · ${r.creator}`, "meta"),
      sourceLink("Inspect original source", r.source_url),
      node(
        "p",
        r.status === "REVIEWED"
          ? "Source review recorded. Ready to download."
          : "Needs source, licence and style review.",
      ),
    );
    if (r.status === "REVIEWED")
      c.append(
        action("Download reviewed material", async () => {
          await api("/api/resource-fetch", {
            id: r.id,
            hash: r.hash,
            actor: actor(),
          });
          notice("Material saved to your design library.");
        }),
      );
    root.append(c);
  });
}
