const FALLBACK_ORIGIN = { lat: 50.0415, lng: 19.9493 };
const MY_WANT_LABEL = {
  spacer: "Spacer",
  pogadac: "Pogadać",
  dom: "W domu",
};
const AVATAR = ["#1f7a4c", "#2e9b63", "#4a8f6a", "#c47b4a", "#3d7a8a", "#6a8f4e"];
const ART = {
  park: "/static/img/park.svg",
  dk: "/static/img/dk.svg",
  swap: "/static/img/swap.svg",
  people: "/static/img/people.svg",
};
const EVENT_DRAW = new Set([
  "kawa",
  "wymiana",
  "spacerek",
  "biblioteka",
  "dk-joga",
  "dk-glina",
  "tata-klub",
  "chusta",
  "lalki",
  "sensoryka",
  "tato-warsztat",
  "kawiarenka",
  "cafe-lipa",
  "cafe-brunch",
]);

function photoFor(item, fallback = "park") {
  if (item?.id && EVENT_DRAW.has(item.id)) return `/static/img/draw/${item.id}.svg?v=20`;
  const src = item?.photo || ART[item?.art] || ART[fallback] || ART.park;
  return src.includes("?") ? src : `${src}?v=20`;
}

const state = {
  origin: FALLBACK_ORIGIN,
  zoom: 14,
  myWant: "spacer",
  filter: "wszyscy",
  similarAge: false,
  needFilters: [],
  starredOnly: false,
  horizon: "wszystkie",
  tab: "poznaj",
  parents: [],
  happenings: [],
  happenFilter: "wszystkie",
  happenPrice: "wszystkie",
  swaps: [],
  swapFilter: "wszystkie",
  places: [],
  placeFilter: "wszystkie",
  profile: null,
  trust: {},
  gateStep: 0,
  areas: [],
  districtId: "podgorze",
  areaId: "stare-podgorze",
  browseDistrictId: "podgorze",
  browseAreaId: "stare-podgorze",
  notices: [],
  threads: [],
  inboxOpen: false,
  email: "",
  radiusM: 500,
};

const RADIUS_STEPS = [500, 1000, 3000, 5000, 10000];
const TIPI_SVG =
  '<svg class="tipi" viewBox="0 0 24 24" aria-hidden="true"><path d="M4.2 11.6 L12 4.2 L19.8 11.6" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/><path d="M6.4 10.8 V19.6 H17.6 V10.8" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><path d="M10.2 19.6 V14.6 H13.8 V19.6" fill="none" stroke="currentColor" stroke-width="1.55" stroke-linejoin="round"/><path d="M3.6 19.6 H20.4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>';

function esc(value) {
  return String(value ?? "").replace(/[&<>"']/g, (ch) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch])
  );
}

function colorFor(id) {
  let n = 0;
  for (const ch of id) n += ch.charCodeAt(0);
  return AVATAR[n % AVATAR.length];
}

function radiusIndex() {
  const i = RADIUS_STEPS.indexOf(state.radiusM);
  return i < 0 ? 0 : i;
}

function radiusLabel(meters) {
  if (meters < 1000) return `${meters} m`;
  const km = meters / 1000;
  return Number.isInteger(km) ? `${km} km` : `${String(km).replace(".", ",")} km`;
}

async function setRadiusByIndex(index) {
  const next = Math.max(0, Math.min(RADIUS_STEPS.length - 1, index));
  if (RADIUS_STEPS[next] === state.radiusM) return;
  state.radiusM = RADIUS_STEPS[next];
  renderChrome();
  await loadVillage();
}

function fillRadiusControl() {
  const range = document.getElementById("radius-range");
  const minus = document.getElementById("radius-minus");
  const plus = document.getElementById("radius-plus");
  const ring = document.getElementById("area-ring");
  const i = radiusIndex();
  if (range) {
    range.value = String(i);
    range.setAttribute("aria-valuetext", radiusLabel(state.radiusM));
  }
  if (minus) minus.disabled = i <= 0;
  if (plus) plus.disabled = i >= RADIUS_STEPS.length - 1;
  if (ring) ring.style.setProperty("--ring-t", String(i / Math.max(1, RADIUS_STEPS.length - 1)));
  document.querySelectorAll("#distance-ticks span").forEach((el, idx) => {
    el.classList.toggle("on", idx === i);
  });
}

function mamWord(n) {
  const mod100 = n % 100;
  const mod10 = n % 10;
  if (n === 1) return "mama";
  if (mod10 >= 2 && mod10 <= 4 && (mod100 < 12 || mod100 > 14)) return "mamy";
  return "mam";
}

function nearbyMomCount() {
  return state.parents.filter((p) => !state.trust[p.id]?.reported).length;
}

function fillAreaCount() {
  const num = document.getElementById("area-count-num");
  const label = document.getElementById("area-count-label");
  if (!num) return;
  const n = nearbyMomCount();
  num.textContent = String(n);
  if (label) label.textContent = mamWord(n);
}

function areaList() {
  return state.areas.length ? state.areas : state.profile?.areas || [];
}

function districtById(id) {
  return areaList().find((d) => d.id === id) || areaList()[0] || null;
}

function areaNode(districtId, areaId) {
  const district = districtById(districtId);
  if (!district) return { ...FALLBACK_ORIGIN, zoom: 14, label: "Podgórze", city: "Kraków" };
  const subs = district.subs || [];
  const sub = subs.find((s) => s.id === areaId);
  if (sub) {
    return { ...sub, district_id: district.id, district_label: district.label, city: district.city };
  }
  return district;
}

function defaultSubId(district) {
  const subs = district?.subs || [];
  if (!subs.length) return "";
  if (district.id === "podgorze") {
    const stare = subs.find((s) => s.id === "stare-podgorze");
    return (stare || subs[0]).id;
  }
  return subs[0].id;
}

function placePhrase(districtId, areaId) {
  const node = areaNode(districtId, areaId);
  if (node.district_label) return `${node.label}, ${node.district_label}`;
  return `${node.label || "Wioska"}, ${node.city || "Kraków"}`;
}

function applyHomePlace(districtId, areaId, persistProfile = true) {
  const district = districtById(districtId) || districtById("podgorze");
  if (!district) return;
  const subs = district.subs || [];
  let nextArea = areaId || "";
  if (subs.length && (!nextArea || nextArea === district.id)) nextArea = defaultSubId(district);
  if (!subs.length) nextArea = "";
  state.districtId = district.id;
  state.areaId = nextArea;
  if (persistProfile && state.profile) {
    state.profile.district_id = district.id;
    state.profile.area_id = nextArea;
    state.profile.district = placePhrase(district.id, nextArea);
  }
}

function applyBrowse(districtId, areaId) {
  const district = districtById(districtId) || districtById("podgorze");
  if (!district) return;
  const subs = district.subs || [];
  const nextArea = subs.some((s) => s.id === areaId) ? areaId : "";
  state.browseDistrictId = district.id;
  state.browseAreaId = nextArea;
  const node = areaNode(district.id, nextArea);
  state.origin = { lat: node.lat, lng: node.lng };
  state.zoom = node.zoom || (nextArea ? 15 : 14);
}

function shouldShowGate() {
  const params = new URLSearchParams(location.search);
  if (params.has("demo") || params.has("start")) return true;
  return !state.profile?.onboarded;
}

async function setBrowse(districtId, areaId) {
  applyBrowse(districtId, areaId);
  renderChrome();
  await loadVillage();
}

function chips(host, items, current, onPick, cls = "chip") {
  if (!host) return;
  host.innerHTML = "";
  items.forEach(([id, label]) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = id === current ? `${cls} on` : cls;
    btn.textContent = label;
    btn.addEventListener("click", () => onPick(id));
    host.appendChild(btn);
  });
}

