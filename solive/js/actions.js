import { peutCreerDgd, avancementPrecedent, devisPrincipal, situationsChantier, detailSituation, ligneMontants } from "./calc.js";
import { ajouterJours, AUJOURDHUI } from "./dates.js";
import { uid } from "./format.js";
import { peindre } from "./views.js";
import { commit, getState, reinitialiser } from "./store.js";

export function gererClic(element) {
  const action = element.dataset.action;
  if (action === "reinitialiser") {
    reinitialiser();
    return;
  }
  if (action === "exporter") {
    exporterSituations(getState());
    return;
  }
  if (action === "creer-chantier") {
    const formulaire = element.closest("form");
    if (!formulaire.reportValidity()) return;
    const donnees = new FormData(formulaire);
    const id = uid("ch");
    commit((brouillon) => {
      brouillon.chantiers.push({
        id,
        nom: String(donnees.get("nom")).trim(),
        client: String(donnees.get("client")).trim(),
        ville: String(donnees.get("ville")).trim(),
        statut: "etude",
        debut: String(donnees.get("debut")),
        fin: String(donnees.get("fin")),
        retenueGarantie: 0.05,
        compteProrata: 0,
        autoliquidation: false,
        tva: 0.1,
      });
      brouillon.historique[id] = { heures: 0, cout: 0 };
    });
    location.hash = `#/app/chantiers/${id}`;
    return;
  }
  if (action === "creer-devis") {
    const chantierId = element.dataset.chantier;
    const existant = getState().devis.find((devis) => devis.chantierId === chantierId);
    if (existant) {
      location.hash = `#/app/devis/${existant.id}`;
      return;
    }
    const id = uid("dv");
    commit((brouillon) => {
      const rang = brouillon.devis.length + 1;
      brouillon.devis.push({
        id,
        chantierId,
        numero: `D-2026-${String(rang).padStart(3, "0")}`,
        statut: "brouillon",
        methode: "debourse",
        fraisGeneraux: 0.08,
        lignes: [],
      });
    });
    location.hash = `#/app/devis/${id}`;
    return;
  }
  if (action === "statut-devis") {
    commit((brouillon) => {
      const devis = brouillon.devis.find((item) => item.id === element.dataset.devis);
      if (devis) devis.statut = element.dataset.statut;
    });
    return;
  }
  if (action === "ajouter-bibliotheque") {
    const select = document.querySelector(`[data-bibliotheque="${element.dataset.devis}"]`);
    if (!select || select.value === "") return;
    const index = Number(select.value);
    commit((brouillon) => {
      const devis = brouillon.devis.find((item) => item.id === element.dataset.devis);
      const modele = brouillon.bibliotheque[index];
      if (!devis || !modele) return;
      devis.lignes.push({
        id: uid("lg"),
        lot: "Lot",
        designation: modele.designation,
        unite: modele.unite,
        qte: modele.unite === "forfait" ? 1 : 0,
        nature: modele.nature,
        debourseUnitaire: modele.debourseUnitaire,
        coefficient: 1.35,
        prixVenteForce: null,
      });
    });
    return;
  }
  if (action === "ajouter-ligne") {
    commit((brouillon) => {
      const devis = brouillon.devis.find((item) => item.id === element.dataset.devis);
      devis?.lignes.push({
        id: uid("lg"),
        lot: "Lot",
        designation: "Nouveau poste",
        unite: "u",
        qte: 1,
        nature: "materiaux",
        debourseUnitaire: 0,
        coefficient: 1.35,
        prixVenteForce: null,
      });
    });
    return;
  }
  if (action === "supprimer-ligne") {
    commit((brouillon) => {
      const devis = brouillon.devis.find((item) => item.id === element.dataset.devis);
      if (!devis) return;
      devis.lignes = devis.lignes.filter((ligne) => ligne.id !== element.dataset.ligne);
    });
    return;
  }
  if (action === "creer-situation") {
    const chantierId = element.dataset.chantier;
    const state = getState();
    const devis = devisPrincipal(state, chantierId);
    if (!devis || devis.statut !== "signe") return;
    const existante = situationsChantier(state, chantierId).find((item) => item.statut === "brouillon");
    if (existante) {
      location.hash = `#/app/situations/${existante.id}`;
      return;
    }
    const id = uid("sit");
    commit((brouillon) => {
      const liste = situationsChantier(brouillon, chantierId);
      const precedente = liste.at(-1);
      brouillon.situations.push({
        id,
        chantierId,
        devisId: devis.id,
        numero: (precedente?.numero ?? 0) + 1,
        date: AUJOURDHUI,
        statut: "brouillon",
        type: "situation",
        libereRetenue: false,
        avancement: { ...(precedente?.avancement ?? {}) },
      });
    });
    location.hash = `#/app/situations/${id}`;
    return;
  }
  if (action === "statut-situation") {
    commit((brouillon) => {
      const situation = brouillon.situations.find((item) => item.id === element.dataset.situation);
      if (!situation || situation.type === "dgd") return;
      situation.statut = element.dataset.statut;
      if (situation.statut !== "brouillon") figerPrix(situation, brouillon);
    });
    return;
  }
  if (action === "supprimer-situation") {
    commit((brouillon) => {
      brouillon.situations = brouillon.situations.filter((item) => {
        return !(item.id === element.dataset.situation && item.statut === "brouillon");
      });
    });
    location.hash = "#/app/situations";
    return;
  }
  if (action === "creer-dgd") {
    const chantierId = element.dataset.chantier;
    const decision = peutCreerDgd(getState(), chantierId);
    if (!decision.ok) return;
    const id = uid("sit");
    commit((brouillon) => {
      const liste = situationsChantier(brouillon, chantierId);
      const avancement = {};
      for (const ligne of decision.devis.lignes) avancement[ligne.id] = 1;
      const dgd = {
        id,
        chantierId,
        devisId: decision.devis.id,
        numero: (liste.at(-1)?.numero ?? 0) + 1,
        date: AUJOURDHUI,
        statut: "validee",
        type: "dgd",
        libereRetenue: true,
        avancement,
      };
      figerPrix(dgd, brouillon);
      brouillon.situations.push(dgd);
      const chantier = brouillon.chantiers.find((item) => item.id === chantierId);
      if (chantier) chantier.statut = "termine";
    });
    location.hash = `#/app/situations/${id}`;
    return;
  }
  if (action === "creer-achat") {
    const formulaire = element.closest("form");
    if (!formulaire.reportValidity()) return;
    const donnees = new FormData(formulaire);
    commit((brouillon) => {
      brouillon.achats.push({
        id: uid("ach"),
        chantierId: String(donnees.get("chantier")),
        fournisseur: String(donnees.get("fournisseur")).trim(),
        designation: String(donnees.get("designation")).trim(),
        typologie: String(donnees.get("typologie")),
        montantHT: Number(donnees.get("montant")),
        date: String(donnees.get("date")),
        statut: "a_payer",
      });
    });
    formulaire.reset();
    return;
  }
  if (action === "supprimer-achat") {
    commit((brouillon) => {
      brouillon.achats = brouillon.achats.filter((achat) => achat.id !== element.dataset.achat);
    });
    return;
  }
  if (action === "statut-achat") {
    commit((brouillon) => {
      const achat = brouillon.achats.find((item) => item.id === element.dataset.achat);
      if (achat) achat.statut = achat.statut === "payee" ? "a_payer" : "payee";
    });
    return;
  }
  if (action === "semaine") {
    const sens = Number(element.dataset.sens);
    commit((brouillon) => {
      brouillon.semaine = ajouterJours(brouillon.semaine, sens * 7);
    });
  }
}

