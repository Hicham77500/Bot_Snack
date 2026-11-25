import { seed } from "./seed.js";

const CLE = "solive.v1";
let state = normaliser(lire());
const ecouteurs = new Set();

function lire() {
  try {
    if (typeof localStorage === "undefined") return null;
    const brut = localStorage.getItem(CLE);
    return brut ? JSON.parse(brut) : null;
  } catch {
    return null;
  }
}

function normaliser(data) {
  if (!data || !Array.isArray(data.chantiers) || !Array.isArray(data.devis)) {
    return structuredClone(seed);
  }
  data.entreprise ??= structuredClone(seed.entreprise);
  data.compagnons ??= structuredClone(seed.compagnons);
  data.bibliotheque ??= structuredClone(seed.bibliotheque);
  data.situations ??= [];
  data.achats ??= [];
  data.pointages ??= [];
  data.historique ??= {};
  data.semaine ??= seed.semaine;
  return data;
}

function persister() {
  try {
    localStorage.setItem(CLE, JSON.stringify(state));
  } catch {
    /* La démo hors navigateur reste en mémoire. */
  }
}

function publier() {
  for (const ecouteur of ecouteurs) ecouteur(state);
}

export function getState() {
  return state;
}

export function subscribe(ecouteur) {
  ecouteurs.add(ecouteur);
  return () => ecouteurs.delete(ecouteur);
}

export function commit(modifier, { notify = true } = {}) {
  const brouillon = structuredClone(state);
  modifier(brouillon);
  state = brouillon;
  persister();
  if (notify) publier();
}

export function reinitialiser() {
  state = structuredClone(seed);
  persister();
  publier();
}