function renderDistrictCards(hostId, selectedId, onPick) {
  const host = document.getElementById(hostId);
  if (!host) return;
  const list = areaList();
  host.innerHTML = list
    .map(
      (d) => `
    <button type="button" class="district ${d.id === selectedId ? "on" : ""}" data-district="${d.id}">
      <strong>${esc(d.label)}</strong>
      <span>${esc(d.city)}${d.demo ? " · demo na prezentację" : ""}${d.subs?.length ? " · osiedla" : ""}</span>
      ${d.demo ? "<em>Polecane</em>" : ""}
    </button>`
    )
    .join("");
  host.querySelectorAll("[data-district]").forEach((btn) => {
    btn.addEventListener("click", () => onPick(btn.dataset.district));
  });
}

function renderSubChips(hostId, titleId, districtId, areaId, onPick, allowAll) {
  const host = document.getElementById(hostId);
  const title = titleId ? document.getElementById(titleId) : null;
  if (!host) return;
  const district = districtById(districtId);
  const subs = district?.subs || [];
  if (!subs.length) {
    host.innerHTML = "";
    host.hidden = true;
    if (title) title.hidden = true;
    return;
  }
  host.hidden = false;
  if (title) title.hidden = false;
  const items = allowAll
    ? [["", "Cała dzielnica"], ...subs.map((s) => [s.id, s.label])]
    : subs.map((s) => [s.id, s.label]);
  const current = allowAll ? areaId || "" : areaId || defaultSubId(district);
  chips(host, items, current, (id) => onPick(id));
}

function renderBrowsePickers() {
  const list = areaList();
  chips(
    document.getElementById("browse-districts"),
    list.map((d) => [d.id, d.label]),
    state.browseDistrictId,
    (id) => setBrowse(id, ""),
    "mini"
  );
  const district = districtById(state.browseDistrictId);
  const label = document.getElementById("browse-areas-label");
  if (label) label.hidden = !(district?.subs || []).length;
  renderSubChips(
    "browse-areas",
    "browse-areas-label",
    state.browseDistrictId,
    state.browseAreaId,
    (id) => setBrowse(state.browseDistrictId, id),
    true
  );
}

function renderHomePickers() {
  renderDistrictCards("gate-districts", state.districtId, (id) => {
    applyHomePlace(id, defaultSubId(districtById(id)));
    renderGate();
  });
  renderSubChips(
    "gate-areas",
    "gate-areas-title",
    state.districtId,
    state.areaId,
    (id) => {
      applyHomePlace(state.districtId, id);
      renderGate();
    },
    false
  );
  renderDistrictCards("profile-districts", state.districtId, (id) => {
    applyHomePlace(id, defaultSubId(districtById(id)));
    renderHomePickers();
  });
  renderSubChips(
    "profile-areas",
    "profile-areas-title",
    state.districtId,
    state.areaId,
    (id) => {
      applyHomePlace(state.districtId, id);
      renderHomePickers();
    },
    false
  );
}

function visibleHappenings() {
  return state.happenings
    .filter((h) => {
      if (state.horizon !== "wszystkie" && h.horizon !== state.horizon) return false;
      if (state.happenPrice === "darmowe" && !h.free) return false;
      if (state.happenPrice === "platne" && h.free) return false;
      if (state.happenFilter !== "wszystkie" && h.category !== state.happenFilter) return false;
      return true;
    })
    .sort((a, b) => Number(Boolean(b.joined)) - Number(Boolean(a.joined)));
}

function visibleParents() {
  return state.parents.filter((p) => {
    if (state.trust[p.id]?.reported) return false;
    if (state.starredOnly && !state.trust[p.id]?.starred) return false;
    return true;
  });
}

function visibleSwaps() {
  return state.swaps.filter((s) => {
    if (state.swapFilter === "wszystkie") return true;
    return s.platform === state.swapFilter;
  });
}

function visiblePlaces() {
  return state.places.filter((p) => {
    if (state.placeFilter === "wszystkie") return true;
    if (state.placeFilter === "sprawdzone") return p.verified;
    return p.kind === state.placeFilter;
  });
}

