import {
  avancementPrecedent,
  detailSituation,
  devisPrincipal,
  devisTotaux,
  ligneMontants,
  peutCreerDgd,
  resumeChantier,
  resumeEntreprise,
  situationsChantier,
} from "./calc.js";
import { AUJOURDHUI, joursOuvres, libelleDate, libelleJour } from "./dates.js";
import { esc, eur, eur2, num, pct } from "./format.js";

const NAV = [
  ["dashboard", "Tableau de bord", "#/app"],
  ["chantiers", "Chantiers", "#/app/chantiers"],
  ["devis", "Devis", "#/app/devis"],
  ["situations", "Situations", "#/app/situations"],
  ["achats", "Achats", "#/app/achats"],
  ["planning", "Planning", "#/app/planning"],
];

const NATURES = [
  ["mo", "Main-d'œuvre"],
  ["materiaux", "Fournitures"],
  ["sous_traitance", "Sous-traitance"],
];

export function render(state, route) {
  if (route.page === "landing") return pageAccueil(state);
  const actif = route.page === "dashboard" ? "dashboard" : route.page;
  return coquille(state, actif, contenu(state, route));
}

export function peindre(state) {
  const zone = document.querySelector("[data-paint]");
  if (!zone) return;
  if (zone.dataset.paint === "devis") peindreDevis(state, zone.dataset.id);
  if (zone.dataset.paint === "situation") peindreSituation(state, zone.dataset.id);
}

function contenu(state, route) {
  if (route.page === "dashboard") return pageTableau(state);
  if (route.page === "chantiers" && route.id) return pageChantier(state, route.id);
  if (route.page === "chantiers") return pageChantiers(state);
  if (route.page === "devis" && route.id) return pageDevis(state, route.id);
  if (route.page === "devis") return pageDevisListe(state);
  if (route.page === "situations" && route.id) return pageSituation(state, route.id);
  if (route.page === "situations") return pageSituations(state);
  if (route.page === "achats") return pageAchats(state);
  if (route.page === "planning") return pagePlanning(state);
  return pageTableau(state);
}

function coquille(state, actif, corps) {
  const liens = NAV.map(([id, label, href]) => {
    const courant = id === actif ? ' aria-current="page"' : "";
    return `<a class="rail-link" href="${href}"${courant}>${label}</a>`;
  }).join("");
  return `<div class="app-shell">
    <aside class="rail">
      <a class="brand" href="#/">Solive</a>
      <p class="rail-meta">${esc(state.entreprise.nom)}</p>
      <nav class="rail-nav">${liens}</nav>
      <button class="rail-reset" type="button" data-action="reinitialiser">Revenir à la démo</button>
    </aside>
    <div class="workspace">
      <header class="topbar">
        <p>${esc(state.entreprise.metier)} · ${esc(state.entreprise.ville)}</p>
        <p>${libelleDate(AUJOURDHUI)}</p>
      </header>
      <main class="canvas">${corps}</main>
    </div>
  </div>`;
}

function pageAccueil(state) {
  const entreprise = resumeEntreprise(state);
  const alertes = entreprise.rows.flatMap((ligne) => phrases(ligne));
  return `<div class="landing">
    <header class="landing-bar">
      <a class="brand brand-dark" href="#/">Solive</a>
      <a class="button" href="#/app">Ouvrir l'atelier</a>
    </header>
    <section class="hero">
      <div>
        <p class="kicker">Logiciel de chantier</p>
        <h1>La marge réelle, pendant que le chantier avance.</h1>
        <p class="lede">Solive rapproche le devis signé, les factures d'achat, les heures des compagnons et les situations. Le reste à dépenser et le reste à facturer se recalculent chantier par chantier.</p>
        <div class="hero-actions">
          <a class="button" href="#/app">Voir le tableau de bord</a>
          <a class="button button-ghost" href="#/app/devis">Chiffrer un devis</a>
        </div>
      </div>
      <article class="preview">
        <header>
          <strong>${esc(state.entreprise.nom)}</strong>
          <span>Chantiers en cours</span>
        </header>
        <div class="metric-row">
          ${metrique("Facturé HT", eur(entreprise.facture))}
          ${metrique("Reste à dépenser", eur(entreprise.resteDepenser))}
          ${metrique("Écart facturé / dépensé", eur(entreprise.ecart))}
        </div>
        <ul class="preview-list">
          ${entreprise.actifs.map((ligne) => `<li>
            <span>${esc(ligne.chantier.nom)}</span>
            <strong class="${ligne.attentionMarge ? "is-alert" : ""}">${ligne.margeReelle == null ? "—" : pct(ligne.margeReelle)}</strong>
          </li>`).join("")}
        </ul>
      </article>
    </section>
    <section class="band">
      <h2>Quatre gestes, une marge.</h2>
      <div class="steps">
        ${etape("01", "Tableau de bord", "Le facturé, le dépensé et l'écart avec le devis restent visibles. Une alerte s'allume quand la marge réelle décroche de plus de 3 points.")}
        ${etape("02", "Chiffrage", "Chaque poste part du déboursé sec. Le prix de vente suit le coefficient, le prix de revient ou un prix saisi, et la marge se met à jour.")}
        ${etape("03", "Situations", "L'avancement par poste calcule la situation du mois, la retenue de garantie, le compte prorata, la TVA ou l'autoliquidation, puis le DGD.")}
        ${etape("04", "Heures et achats", "Une heure pointée et une facture fournisseur entrent dans le dépensé du chantier. La marge n'attend pas la comptabilité.")}
      </div>
    </section>
    <section class="band band-quiet">
      <h2>${alertes.length ? "Ce que la démo montre déjà" : "La démo part d'une entreprise fictive"}</h2>
      <ul class="alert-list">
        ${alertes.length ? alertes.map((texte) => `<li>${esc(texte)}</li>`).join("") : "<li>Ajoutez un achat ou des heures pour voir la marge bouger.</li>"}
      </ul>
      <a class="button" href="#/app">Entrer dans Atelier des Cimes</a>
    </section>
    <footer class="landing-foot">
      <p>Solive est une démonstration indépendante. L'entreprise, les chantiers et les montants sont fictifs.</p>
    </footer>
  </div>`;
}