export function gererSaisie(element) {
  const bind = element.dataset.bind;
  if (!bind) return;
  if (bind === "ligne") {
    commit((brouillon) => {
      const devis = brouillon.devis.find((item) => item.id === element.dataset.devis);
      const ligne = devis?.lignes.find((item) => item.id === element.dataset.ligne);
      if (!ligne) return;
      ecrireLigne(ligne, element.dataset.key, element.value);
    }, { notify: false });
    peindre(getState());
    return;
  }
  if (bind === "frais") {
    commit((brouillon) => {
      const devis = brouillon.devis.find((item) => item.id === element.dataset.devis);
      if (devis) devis.fraisGeneraux = Math.max(0, Number(element.value) || 0) / 100;
    }, { notify: false });
    peindre(getState());
    return;
  }
  if (bind === "avancement") {
    commit((brouillon) => {
      const situation = brouillon.situations.find((item) => item.id === element.dataset.situation);
      if (!situation || situation.type === "dgd") return;
      const plancher = avancementPrecedent(brouillon, situation, element.dataset.ligne);
      const valeur = (Number(element.value) || 0) / 100;
      situation.avancement[element.dataset.ligne] = Math.min(1, Math.max(plancher, valeur));
    }, { notify: false });
    peindre(getState());
  }
}