function renderChrome() {
  document.body.dataset.tab = state.tab;
  fillRadiusControl();
  fillNeedFilters();
  chips(
    document.getElementById("age-filters"),
    [
      [false, "Każdy wiek"],
      [true, "Podobny wiek"],
    ],
    state.similarAge,
    async (id) => {
      state.similarAge = id;
      renderChrome();
      await loadVillage();
    },
    "mini"
  );
  fillStarFilters();
  chips(
    document.getElementById("horizon-filters"),
    [
      ["dzis", "Dziś"],
      ["tydzien", "W tym tygodniu"],
    ],
    state.horizon,
    (id) => {
      state.horizon = state.horizon === id ? "wszystkie" : id;
      renderChrome();
      renderLists();
    },
    "mini"
  );
  chips(
    document.getElementById("happen-filters"),
    [
      ["wszystkie", "Wszystkie"],
      ["ruch", "Ruch"],
      ["warsztat", "Warsztat"],
      ["inicjatywa", "Inicjatywa"],
    ],
    state.happenFilter,
    (id) => {
      state.happenFilter = id;
      renderChrome();
      renderLists();
    },
    "mini"
  );
  chips(
    document.getElementById("price-filters"),
    [
      ["darmowe", "Darmowe"],
      ["platne", "Płatne"],
    ],
    state.happenPrice,
    (id) => {
      state.happenPrice = state.happenPrice === id ? "wszystkie" : id;
      renderChrome();
      renderLists();
    },
    "mini"
  );
  chips(
    document.getElementById("swap-filters"),
    [
      ["wszystkie", "Wszystko"],
      ["osiedle", "Osiedle"],
      ["vinted", "Vinted"],
      ["olx", "OLX"],
      ["facebook", "FB"],
    ],
    state.swapFilter,
    (id) => {
      state.swapFilter = id;
      renderChrome();
      renderLists();
    },
    "mini"
  );
  chips(
    document.getElementById("place-filters"),
    [
      ["wszystkie", "Wszystko"],
      ["sprawdzone", "Sprawdzone"],
      ["miejsce", "Miejsca"],
      ["usluga", "Usługi"],
      ["opiekunka", "Opiekunki"],
    ],
    state.placeFilter,
    (id) => {
      state.placeFilter = id;
      renderChrome();
      renderLists();
    },
    "mini"
  );
  document.querySelectorAll(".tab").forEach((btn) => {
    btn.classList.toggle("on", btn.dataset.tab === state.tab);
  });
  document.getElementById("btn-profile")?.classList.toggle("on", state.tab === "profil");
  fillBadges();
}

