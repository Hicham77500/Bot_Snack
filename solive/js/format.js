const euroEntier = new Intl.NumberFormat("fr-FR", {
  style: "currency",
  currency: "EUR",
  maximumFractionDigits: 0,
});

const euroCentimes = new Intl.NumberFormat("fr-FR", {
  style: "currency",
  currency: "EUR",
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
});

const pourcentage = new Intl.NumberFormat("fr-FR", {
  style: "percent",
  minimumFractionDigits: 1,
  maximumFractionDigits: 1,
});

const nombre = new Intl.NumberFormat("fr-FR", {
  maximumFractionDigits: 1,
});

export function eur(valeur) {
  return euroEntier.format(Number.isFinite(valeur) ? valeur : 0);
}

export function eur2(valeur) {
  return euroCentimes.format(Number.isFinite(valeur) ? valeur : 0);
}

export function pct(ratio) {
  return pourcentage.format(Number.isFinite(ratio) ? ratio : 0);
}

export function num(valeur) {
  return nombre.format(Number.isFinite(valeur) ? valeur : 0);
}

export function esc(valeur) {
  return String(valeur ?? "").replace(/[&<>"']/g, (caractere) => {
    switch (caractere) {
      case "&":
        return "&amp;";
      case "<":
        return "&lt;";
      case ">":
        return "&gt;";
      case '"':
        return "&quot;";
      default:
        return "&#39;";
    }
  });
}

export function uid(prefixe) {
  return `${prefixe}-${Math.random().toString(36).slice(2, 8)}`;
}