export function gererChange(element) {
  const bind = element.dataset.bind;
  if (bind === "ligne-choix") {
    commit((brouillon) => {
      const devis = brouillon.devis.find((item) => item.id === element.dataset.devis);
      const ligne = devis?.lignes.find((item) => item.id === element.dataset.ligne);
      if (!ligne) return;
      ligne[element.dataset.key] = element.value;
    });
    return;
  }
  if (bind === "methode") {
    commit((brouillon) => {
      const devis = brouillon.devis.find((item) => item.id === element.dataset.devis);
      if (devis) devis.methode = element.value;
    });
    return;
  }
  if (bind === "texte-ligne") {
    commit((brouillon) => {
      const devis = brouillon.devis.find((item) => item.id === element.dataset.devis);
      const ligne = devis?.lignes.find((item) => item.id === element.dataset.ligne);
      if (ligne) ligne[element.dataset.key] = element.value;
    }, { notify: false });
    return;
  }
  if (bind === "ratio") {
    commit((brouillon) => {
      const chantier = brouillon.chantiers.find((item) => item.id === element.dataset.chantier);
      if (!chantier) return;
      chantier[element.dataset.key] = Math.max(0, Number(element.value) || 0) / 100;
    });
    return;
  }
  if (bind === "flag") {
    commit((brouillon) => {
      const chantier = brouillon.chantiers.find((item) => item.id === element.dataset.chantier);
      if (chantier) chantier.autoliquidation = element.checked;
    });
    return;
  }
  if (bind === "statut-chantier") {
    commit((brouillon) => {
      const chantier = brouillon.chantiers.find((item) => item.id === element.dataset.chantier);
      if (chantier) chantier.statut = element.value;
    });
    return;
  }
  if (bind === "pointage") {
    const cellule = element.closest("[data-pointage]");
    const chantierId = cellule.querySelector("[data-role='chantier']").value;
    const heures = Number(cellule.querySelector("[data-role='heures']").value) || 0;
    commit((brouillon) => {
      brouillon.pointages = brouillon.pointages.filter((pointage) => {
        return !(pointage.compagnonId === cellule.dataset.compagnon && pointage.date === cellule.dataset.date);
      });
      if (chantierId && heures > 0) {
        brouillon.pointages.push({
          compagnonId: cellule.dataset.compagnon,
          chantierId,
          date: cellule.dataset.date,
          heures,
        });
      }
    });
  }
}

function figerPrix(situation, state) {
  if (situation.prixFige) return;
  const devis = state.devis.find((item) => item.id === situation.devisId);
  if (!devis) return;
  situation.prixFige = {};
  for (const ligne of devis.lignes) situation.prixFige[ligne.id] = ligneMontants(ligne, devis).pv;
}

function ecrireLigne(ligne, cle, valeur) {
  if (cle === "designation" || cle === "lot" || cle === "unite") {
    ligne[cle] = valeur;
    return;
  }
  const nombre = valeur === "" ? 0 : Number(valeur);
  ligne[cle] = Number.isFinite(nombre) ? Math.max(0, nombre) : 0;
}

function exporterSituations(state) {
  const lignes = ["chantier;numero;type;date;statut;mois_ht;retenue;prorata;net_ht;tva;ttc"];
  for (const situation of state.situations) {
    const detail = detailSituation(state, situation);
    const chantier = detail.chantier?.nom ?? situation.chantierId;
    lignes.push([
      chantier,
      situation.numero,
      situation.type,
      situation.date,
      situation.statut,
      detail.mois,
      detail.retenueAppliquee,
      detail.prorata,
      detail.netHT,
      detail.tva,
      detail.ttc,
    ].join(";"));
  }
  const blob = new Blob([`${lignes.join("\n")}\n`], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const lien = document.createElement("a");
  lien.href = url;
  lien.download = "solive-situations.csv";
  lien.click();
  URL.revokeObjectURL(url);
}