function renderLists() {
  const happenings = visibleHappenings();
  const swaps = visibleSwaps();
  const places = visiblePlaces();
  const peopleRows = visibleParents();
  document.getElementById("count-parents").textContent = peopleRows.length;
  fillAreaCount();
  document.getElementById("count-happenings").textContent = happenings.length;
  document.getElementById("count-swaps").textContent = swaps.length;
  document.getElementById("count-places").textContent = places.length;
  document.getElementById("panel-dzieje").hidden = state.tab !== "dzieje";
  document.getElementById("panel-poznaj").hidden = state.tab !== "poznaj";
  document.getElementById("panel-wymiana").hidden = state.tab !== "wymiana";
  document.getElementById("panel-miejsca").hidden = state.tab !== "miejsca";
  document.getElementById("panel-inbox").hidden = state.tab !== "inbox";
  document.getElementById("panel-profil").hidden = state.tab !== "profil";
  document.getElementById("empty-parents").hidden = peopleRows.length > 0;
  document.getElementById("empty-parents-text").textContent = state.starredOnly
    ? "Nikogo jeszcze nie oznaczyłaś w wiosce. Dotknij tipi przy osobie."
    : radiusIndex() >= RADIUS_STEPS.length - 1 && !(state.needFilters || []).length
      ? "Nikogo w tym promieniu."
      : "Nikogo w tym promieniu. Zmień filtry albo powiększ obszar.";
  document.getElementById("empty-happenings").hidden = happenings.length > 0;
  document.getElementById("empty-swaps").hidden = swaps.length > 0;
  document.getElementById("empty-places").hidden = places.length > 0;

  const people = document.getElementById("list-parents");
  people.innerHTML = peopleRows
    .map((p) => {
      const overlap = (p.overlap_labels || []).slice(0, 2).join(" · ");
      const starred = Boolean(state.trust[p.id]?.starred);
      return `
      <li class="person-item">
        <button class="card" data-person="${esc(p.id)}" type="button">
          <div class="avatar-wrap">
            <div class="avatar" style="background:${colorFor(p.id)}">${esc(p.name[0])}</div>
            ${starred ? `<span class="village-badge">${TIPI_SVG}</span>` : ""}
          </div>
          <div>
            <strong>${esc(p.name)}</strong>
            <span>${esc(p.kid_label)}</span>
            <span class="meta">${esc(p.distance)} · ${esc(p.want_label)}</span>
            ${overlap ? `<span class="match">${p.match_score > 0 ? "Podobnie: " : ""}${esc(overlap)}</span>` : ""}
          </div>
        </button>
        <button class="village-mark${starred ? " on" : ""}" type="button" data-star="${esc(p.id)}" aria-pressed="${starred}" aria-label="${starred ? "Usuń z wioski" : "Dodaj do wioski"}">${TIPI_SVG}</button>
      </li>`;
    })
    .join("");
  people.querySelectorAll("[data-person]").forEach((btn) => {
    btn.addEventListener("click", () => openPerson(btn.dataset.person));
  });
  people.querySelectorAll("[data-star]").forEach((btn) => {
    btn.addEventListener("click", (ev) => {
      ev.stopPropagation();
      const id = btn.dataset.star;
      const starred = Boolean(state.trust[id]?.starred);
      toggleTrust(id, { starred: !starred }, { reopen: false });
    });
  });

  const happenList = document.getElementById("list-happenings");
  happenList.innerHTML = happenings
    .map(
      (e) => `
      <li>
        <button class="card event-card ${e.sponsored ? "sponsor" : ""} ${e.joined ? "joined" : ""}" data-happen="${esc(e.id)}" type="button">
          <span class="event-photo">
            <img src="${esc(photoFor(e))}" alt="" />
            <em>${esc(e.joined ? "Dołączasz" : e.sponsored ? "Zaprasza kawiarnia" : e.category_label)}</em>
          </span>
          <span class="event-body">
            <strong>${esc(e.title)}</strong>
            <span>${esc(e.source)} · ${esc(e.when)}</span>
            <span class="meta">${esc(e.distance)} · ${esc(e.price_label)} · ${esc(e.audience_label)}${e.joined ? " · Dołączasz" : ""}</span>
          </span>
        </button>
      </li>`
    )
    .join("");
  happenList.querySelectorAll("[data-happen]").forEach((btn) => {
    btn.addEventListener("click", () => openHappening(btn.dataset.happen));
  });

  const swapList = document.getElementById("list-swaps");
  swapList.innerHTML = swaps
    .map(
      (s) => `
      <li>
        <button class="card media-card" data-swap="${esc(s.id)}" type="button">
          <img class="thumb" src="${esc(photoFor(s, "swap"))}" alt="" />
          <div>
            <strong>${esc(s.title)}</strong>
            <span>${esc(s.who || "Wioska")} · ${esc(s.kind_label)}</span>
            <span class="meta">${esc(s.distance)}</span>
          </div>
          <span class="go" aria-hidden="true">→</span>
        </button>
      </li>`
    )
    .join("");
  swapList.querySelectorAll("[data-swap]").forEach((btn) => {
    btn.addEventListener("click", () => openSwap(btn.dataset.swap));
  });

  const placeList = document.getElementById("list-places");
  placeList.innerHTML = places
    .map(
      (p) => `
      <li>
        <button class="card media-card" data-place="${esc(p.id)}" type="button">
          <img class="thumb" src="${esc(photoFor(p, p.kind === "opiekunka" ? "people" : "dk"))}" alt="" />
          <div>
            <strong>${esc(p.name)}</strong>
            <span>${esc(p.tag)} · ${esc(p.by)}</span>
            <span class="meta">${esc(p.distance)}${p.verified ? " · sprawdzone" : ""}</span>
          </div>
          <span class="go" aria-hidden="true">→</span>
        </button>
      </li>`
    )
    .join("");
  placeList.querySelectorAll("[data-place]").forEach((btn) => {
    btn.addEventListener("click", () => openPlace(btn.dataset.place));
  });

  const inboxList = document.getElementById("list-inbox");
  const threads = state.threads || [];
  document.getElementById("empty-inbox").hidden = threads.length > 0;
  inboxList.innerHTML = threads
    .map(
      (t) => `
      <li>
        <button class="card ${t.unread ? "fresh" : ""}" data-thread="${esc(t.id)}" type="button">
          <div class="avatar" style="background:${colorFor(t.id)}">${esc((t.name || "?")[0])}</div>
          <div>
            <strong>${esc(t.name)}</strong>
            <span>${esc(t.last)}</span>
            <span class="meta">${esc(t.at)}${t.unread ? " · nowa" : ""}</span>
          </div>
          <span class="go" aria-hidden="true">→</span>
        </button>
      </li>`
    )
    .join("");
  inboxList.querySelectorAll("[data-thread]").forEach((btn) => {
    btn.addEventListener("click", () => openChat(personFromId(btn.dataset.thread), true));
  });
}

function hideSheet() {
  document.getElementById("sheet").hidden = true;
  document.getElementById("sheet").innerHTML = "";
  document.getElementById("scrim").hidden = true;
}

function showSheet(html) {
  const sheet = document.getElementById("sheet");
  document.getElementById("scrim").hidden = false;
  sheet.hidden = false;
  sheet.innerHTML = html;
  sheet.querySelector(".close")?.addEventListener("click", hideSheet);
}

function personFromId(id) {
  return state.parents.find((x) => x.id === id) || state.threads.find((x) => x.id === id) || { id, name: id };
}

function fillBadges() {
  const n = state.unreadNotices || 0;
  const m = state.unreadMessages || 0;
  const nb = document.getElementById("badge-notices");
  const mb = document.getElementById("badge-inbox");
  if (nb) {
    nb.hidden = n < 1;
    nb.textContent = String(n);
  }
  if (mb) {
    mb.hidden = m < 1;
    mb.textContent = String(m);
  }
}

async function loadInbox() {
  const data = await fetch("/api/inbox").then((r) => r.json());
  state.notices = data.notices || [];
  state.threads = data.threads || [];
  state.unreadNotices = data.unread_notices || 0;
  state.unreadMessages = data.unread_messages || 0;
  fillBadges();
}

function openNotices() {
  const rows = (state.notices || [])
    .map(
      (n) => `
      <li>
        <button class="card notice ${n.read ? "" : "fresh"}" data-notice="${esc(n.id)}" type="button">
          <div>
            <strong>${esc(n.title)}</strong>
            <span>${esc(n.body)}</span>
            <span class="meta">${esc(n.at)}${n.read ? "" : " · nowe"}</span>
          </div>
          <span class="go" aria-hidden="true">→</span>
        </button>
      </li>`
    )
    .join("");
  showSheet(`
    <button class="close" type="button">Zamknij</button>
    <h2>Powiadomienia</h2>
    <ul class="cards inbox-list">${rows || "<li class='empty'>Cicho. Nic nowego.</li>"}</ul>
  `);
  document.querySelectorAll("[data-notice]").forEach((btn) => {
    btn.addEventListener("click", () => openNotice(btn.dataset.notice));
  });
}

function openInbox() {
  state.tab = "inbox";
  state.inboxOpen = true;
  hideSheet();
  renderChrome();
  renderLists();
}

