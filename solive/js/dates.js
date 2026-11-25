export const AUJOURDHUI = "2026-11-25";

export function ajouterJours(iso, jours) {
  const date = new Date(`${iso}T12:00:00Z`);
  date.setUTCDate(date.getUTCDate() + jours);
  return date.toISOString().slice(0, 10);
}

export function lundiDe(iso) {
  const date = new Date(`${iso}T12:00:00Z`);
  const jour = date.getUTCDay();
  const decalage = jour === 0 ? -6 : 1 - jour;
  return ajouterJours(iso, decalage);
}

export function joursOuvres(lundi) {
  return [0, 1, 2, 3, 4].map((offset) => ajouterJours(lundi, offset));
}

const JOURS = ["dim.", "lun.", "mar.", "mer.", "jeu.", "ven.", "sam."];

export function libelleJour(iso) {
  const date = new Date(`${iso}T12:00:00Z`);
  const jour = JOURS[date.getUTCDay()];
  return `${jour} ${date.getUTCDate()}`;
}

export function libelleDate(iso) {
  const date = new Date(`${iso}T12:00:00Z`);
  return new Intl.DateTimeFormat("fr-FR", {
    day: "numeric",
    month: "long",
    year: "numeric",
    timeZone: "UTC",
  }).format(date);
}