function pageTableau(state) {
  const entreprise = resumeEntreprise(state);
  const alertes = entreprise.rows.flatMap((ligne) => phrases(ligne));
  const brouillons = state.situations.filter((situation) => situation.statut === "brouillon");
  return `<section class="page">
    <p class="kicker">Direction</p>
    <h1>Tableau de bord</h1>
    <div class="metrics">
      ${metrique("Facturé HT", eur(entreprise.facture), "Situations validées ou envoyées")}
      ${metrique("Dépensé", eur(entreprise.depense), "Heures pointées et achats")}
      ${metrique("Reste à dépenser", eur(entreprise.resteDepenser), "Déboursé du devis moins le réalisé")}
      ${metrique("Marge réelle", entreprise.margeReelle == null ? "—" : pct(entreprise.margeReelle), "Sur le facturé des chantiers ouverts")}
    </div>
    ${alertes.length ? `<aside class="callout"><h2>Points d'attention</h2><ul>${alertes.map((texte) => `<li>${esc(texte)}</li>`).join("")}</ul></aside>` : ""}
    <div class="split">
      <section>
        <h2>Marge par chantier</h2>
        <div class="bars">
          ${entreprise.rows.map((ligne) => barre(ligne)).join("")}
        </div>
      </section>
      <section>
        <h2>Situations à reprendre</h2>
        ${brouillons.length ? `<ul class="stack-list">${brouillons.map((situation) => {
          const chantier = state.chantiers.find((item) => item.id === situation.chantierId);
          const detail = detailSituation(state, situation);
          return `<li><a href="#/app/situations/${situation.id}"><strong>${esc(chantier?.nom ?? "Chantier")}</strong><span>Situation ${situation.numero} · ${eur(detail.mois)}</span></a></li>`;
        }).join("")}</ul>` : `<p class="muted">Aucun brouillon en cours.</p>`}
      </section>
    </div>
    <h2>Facturé et dépensé</h2>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Chantier</th><th>Devis HT</th><th>Facturé</th><th>Dépensé</th><th>Reste à facturer</th><th>Marge devis</th><th>Marge réelle</th></tr></thead>
        <tbody>
          ${entreprise.rows.map((ligne) => `<tr>
            <td><a href="#/app/chantiers/${ligne.chantier.id}">${esc(ligne.chantier.nom)}</a></td>
            <td class="num">${eur(ligne.totaux.pv)}</td>
            <td class="num">${eur(ligne.facture)}</td>
            <td class="num">${eur(ligne.dep.total)}</td>
            <td class="num">${eur(ligne.resteFacturer)}</td>
            <td class="num">${pct(ligne.totaux.marge)}</td>
            <td class="num ${ligne.attentionMarge ? "is-alert" : ""}">${ligne.margeReelle == null ? "—" : pct(ligne.margeReelle)}</td>
          </tr>`).join("")}
        </tbody>
      </table>
    </div>
  </section>`;
}

function pageChantiers(state) {
  return `<section class="page">
    <p class="kicker">Portefeuille</p>
    <h1>Chantiers</h1>
    <div class="cards">
      ${state.chantiers.map((chantier) => {
        const resume = resumeChantier(state, chantier.id);
        return `<a class="card" href="#/app/chantiers/${chantier.id}">
          <p class="card-kicker">${esc(libelleStatutChantier(chantier.statut))} · ${esc(chantier.ville)}</p>
          <h2>${esc(chantier.nom)}</h2>
          <p>${esc(chantier.client)}</p>
          <dl>
            <div><dt>Devis</dt><dd>${eur(resume.totaux.pv)}</dd></div>
            <div><dt>Marge réelle</dt><dd class="${resume.attentionMarge ? "is-alert" : ""}">${resume.margeReelle == null ? "—" : pct(resume.margeReelle)}</dd></div>
          </dl>
        </a>`;
      }).join("")}
    </div>
    <form class="panel form-grid">
      <h2>Nouveau chantier</h2>
      <label>Nom<input name="nom" required maxlength="80"></label>
      <label>Client<input name="client" required maxlength="80"></label>
      <label>Ville<input name="ville" required maxlength="80"></label>
      <label>Début<input name="debut" type="date" value="2026-12-01" required></label>
      <label>Fin<input name="fin" type="date" value="2027-04-30" required></label>
      <button class="button" type="button" data-action="creer-chantier">Créer le chantier</button>
    </form>
  </section>`;
}

function pageChantier(state, id) {
  const chantier = state.chantiers.find((item) => item.id === id);
  if (!chantier) return introuvable("Chantier introuvable", "#/app/chantiers");
  const resume = resumeChantier(state, id);
  const devis = resume.devis;
  const situations = situationsChantier(state, id);
  const decision = peutCreerDgd(state, id);
  const brouillon = situations.find((situation) => situation.statut === "brouillon");
  return `<section class="page">
    <p class="kicker"><a href="#/app/chantiers">Chantiers</a> · ${esc(chantier.client)}</p>
    <div class="title-row">
      <h1>${esc(chantier.nom)}</h1>
      <label class="inline">Statut
        <select data-bind="statut-chantier" data-chantier="${chantier.id}">
          ${options([["etude", "Étude"], ["en_cours", "En cours"], ["termine", "Terminé"]], chantier.statut)}
        </select>
      </label>
    </div>
    <p class="lede">${esc(chantier.ville)} · du ${libelleDate(chantier.debut)} au ${libelleDate(chantier.fin)}</p>
    <div class="metrics">
      ${metrique("Devis HT", eur(resume.totaux.pv), devis ? devis.numero : "Pas encore de devis")}
      ${metrique("Facturé", eur(resume.facture))}
      ${metrique("Dépensé", eur(resume.dep.total), `${num(resume.dep.heures)} h pointées`)}
      ${metrique("Marge réelle", resume.margeReelle == null ? "—" : pct(resume.margeReelle), `Devis ${pct(resume.totaux.marge)}`)}
    </div>
    <div class="split">
      <section class="panel">
        <h2>Déboursé et réalisé</h2>
        <table>
          <thead><tr><th></th><th>Prévu</th><th>Réalisé</th></tr></thead>
          <tbody>
            <tr><td>Main-d'œuvre</td><td class="num">${eur(resume.totaux.mo)}</td><td class="num">${eur(resume.dep.mo)}</td></tr>
            <tr><td>Fournitures</td><td class="num">${eur(resume.totaux.materiaux)}</td><td class="num">${eur(resume.dep.materiaux)}</td></tr>
            <tr><td>Sous-traitance</td><td class="num">${eur(resume.totaux.sousTraitance)}</td><td class="num">${eur(resume.dep.sousTraitance)}</td></tr>
            <tr><td>Heures</td><td class="num">${num(resume.totaux.heures)} h</td><td class="num ${resume.depassementHeures ? "is-alert" : ""}">${num(resume.dep.heures)} h</td></tr>
          </tbody>
        </table>
      </section>
      <section class="panel">
        <h2>Règles de facturation</h2>
        <div class="form-grid">
          <label>Retenue de garantie %<input data-bind="ratio" data-key="retenueGarantie" data-chantier="${chantier.id}" type="number" min="0" max="20" step="0.1" value="${pourcentageSaisi(chantier.retenueGarantie)}"></label>
          <label>Compte prorata %<input data-bind="ratio" data-key="compteProrata" data-chantier="${chantier.id}" type="number" min="0" max="20" step="0.1" value="${pourcentageSaisi(chantier.compteProrata)}"></label>
          <label>TVA %<input data-bind="ratio" data-key="tva" data-chantier="${chantier.id}" type="number" min="0" max="20" step="0.1" value="${pourcentageSaisi(chantier.tva)}"></label>
          <label class="check"><input data-bind="flag" data-chantier="${chantier.id}" type="checkbox"${chantier.autoliquidation ? " checked" : ""}> Autoliquidation de TVA</label>
        </div>
        <div class="button-row">
          ${devis ? `<a class="button button-ghost" href="#/app/devis/${devis.id}">Ouvrir le devis</a>` : `<button class="button" type="button" data-action="creer-devis" data-chantier="${chantier.id}">Créer le devis</button>`}
          ${brouillon ? `<a class="button" href="#/app/situations/${brouillon.id}">Situation en cours</a>` : `<button class="button" type="button" data-action="creer-situation" data-chantier="${chantier.id}"${devis?.statut === "signe" ? "" : " disabled"}>Nouvelle situation</button>`}
          <button class="button button-ghost" type="button" data-action="creer-dgd" data-chantier="${chantier.id}"${decision.ok ? "" : " disabled"}>Établir le DGD</button>
          ${decision.ok ? "" : `<p class="muted">${esc(decision.raison)}</p>`}
        </div>
      </section>
    </div>
  </section>`;
}

function pageDevisListe(state) {
  return `<section class="page">
    <p class="kicker">Chiffrage</p>
    <h1>Devis</h1>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Numéro</th><th>Chantier</th><th>Méthode</th><th>Statut</th><th>Déboursé</th><th>Vente HT</th><th>Marge</th></tr></thead>
        <tbody>
          ${state.devis.map((devis) => {
            const totaux = devisTotaux(devis);
            const chantier = state.chantiers.find((item) => item.id === devis.chantierId);
            return `<tr>
              <td><a href="#/app/devis/${devis.id}">${esc(devis.numero)}</a></td>
              <td>${esc(chantier?.nom ?? "")}</td>
              <td>${esc(libelleMethode(devis.methode))}</td>
              <td>${esc(libelleStatutDevis(devis.statut))}</td>
              <td class="num">${eur(totaux.ds)}</td>
              <td class="num">${eur(totaux.pv)}</td>
              <td class="num">${pct(totaux.marge)}</td>
            </tr>`;
          }).join("")}
        </tbody>
      </table>
    </div>
  </section>`;
}

function pageDevis(state, id) {
  const devis = state.devis.find((item) => item.id === id);
  if (!devis) return introuvable("Devis introuvable", "#/app/devis");
  const chantier = state.chantiers.find((item) => item.id === devis.chantierId);
  const totaux = devisTotaux(devis);
  const vente = devis.methode === "vente";
  return `<section class="page" data-paint="devis" data-id="${devis.id}">
    <p class="kicker"><a href="#/app/devis">Devis</a> · ${esc(chantier?.nom ?? "")}</p>
    <div class="title-row">
      <h1>${esc(devis.numero)}</h1>
      <div class="button-row">
        <button class="button button-ghost" type="button" data-action="statut-devis" data-devis="${devis.id}" data-statut="brouillon">Brouillon</button>
        <button class="button button-ghost" type="button" data-action="statut-devis" data-devis="${devis.id}" data-statut="envoye">Envoyé</button>
        <button class="button" type="button" data-action="statut-devis" data-devis="${devis.id}" data-statut="signe">Signé</button>
      </div>
    </div>
    <p class="lede">Statut : ${esc(libelleStatutDevis(devis.statut))}. ${phraseMethode(devis.methode)}</p>
    <div class="toolbar">
      <label>Méthode
        <select data-bind="methode" data-devis="${devis.id}">
          ${options([["debourse", "Déboursé sec"], ["revient", "Prix de revient"], ["vente", "Prix de vente"]], devis.methode)}
        </select>
      </label>
      <label>Frais généraux %
        <input data-bind="frais" data-devis="${devis.id}" type="number" min="0" step="0.1" value="${pourcentageSaisi(devis.fraisGeneraux)}">
      </label>
      <label>Bibliothèque
        <select data-bibliotheque="${devis.id}">
          <option value="">Choisir un poste</option>
          ${state.bibliotheque.map((item, index) => `<option value="${index}">${esc(item.designation)} · ${eur2(item.debourseUnitaire)}</option>`).join("")}
        </select>
      </label>
      <button class="button button-ghost" type="button" data-action="ajouter-bibliotheque" data-devis="${devis.id}">Ajouter</button>
      <button class="button" type="button" data-action="ajouter-ligne" data-devis="${devis.id}">Ligne vide</button>
    </div>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Poste</th><th>Lot</th><th>Nature</th><th>Unité</th><th>Qté</th><th>Déboursé u.</th><th>Coeff.</th>${vente ? "<th>PV forcé u.</th>" : ""}<th>PV</th><th>Marge</th><th></th></tr></thead>
        <tbody>
          ${devis.lignes.map((ligne) => ligneDevis(devis, ligne, vente)).join("")}
        </tbody>
      </table>
    </div>
    <div class="totals">
      <p>Déboursé <strong data-live="totaux-ds">${eur(totaux.ds)}</strong></p>
      <p>Prix de revient <strong data-live="totaux-pr">${eur(totaux.pr)}</strong></p>
      <p>Vente HT <strong data-live="totaux-pv">${eur(totaux.pv)}</strong></p>
      <p>Marge <strong data-live="totaux-marge">${pct(totaux.marge)}</strong></p>
    </div>
  </section>`;
}

function ligneDevis(devis, ligne, vente) {
  const montants = ligneMontants(ligne, devis);
  const pu = ligne.qte > 0 ? montants.pv / ligne.qte : 0;
  return `<tr>
    <td><input data-bind="ligne" data-key="designation" data-devis="${devis.id}" data-ligne="${ligne.id}" value="${esc(ligne.designation)}"></td>
    <td><input data-bind="ligne" data-key="lot" data-devis="${devis.id}" data-ligne="${ligne.id}" value="${esc(ligne.lot)}"></td>
    <td><select data-bind="ligne-choix" data-key="nature" data-devis="${devis.id}" data-ligne="${ligne.id}">${options(NATURES, ligne.nature)}</select></td>
    <td><input class="short" data-bind="ligne" data-key="unite" data-devis="${devis.id}" data-ligne="${ligne.id}" value="${esc(ligne.unite)}"></td>
    <td><input class="num-input" data-bind="ligne" data-key="qte" data-devis="${devis.id}" data-ligne="${ligne.id}" type="number" min="0" step="0.5" value="${ligne.qte}"></td>
    <td><input class="num-input" data-bind="ligne" data-key="debourseUnitaire" data-devis="${devis.id}" data-ligne="${ligne.id}" type="number" min="0" step="0.01" value="${ligne.debourseUnitaire}"></td>
    <td><input class="num-input" data-bind="ligne" data-key="coefficient" data-devis="${devis.id}" data-ligne="${ligne.id}" type="number" min="0" step="0.01" value="${ligne.coefficient}"></td>
    ${vente ? `<td><input class="num-input" data-bind="ligne" data-key="prixVenteForce" data-devis="${devis.id}" data-ligne="${ligne.id}" type="number" min="0" step="0.01" value="${ligne.prixVenteForce ?? ""}"></td>` : ""}
    <td class="num" data-live="ligne-pv" data-ligne="${ligne.id}">${eur2(pu)} · ${eur(montants.pv)}</td>
    <td class="num" data-live="ligne-marge" data-ligne="${ligne.id}">${pct(montants.marge)}</td>
    <td><button class="text-button" type="button" data-action="supprimer-ligne" data-devis="${devis.id}" data-ligne="${ligne.id}">Retirer</button></td>
  </tr>`;
}

function pageSituations(state) {
  return `<section class="page">
    <div class="title-row">
      <div>
        <p class="kicker">Facturation</p>
        <h1>Situations</h1>
      </div>
      <button class="button button-ghost" type="button" data-action="exporter">Exporter CSV</button>
    </div>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Chantier</th><th>N°</th><th>Date</th><th>Statut</th><th>Mois HT</th><th>Net HT</th><th>TTC</th></tr></thead>
        <tbody>
          ${state.situations.map((situation) => {
            const detail = detailSituation(state, situation);
            return `<tr>
              <td><a href="#/app/situations/${situation.id}">${esc(detail.chantier?.nom ?? "")}</a></td>
              <td>${situation.type === "dgd" ? "DGD" : situation.numero}</td>
              <td>${libelleDate(situation.date)}</td>
              <td>${esc(libelleStatutSituation(situation.statut))}</td>
              <td class="num">${eur(detail.mois)}</td>
              <td class="num">${eur(detail.netHT)}</td>
              <td class="num">${eur(detail.ttc)}</td>
            </tr>`;
          }).join("")}
        </tbody>
      </table>
    </div>
  </section>`;
}

function pageSituation(state, id) {
  const situation = state.situations.find((item) => item.id === id);
  if (!situation) return introuvable("Situation introuvable", "#/app/situations");
  const detail = detailSituation(state, situation);
  const figee = situation.type === "dgd" || situation.statut !== "brouillon";
  return `<section class="page" data-paint="situation" data-id="${situation.id}">
    <p class="kicker"><a href="#/app/situations">Situations</a> · ${esc(detail.chantier?.nom ?? "")}</p>
    <div class="title-row">
      <h1>${situation.type === "dgd" ? "Décompte général et définitif" : `Situation ${situation.numero}`}</h1>
      <div class="button-row">
        ${situation.statut === "brouillon" ? `<button class="button" type="button" data-action="statut-situation" data-situation="${situation.id}" data-statut="validee">Valider</button>` : ""}
        ${situation.statut === "validee" ? `<button class="button" type="button" data-action="statut-situation" data-situation="${situation.id}" data-statut="envoyee">Marquer envoyée</button>` : ""}
        ${situation.statut === "brouillon" ? `<button class="text-button" type="button" data-action="supprimer-situation" data-situation="${situation.id}">Supprimer le brouillon</button>` : ""}
      </div>
    </div>
    <p class="lede">${libelleDate(situation.date)} · ${esc(libelleStatutSituation(situation.statut))}${detail.autoliquidation ? " · TVA en autoliquidation" : ""}</p>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Poste</th><th>Vente</th><th>Avancement cumulé</th><th>Montant cumulé</th></tr></thead>
        <tbody>
          ${detail.lignes.map((ligne) => {
            const plancher = Math.round(avancementPrecedent(state, situation, ligne.ligne.id) * 100);
            return `<tr>
              <td>${esc(ligne.ligne.designation)}</td>
              <td class="num">${eur(ligne.pv)}</td>
              <td class="avancement">
                <input data-bind="avancement" data-situation="${situation.id}" data-ligne="${ligne.ligne.id}" type="range" min="${plancher}" max="100" step="1" value="${Math.round(ligne.avancement * 100)}"${figee ? " disabled" : ""}>
                <span data-live="avancement" data-ligne="${ligne.ligne.id}">${pct(ligne.avancement)}</span>
              </td>
              <td class="num" data-live="montant" data-ligne="${ligne.ligne.id}">${eur(ligne.montant)}</td>
            </tr>`;
          }).join("")}
        </tbody>
      </table>
    </div>
    <aside class="totals totals-block" aria-live="polite">
      <p>Cumul <strong data-live="cumul">${eur2(detail.cumul)}</strong></p>
      <p>Déjà facturé <strong data-live="precedent">${eur2(detail.precedent)}</strong></p>
      <p>Situation du mois <strong data-live="mois">${eur2(detail.mois)}</strong></p>
      <p>Retenue de garantie <strong data-live="retenue">${eur2(detail.retenueAppliquee)}</strong></p>
      <p>Compte prorata <strong data-live="prorata">${eur2(detail.prorata)}</strong></p>
      ${detail.liberation ? `<p>Retenues libérées <strong data-live="liberation">${eur2(detail.liberation)}</strong></p>` : `<p data-live="liberation-row" hidden>Retenues libérées <strong data-live="liberation">${eur2(0)}</strong></p>`}
      <p>Net HT <strong data-live="net">${eur2(detail.netHT)}</strong></p>
      <p>TVA <strong data-live="tva">${detail.autoliquidation ? "Autoliquidation" : eur2(detail.tva)}</strong></p>
      <p>TTC <strong data-live="ttc">${eur2(detail.ttc)}</strong></p>
    </aside>
  </section>`;
}

function pageAchats(state) {
  const totalAPayer = state.achats.filter((achat) => achat.statut === "a_payer").reduce((total, achat) => total + achat.montantHT, 0);
  return `<section class="page">
    <p class="kicker">Dépenses</p>
    <h1>Achats</h1>
    <div class="metrics">
      ${metrique("À payer", eur(totalAPayer))}
      ${metrique("Factures", String(state.achats.length), "Rattachées à un chantier")}
    </div>
    <form class="panel form-grid">
      <h2>Nouvelle facture</h2>
      <label>Fournisseur<input name="fournisseur" required maxlength="80"></label>
      <label>Libellé<input name="designation" required maxlength="120"></label>
      <label>Chantier
        <select name="chantier" required>
          ${state.chantiers.map((chantier) => `<option value="${chantier.id}">${esc(chantier.nom)}</option>`).join("")}
        </select>
      </label>
      <label>Nature
        <select name="typologie">
          <option value="materiaux">Fournitures</option>
          <option value="sous_traitance">Sous-traitance</option>
        </select>
      </label>
      <label>Montant HT<input name="montant" type="number" min="0" step="0.01" required></label>
      <label>Date<input name="date" type="date" value="${AUJOURDHUI}" required></label>
      <button class="button" type="button" data-action="creer-achat">Enregistrer</button>
    </form>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Date</th><th>Fournisseur</th><th>Chantier</th><th>Nature</th><th>Montant</th><th>Statut</th><th></th></tr></thead>
        <tbody>
          ${[...state.achats].reverse().map((achat) => {
            const chantier = state.chantiers.find((item) => item.id === achat.chantierId);
            return `<tr>
              <td>${libelleDate(achat.date)}</td>
              <td>${esc(achat.fournisseur)}<br><span class="muted">${esc(achat.designation)}</span></td>
              <td>${esc(chantier?.nom ?? "")}</td>
              <td>${achat.typologie === "sous_traitance" ? "Sous-traitance" : "Fournitures"}</td>
              <td class="num">${eur(achat.montantHT)}</td>
              <td><button class="text-button" type="button" data-action="statut-achat" data-achat="${achat.id}">${achat.statut === "payee" ? "Payée" : "À payer"}</button></td>
              <td><button class="text-button" type="button" data-action="supprimer-achat" data-achat="${achat.id}">Retirer</button></td>
            </tr>`;
          }).join("")}
        </tbody>
      </table>
    </div>
  </section>`;
}

function pagePlanning(state) {
  const jours = joursOuvres(state.semaine);
  const ouverts = state.chantiers.filter((chantier) => chantier.statut !== "termine");
  return `<section class="page">
    <p class="kicker">Terrain</p>
    <div class="title-row">
      <h1>Semaine du ${libelleDate(state.semaine)}</h1>
      <div class="button-row">
        <button class="button button-ghost" type="button" data-action="semaine" data-sens="-1">Semaine précédente</button>
        <button class="button button-ghost" type="button" data-action="semaine" data-sens="1">Semaine suivante</button>
      </div>
    </div>
    <p class="lede">Les heures saisies s'ajoutent au dépensé de main-d'œuvre du chantier, au taux de chaque compagnon.</p>
    <div class="table-wrap">
      <table class="planning">
        <thead><tr><th>Compagnon</th>${jours.map((jour) => `<th>${esc(libelleJour(jour))}</th>`).join("")}<th>Total</th></tr></thead>
        <tbody>
          ${state.compagnons.map((compagnon) => {
            let total = 0;
            const cellules = jours.map((jour) => {
              const pointage = state.pointages.find((item) => item.compagnonId === compagnon.id && item.date === jour);
              total += pointage?.heures ?? 0;
              return `<td class="${pointage ? teinte(state, pointage.chantierId) : ""}">
                <div data-pointage data-compagnon="${compagnon.id}" data-date="${jour}">
                  <select data-bind="pointage" data-role="chantier">
                    <option value="">—</option>
                    ${ouverts.map((chantier) => `<option value="${chantier.id}"${pointage?.chantierId === chantier.id ? " selected" : ""}>${esc(chantier.nom)}</option>`).join("")}
                  </select>
                  <input data-bind="pointage" data-role="heures" type="number" min="0" max="12" step="0.5" value="${pointage?.heures ?? ""}" aria-label="Heures de ${esc(compagnon.nom)} le ${jour}">
                </div>
              </td>`;
            }).join("");
            return `<tr><th>${esc(compagnon.nom)}<span>${esc(compagnon.metier)} · ${eur(compagnon.taux)} / h</span></th>${cellules}<td class="num">${num(total)} h</td></tr>`;
          }).join("")}
        </tbody>
      </table>
    </div>
  </section>`;
}

function peindreDevis(state, id) {
  const devis = state.devis.find((item) => item.id === id);
  if (!devis) return;
  const totaux = devisTotaux(devis);
  for (const ligne of devis.lignes) {
    const montants = ligneMontants(ligne, devis);
    const pu = ligne.qte > 0 ? montants.pv / ligne.qte : 0;
    ecrire(`[data-live="ligne-pv"][data-ligne="${ligne.id}"]`, `${eur2(pu)} · ${eur(montants.pv)}`);
    ecrire(`[data-live="ligne-marge"][data-ligne="${ligne.id}"]`, pct(montants.marge));
  }
  ecrire('[data-live="totaux-ds"]', eur(totaux.ds));
  ecrire('[data-live="totaux-pr"]', eur(totaux.pr));
  ecrire('[data-live="totaux-pv"]', eur(totaux.pv));
  ecrire('[data-live="totaux-marge"]', pct(totaux.marge));
}

function peindreSituation(state, id) {
  const situation = state.situations.find((item) => item.id === id);
  if (!situation) return;
  const detail = detailSituation(state, situation);
  for (const ligne of detail.lignes) {
    ecrire(`[data-live="avancement"][data-ligne="${ligne.ligne.id}"]`, pct(ligne.avancement));
    ecrire(`[data-live="montant"][data-ligne="${ligne.ligne.id}"]`, eur(ligne.montant));
  }
  ecrire('[data-live="cumul"]', eur2(detail.cumul));
  ecrire('[data-live="precedent"]', eur2(detail.precedent));
  ecrire('[data-live="mois"]', eur2(detail.mois));
  ecrire('[data-live="retenue"]', eur2(detail.retenueAppliquee));
  ecrire('[data-live="prorata"]', eur2(detail.prorata));
  ecrire('[data-live="liberation"]', eur2(detail.liberation));
  ecrire('[data-live="net"]', eur2(detail.netHT));
  ecrire('[data-live="tva"]', detail.autoliquidation ? "Autoliquidation" : eur2(detail.tva));
  ecrire('[data-live="ttc"]', eur2(detail.ttc));
}

function ecrire(selecteur, texte) {
  const noeud = document.querySelector(selecteur);
  if (noeud) noeud.textContent = texte;
}

function barre(ligne) {
  const ratio = Math.max(0, ligne.margeReelle ?? ligne.totaux.marge);
  const largeur = Math.max(ligne.attentionMarge ? 10 : 0, Math.min(100, ratio * 100));
  return `<a class="bar-row" href="#/app/chantiers/${ligne.chantier.id}">
    <span>${esc(ligne.chantier.nom)}</span>
    <span class="bar ${ligne.attentionMarge ? "is-alert" : ""}"><i style="width:${largeur}%"></i></span>
    <strong>${ligne.margeReelle == null ? `${pct(ligne.totaux.marge)} devis` : pct(ligne.margeReelle)}</strong>
  </a>`;
}

function metrique(label, valeur, detail = "") {
  return `<article class="metric"><p>${label}</p><strong>${valeur}</strong>${detail ? `<span>${detail}</span>` : ""}</article>`;
}

function etape(numero, titre, texte) {
  return `<article><p>${numero}</p><h3>${titre}</h3><p>${texte}</p></article>`;
}

function phrases(ligne) {
  const textes = [];
  if (ligne.attentionMarge) textes.push(phraseAlerte(ligne));
  if (ligne.depassementHeures) {
    textes.push(`${ligne.chantier.nom} : ${num(ligne.dep.heures)} h pointées pour ${num(ligne.totaux.heures)} h prévues au devis.`);
  }
  return textes;
}

function phraseAlerte(ligne) {
  if (ligne.attentionMarge) {
    const points = num((ligne.ecartMarge ?? 0) * 100);
    return `${ligne.chantier.nom} : marge réelle ${pct(ligne.margeReelle)}, ${points} pts sous le devis.`;
  }
  return `${ligne.chantier.nom} : ${num(ligne.dep.heures)} h pointées pour ${num(ligne.totaux.heures)} h prévues au devis.`;
}

function options(liste, courant) {
  return liste.map(([valeur, label]) => {
    const selected = valeur === courant ? " selected" : "";
    return `<option value="${esc(valeur)}"${selected}>${esc(label)}</option>`;
  }).join("");
}

function pourcentageSaisi(ratio) {
  return String(Math.round(ratio * 1000) / 10);
}

function teinte(state, chantierId) {
  const index = Math.max(0, state.chantiers.findIndex((chantier) => chantier.id === chantierId));
  return `teinte-${index % 4}`;
}

function introuvable(message, href) {
  return `<section class="page"><h1>${esc(message)}</h1><a class="button" href="${href}">Retour</a></section>`;
}

function libelleStatutChantier(statut) {
  return { etude: "Étude", en_cours: "En cours", termine: "Terminé" }[statut] ?? statut;
}

function libelleStatutDevis(statut) {
  return { brouillon: "Brouillon", envoye: "Envoyé", signe: "Signé" }[statut] ?? statut;
}

function libelleStatutSituation(statut) {
  return { brouillon: "Brouillon", validee: "Validée", envoyee: "Envoyée" }[statut] ?? statut;
}

function libelleMethode(methode) {
  return { debourse: "Déboursé sec", revient: "Prix de revient", vente: "Prix de vente" }[methode] ?? methode;
}

function phraseMethode(methode) {
  if (methode === "revient") return "Le prix de vente reprend le déboursé, les frais généraux, puis le coefficient.";
  if (methode === "vente") return "Le prix de vente est saisi. La marge se mesure face au déboursé.";
  return "Le prix de vente est le déboursé multiplié par le coefficient.";
}