async function openNotice(id) {
  const item = (state.notices || []).find((n) => n.id === id);
  if (!item) return;
  await fetch("/api/notices/read", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ notice_id: id }),
  }).then((r) => r.json()).then((data) => {
    state.notices = data.notices || state.notices;
    state.unreadNotices = data.unread_notices || 0;
    fillBadges();
  });
  if (item.parent_id) {
    await openChat(personFromId(item.parent_id), true);
    return;
  }
  if (item.happening_id) {
    hideSheet();
    const found = state.happenings.find((h) => h.id === item.happening_id);
    if (found) {
      openHappening(found.id);
      return;
    }
    state.tab = "dzieje";
    renderChrome();
    renderLists();
  }
}

function openPerson(id) {
  const p = state.parents.find((x) => x.id === id);
  if (!p) return;
  const trust = state.trust[p.id] || {};
  state.tab = "poznaj";
  renderChrome();
  renderLists();
  showSheet(`
    <button class="close" type="button">Zamknij</button>
    <div class="avatar" style="background:${colorFor(p.id)};width:56px;height:56px;margin-bottom:10px">${esc(p.name[0])}</div>
    <h2>${esc(p.name)}</h2>
    <p class="kid">${esc(p.kid_label)}</p>
    <p>${esc(p.bio)}</p>
    <p class="meta">${esc(p.distance)} · ${esc(p.want_label)}</p>
    ${(p.overlap_labels || []).length ? `<p class="match">Szuka podobnie: ${esc((p.overlap_labels || []).join(", "))}</p>` : ""}
    ${p.window ? `<p class="hint">Okno: ${esc(p.window)}</p>` : ""}
    <div class="sheet-actions">
      <button class="village-sheet${trust.starred ? " on" : ""}" id="star-village" type="button">${TIPI_SVG} ${trust.starred ? "W Twojej wiosce" : "Dodaj do wioski"}</button>
      <button class="primary" id="write" type="button">Napisz wiadomość</button>
      <button class="ghost mini" id="report" type="button">${trust.reported ? "Cofnij zgłoszenie" : "Zgłoś profil"}</button>
    </div>
  `);
  document.getElementById("star-village").addEventListener("click", () => toggleTrust(p.id, { starred: !trust.starred }));
  document.getElementById("write").addEventListener("click", () => openChat(p, false));
  document.getElementById("report").addEventListener("click", () => toggleTrust(p.id, { reported: !trust.reported }));
}

function fillStarFilters() {
  const host = document.getElementById("star-filters");
  if (!host) return;
  host.innerHTML = "";
  const btn = document.createElement("button");
  btn.type = "button";
  btn.className = state.starredOnly ? "mini on village-chip" : "mini village-chip";
  btn.innerHTML = `${TIPI_SVG} Oznaczone`;
  btn.addEventListener("click", () => {
    state.starredOnly = !state.starredOnly;
    renderChrome();
    renderLists();
  });
  host.appendChild(btn);
}

async function toggleTrust(parentId, patch, opts = {}) {
  const reopen = opts.reopen !== false;
  const saved = await fetch("/api/trust", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ parent_id: parentId, ...patch }),
  }).then((r) => r.json());
  state.trust[parentId] = saved;
  const sheetOpen = !document.getElementById("sheet")?.hidden;
  if (saved.reported) hideSheet();
  else if (reopen || sheetOpen) openPerson(parentId);
  renderLists();
}

async function openHappening(id) {
  const e = state.happenings.find((x) => x.id === id);
  if (!e) return;
  state.tab = "dzieje";
  renderChrome();
  renderLists();
  showSheet(`
    <button class="close" type="button">Zamknij</button>
    <img class="cover" src="${esc(photoFor(e))}" alt="" />
    <p class="eyebrow">${esc(e.sponsored ? "Zaproszenie kawiarni" : e.category_label)} · ${esc(e.price_label)} · ${esc(e.audience_label)}</p>
    <h2>${esc(e.title)}</h2>
    <p>${esc(e.source)} · ${esc(e.when)}</p>
    <p>${esc(e.place)}</p>
    <p>${esc(e.blurb)}</p>
    ${e.perk ? `<p class="match">${esc(e.perk)}</p>` : ""}
    <p class="meta">${esc(e.distance)}</p>
    <button class="primary" id="join" type="button">${e.joined ? "Jesteś zapisana" : "Dołącz"}</button>
  `);
  document.getElementById("join").addEventListener("click", async () => {
    await fetch("/api/join", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ event_id: e.id, joined: !e.joined }),
    });
    await loadVillage();
    openHappening(e.id);
  });
}

function openSwap(id) {
  const s = state.swaps.find((x) => x.id === id);
  if (!s) return;
  state.tab = "wymiana";
  renderChrome();
  renderLists();
  const link = s.url
    ? `<a class="out primary" href="${esc(s.url)}" target="_blank" rel="noopener noreferrer">Otwórz na ${esc(s.platform_label)}</a>`
    : `<p class="hint">Bez linku — umów odbiór w wiosce.</p>`;
  showSheet(`
    <button class="close" type="button">Zamknij</button>
    <img class="cover" src="${esc(photoFor(s, "swap"))}" alt="" />
    <p class="eyebrow">${esc(s.platform_label)} · ${esc(s.kind_label)}</p>
    <h2>${esc(s.title)}</h2>
    <p class="kid">${esc(s.who || "Wioska")} · ${esc(s.distance)}</p>
    <p>${esc(s.note)}</p>
    ${link}
  `);
}

function openPlace(id) {
  const p = state.places.find((x) => x.id === id);
  if (!p) return;
  state.tab = "miejsca";
  renderChrome();
  renderLists();
  showSheet(`
    <button class="close" type="button">Zamknij</button>
    <img class="cover" src="${esc(photoFor(p, p.kind === "opiekunka" ? "people" : "dk"))}" alt="" />
    <p class="eyebrow">${esc(p.kind_label)}${p.verified ? " · sprawdzone" : ""}</p>
    <h2>${esc(p.name)}</h2>
    <p class="kid">${esc(p.tag)} · ${esc(p.distance)}</p>
    <p>${esc(p.note)}</p>
    <p class="hint">Poleca: ${esc(p.by)}</p>
  `);
}

async function openChat(person, fromInbox = false) {
  state.inboxOpen = fromInbox;
  const data = await fetch(`/api/messages/${person.id}`).then((r) => r.json());
  const log =
    data.messages.length === 0
      ? `<p class="empty">Napisz pierwsze „cześć, wychodzę za 10 min?”</p>`
      : data.messages
          .map((m) => {
            const mine = m.sender === "ty";
            return `<p class="bubble ${mine ? "me" : "them"}"><span>${esc(m.at)} · ${mine ? "Ty" : esc(person.name)}</span>${esc(m.text)}</p>`;
          })
          .join("");
  showSheet(`
    <button class="close" type="button">${fromInbox ? "Wiadomości" : "Zamknij"}</button>
    <div class="avatar" style="background:${colorFor(person.id)};width:48px;height:48px;margin-bottom:8px">${esc(person.name[0])}</div>
    <h2>${esc(person.name)}</h2>
    <p class="kid">Wiadomość zostaje między wami. Imion dzieci tu nie wpisujemy.</p>
    <div class="log">${log}</div>
    <div class="composer">
      <input id="draft" placeholder="Krótka wiadomość…" />
      <button class="primary" id="send" type="button">Wyślij</button>
    </div>
  `);
  const close = document.querySelector("#sheet .close");
  if (fromInbox && close) {
    const fresh = close.cloneNode(true);
    close.replaceWith(fresh);
    fresh.addEventListener("click", async () => {
      await loadInbox();
      openInbox();
    });
  }
  const send = async () => {
    const text = document.getElementById("draft").value.trim();
    if (!text) return;
    await fetch("/api/messages", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ parent_id: person.id, text }),
    });
    await openChat(person, fromInbox);
    await loadInbox();
  };
  document.getElementById("send").addEventListener("click", send);
  document.getElementById("draft").addEventListener("keydown", (ev) => {
    if (ev.key === "Enter") send();
  });
  await loadInbox();
}

async function loadVillage() {
  const data = await fetch("/api/village", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      seeking: state.needFilters || [],
      similar_age: state.similarAge,
      radius_km: state.radiusM ? state.radiusM / 1000 : null,
    }),
  }).then((r) => r.json());
  state.parents = data.parents;
  state.happenings = data.happenings;
  state.swaps = data.swaps;
  state.places = data.places;
  if (data.areas?.length) state.areas = data.areas;
  if (data.origin) state.origin = data.origin;
  if (data.zoom) state.zoom = data.zoom;
  renderLists();
}

async function loadTrust() {
  state.trust = await fetch("/api/trust").then((r) => r.json());
}

function checks(host, options, selected, onChange) {
  if (!host || !options) return;
  host.innerHTML = Object.entries(options)
    .map(
      ([id, label]) => `
      <label class="${selected.includes(id) ? "on" : ""}">
        <input type="checkbox" value="${esc(id)}" ${selected.includes(id) ? "checked" : ""} />
        ${esc(label)}
      </label>`
    )
    .join("");
  host.querySelectorAll("input").forEach((el) => {
    el.addEventListener("change", () => {
      el.closest("label").classList.toggle("on", el.checked);
      onChange?.();
    });
  });
}

function estimateChipWidth(label, id, measured) {
  if (measured?.[id]) return measured[id];
  const canvas = document.createElement("canvas").getContext("2d");
  if (!canvas) return 40 + [...String(label)].length * 7;
  const root = Number.parseFloat(getComputedStyle(document.documentElement).fontSize) || 16;
  canvas.font = `600 ${0.84 * root}px "Source Sans 3", "Segoe UI", sans-serif`;
  return 22 + canvas.measureText(String(label)).width;
}

function packFilterOptions(options, rowWidth, measured) {
  const items = Object.entries(options).map(([id, label]) => ({
    id,
    label,
    width: estimateChipWidth(label, id, measured),
  }));
  items.sort((a, b) => b.width - a.width);
  const gap = 5;
  const longest = items[0];
  const companion = items.find((item) => item.id === "jedzenie" && item !== longest);
  const usedIds = new Set([longest.id, companion?.id].filter(Boolean));
  const rest = items.filter((item) => !usedIds.has(item.id));
  const rows = [
    {
      items: companion ? [longest, companion] : [longest],
      used: longest.width + (companion ? gap + companion.width : 0),
    },
  ];
  const seedMin = companion ? companion.width * 0.82 : longest.width * 0.7;
  const seeds = rest.filter((item) => item.width >= seedMin);
  const fillers = rest.filter((item) => item.width < seedMin).sort((a, b) => a.width - b.width);
  for (const seed of seeds) rows.push({ items: [seed], used: seed.width });
  const place = (item, from) => {
    for (let r = from; r < rows.length; r += 1) {
      if (rows[r].used + gap + item.width <= rowWidth) {
        rows[r].items.push(item);
        rows[r].used += gap + item.width;
        return true;
      }
    }
    return false;
  };
  const leftover = [];
  for (const item of fillers) {
    if (item.id === "narzekac" && rows.length > 2 && place(item, rows.length - 2)) continue;
    leftover.push(item);
  }
  leftover.sort((a, b) => a.width - b.width);
  for (const item of leftover) {
    if (!place(item, 1)) rows.push({ items: [item], used: item.width });
  }
  return Object.fromEntries(rows.flatMap((row) => row.items).map((item) => [item.id, item.label]));
}

function fillNeedFilters() {
  const host = document.getElementById("need-filters");
  const options = state.profile?.seeking_options;
  if (!host || !options) return;
  const rowWidth = Math.max(240, host.clientWidth || (document.querySelector(".feed")?.clientWidth || 360) - 4);
  const paint = (packed) => {
    checks(host, packed, state.needFilters || [], async () => {
      state.needFilters = [...host.querySelectorAll("input:checked")].map((el) => el.value);
      await loadVillage();
    });
  };
  paint(packFilterOptions(options, rowWidth, fillNeedFilters.measured));
  const measured = {};
  host.querySelectorAll("label").forEach((label) => {
    const id = label.querySelector("input")?.value;
    if (id) measured[id] = label.getBoundingClientRect().width;
  });
  fillNeedFilters.measured = measured;
  const realWidth = host.clientWidth || rowWidth;
  paint(packFilterOptions(options, realWidth, measured));
}

function optionsHtml(options, selected) {
  return Object.entries(options)
    .map(([id, label]) => `<option value="${esc(id)}" ${id === selected ? "selected" : ""}>${esc(label)}</option>`)
    .join("");
}

function renderKids() {
  ["kids-list", "gate-kids"].forEach((hostId) => {
    const host = document.getElementById(hostId);
    const p = state.profile;
    if (!host || !p) return;
    const kids = p.kids && p.kids.length ? p.kids : [{ gender: "dziewczynka", age_band: "6-12m" }];
    p.kids = kids;
    const options = p.gender_options && p.age_band_options
      ? p
      : {
          gender_options: { dziewczynka: "Dziewczynka", chlopiec: "Chłopiec", bliznieta: "Bliźnięta", dziecko: "Dziecko" },
          age_band_options: {
            "0-6m": "0–6 mies.",
            "6-12m": "6–12 mies.",
            "1-2": "1–2 lata",
            "2-3": "2–3 lata",
            "3-5": "3–5 lat",
            "6-8": "6–8 lat",
            "9-12": "9–12 lat",
            "13-17": "13–17 lat",
          },
        };
    host.innerHTML = kids
      .map(
        (kid, idx) => `
        <div class="kid-row" data-idx="${idx}">
          <select name="gender">${optionsHtml(options.gender_options, kid.gender)}</select>
          <select name="age_band">${optionsHtml(options.age_band_options, kid.age_band)}</select>
          <button type="button" class="mini" data-remove="${idx}" ${kids.length < 2 ? "disabled" : ""}>Usuń</button>
        </div>`
      )
      .join("");
    host.querySelectorAll(".kid-row").forEach((row) => {
      const idx = Number(row.dataset.idx);
      row.querySelectorAll("select").forEach((sel) => {
        sel.addEventListener("change", () => {
          p.kids[idx][sel.name] = sel.value;
        });
      });
    });
    host.querySelectorAll("[data-remove]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const idx = Number(btn.dataset.remove);
        p.kids.splice(idx, 1);
        renderKids();
      });
    });
  });
}

function collectProfile(extra = {}) {
  const form = document.getElementById("profile-form");
  const seekingHosts = extra.seekingHost
    ? extra.seekingHost
    : [...document.querySelectorAll("#seeking-checks input:checked")].map((el) => el.value);
  return {
    name: extra.name ?? form.name.value.trim(),
    district: placePhrase(state.districtId, state.areaId),
    district_id: extra.district_id ?? state.districtId,
    area_id: extra.area_id ?? state.areaId,
    about: extra.about ?? form.about.value.trim(),
    kids: (state.profile.kids || []).map((kid) => ({
      gender: kid.gender,
      age_band: kid.age_band,
    })),
    interests: extra.interests ?? [],
    seeking: extra.seeking ?? seekingHosts,
    availability: state.myWant,
    window: extra.window ?? state.profile?.window ?? "",
    quiet: false,
    onboarded: extra.onboarded ?? true,
    email: extra.email ?? state.email ?? state.profile?.email ?? "",
    verified: extra.verified ?? Boolean(state.profile?.verified || state.email),
  };
}

function fillHello() {
  const name = state.profile?.name;
  document.getElementById("hello").textContent = name ? `Cześć, ${name}` : "Cześć";
}

function renderGate() {
  const total = 6;
  document.getElementById("gate-count").textContent = `${state.gateStep + 1} / ${total}`;
  document.getElementById("gate-dots").innerHTML = Array.from({ length: total }, (_, i) =>
    `<i class="${i <= state.gateStep ? "on" : ""}"></i>`
  ).join("");
  document.querySelectorAll(".gate-step").forEach((el) => {
    el.hidden = Number(el.dataset.step) !== state.gateStep;
  });
  document.getElementById("gate-back").disabled = state.gateStep === 0;
  document.getElementById("gate-next").textContent = state.gateStep === total - 1 ? "Wejdź do wioski" : "Dalej";
  const mail = document.getElementById("gate-email")?.value.trim() || state.email;
  const mailLabel = document.getElementById("gate-code-mail");
  if (mailLabel) mailLabel.textContent = mail || "Twój e-mail";
  if (state.gateStep === 4) renderKids();
  if (state.gateStep === 5) {
    const seeking = state.profile?.seeking || [];
    checks(document.getElementById("gate-seeking"), state.profile?.seeking_options, seeking);
  }
}

function showGate(blank = false) {
  const p = state.profile || {};
  document.getElementById("gate-name").value = blank ? "" : p.name || "";
  document.getElementById("gate-about").value = blank ? "" : p.about || "";
  const emailEl = document.getElementById("gate-email");
  const codeEl = document.getElementById("gate-code");
  if (emailEl) emailEl.value = blank ? "" : p.email || state.email || "";
  if (codeEl) codeEl.value = "";
  const resent = document.getElementById("gate-resent");
  if (resent) resent.hidden = true;
  if (blank) {
    p.kids = [{ gender: "dziewczynka", age_band: "6-12m" }];
    p.seeking = ["spacerek"];
    state.myWant = "spacer";
  }
  state.gateStep = 0;
  document.getElementById("gate").hidden = false;
  document.body.classList.add("gate-on");
  renderGate();
}

function hideGate() {
  document.getElementById("gate").hidden = true;
  document.body.classList.remove("gate-on");
}

async function finishGate() {
  const name = document.getElementById("gate-name").value.trim();
  if (!name) {
    state.gateStep = 3;
    renderGate();
    document.getElementById("gate-name").focus();
    return;
  }
  const email = document.getElementById("gate-email").value.trim() || state.email;
  const seeking = [...document.querySelectorAll("#gate-seeking input:checked")].map((el) => el.value);
  const payload = collectProfile({
    name,
    about: document.getElementById("gate-about").value.trim(),
    seeking: seeking.length ? seeking : ["spacerek"],
    interests: [],
    quiet: false,
    onboarded: true,
    email,
    verified: true,
  });
  state.profile = {
    ...state.profile,
    ...(await fetch("/api/me", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    }).then((r) => r.json())),
  };
  hideGate();
  state.tab = "poznaj";
  fillProfileForm();
  fillHello();
  renderChrome();
  await loadInbox();
  await loadVillage();
}

function fillProfileForm() {
  const p = state.profile;
  if (!p) return;
  const form = document.getElementById("profile-form");
  form.name.value = p.name || "";
  form.about.value = p.about || "";
  checks(document.getElementById("seeking-checks"), p.seeking_options, p.seeking || []);
  state.myWant = p.availability || p.today || "spacer";
  renderKids();
  state.email = p.email || state.email || "";
  const verified = document.getElementById("profile-verified");
  if (verified) {
    if (p.email && p.verified !== false) {
      verified.hidden = false;
      verified.textContent = `Zweryfikowany e-mail: ${p.email}`;
    } else {
      verified.hidden = true;
    }
  }
}

async function loadProfile() {
  state.profile = await fetch("/api/me").then((r) => r.json());
  fillProfileForm();
  fillHello();
}

document.getElementById("add-kid").addEventListener("click", () => {
  if (!state.profile) return;
  state.profile.kids = state.profile.kids || [];
  state.profile.kids.push({ gender: "dziewczynka", age_band: "6-12m" });
  renderKids();
});
document.getElementById("gate-add-kid").addEventListener("click", () => {
  if (!state.profile) return;
  state.profile.kids = state.profile.kids || [];
  state.profile.kids.push({ gender: "dziewczynka", age_band: "6-12m" });
  renderKids();
});
document.getElementById("gate-back").addEventListener("click", () => {
  if (state.gateStep > 0) {
    state.gateStep -= 1;
    renderGate();
  }
});
document.getElementById("gate-next").addEventListener("click", async () => {
  if (state.gateStep === 1) {
    const email = document.getElementById("gate-email").value.trim();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      document.getElementById("gate-email").focus();
      return;
    }
    state.email = email;
  }
  if (state.gateStep === 2) {
    const code = document.getElementById("gate-code").value.replace(/\D/g, "");
    if (code.length < 4) {
      document.getElementById("gate-code").focus();
      return;
    }
  }
  if (state.gateStep === 3 && !document.getElementById("gate-name").value.trim()) {
    document.getElementById("gate-name").focus();
    return;
  }
  if (state.gateStep < 5) {
    state.gateStep += 1;
    renderGate();
    return;
  }
  await finishGate();
});
document.getElementById("replay-demo").addEventListener("click", () => {
  showGate(false);
});

document.getElementById("profile-form").addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const payload = collectProfile({ onboarded: true });
  state.profile = {
    ...state.profile,
    ...(await fetch("/api/me", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    }).then((r) => r.json())),
  };
  fillHello();
  await loadVillage();
  const saved = document.getElementById("profile-saved");
  saved.hidden = false;
  setTimeout(() => {
    saved.hidden = true;
  }, 2000);
});

document.getElementById("scrim").addEventListener("click", hideSheet);
document.getElementById("btn-notices").addEventListener("click", () => {
  loadInbox().then(openNotices);
});
document.getElementById("btn-profile").addEventListener("click", () => {
  state.tab = "profil";
  hideSheet();
  renderChrome();
  renderLists();
});
document.getElementById("gate-resend").addEventListener("click", () => {
  document.getElementById("gate-resent").hidden = false;
});

document.getElementById("radius-minus").addEventListener("click", () => {
  setRadiusByIndex(radiusIndex() - 1);
});
document.getElementById("radius-plus").addEventListener("click", () => {
  setRadiusByIndex(radiusIndex() + 1);
});
document.getElementById("radius-range").addEventListener("input", (ev) => {
  setRadiusByIndex(Number(ev.target.value));
});

document.querySelectorAll(".tab").forEach((btn) => {
  btn.addEventListener("click", () => {
    state.tab = btn.dataset.tab;
    hideSheet();
    renderChrome();
    renderLists();
    if (state.tab === "inbox") loadInbox().then(() => renderLists());
  });
});

document.getElementById("create-event").addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const form = new FormData(ev.target);
  await fetch("/api/events", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      title: form.get("title"),
      when: form.get("when"),
      place: form.get("place"),
      kind: "inicjatywa",
      lat: state.origin.lat,
      lng: state.origin.lng,
    }),
  });
  ev.target.reset();
  state.tab = "dzieje";
  renderChrome();
  await loadVillage();
});

document.getElementById("create-swap").addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const form = new FormData(ev.target);
  await fetch("/api/swaps", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      title: form.get("title"),
      platform: form.get("platform"),
      url: form.get("url"),
      note: form.get("note"),
      lat: state.origin.lat,
      lng: state.origin.lng,
    }),
  });
  ev.target.reset();
  state.tab = "wymiana";
  renderChrome();
  await loadVillage();
});

renderChrome();
Promise.all([loadProfile(), loadTrust(), loadInbox()]).then(() => {
  fillProfileForm();
  renderChrome();
  renderLists();
  const params = new URLSearchParams(location.search);
  if (shouldShowGate()) showGate(params.has("demo") || params.has("start") || !state.profile?.onboarded);
  loadVillage();
});
