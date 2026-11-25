export function ligneMontants(ligne, devis) {
  const quantite = nombrePositif(ligne.qte);
  const debourseUnitaire = nombrePositif(ligne.debourseUnitaire);
  const coefficient = nombrePositif(ligne.coefficient) || 1;
  const ds = arrondir(quantite * debourseUnitaire);
  const pr = arrondir(ds * (1 + nombrePositif(devis.fraisGeneraux)));
  let pv;
  if (devis.methode === "vente" && ligne.prixVenteForce != null && ligne.prixVenteForce !== "") {
    pv = arrondir(quantite * nombrePositif(ligne.prixVenteForce));
  } else if (devis.methode === "revient") {
    pv = arrondir(pr * coefficient);
  } else {
    pv = arrondir(ds * coefficient);
  }
  const marge = pv > 0 ? (pv - ds) / pv : 0;
  return { ds, pr, pv, marge };
}

export function devisTotaux(devis) {
  const vide = { ds: 0, pr: 0, pv: 0, marge: 0, heures: 0, mo: 0, materiaux: 0, sousTraitance: 0 };
  if (!devis) return vide;
  const totaux = devis.lignes.reduce((acc, ligne) => {
    const montants = ligneMontants(ligne, devis);
    acc.ds += montants.ds;
    acc.pr += montants.pr;
    acc.pv += montants.pv;
    if (ligne.nature === "mo") acc.mo += montants.ds;
    if (ligne.nature === "materiaux") acc.materiaux += montants.ds;
    if (ligne.nature === "sous_traitance") acc.sousTraitance += montants.ds;
    if (ligne.nature === "mo" && String(ligne.unite).toLowerCase() === "h") {
      acc.heures += nombrePositif(ligne.qte);
    }
    return acc;
  }, { ...vide });
  totaux.ds = arrondir(totaux.ds);
  totaux.pr = arrondir(totaux.pr);
  totaux.pv = arrondir(totaux.pv);
  totaux.mo = arrondir(totaux.mo);
  totaux.materiaux = arrondir(totaux.materiaux);
  totaux.sousTraitance = arrondir(totaux.sousTraitance);
  totaux.marge = totaux.pv > 0 ? (totaux.pv - totaux.ds) / totaux.pv : 0;
  return totaux;
}

export function devisPrincipal(state, chantierId) {
  const liste = state.devis.filter((devis) => devis.chantierId === chantierId);
  return liste.find((devis) => devis.statut === "signe") ?? liste[0] ?? null;
}

export function moReelle(state, chantierId) {
  const historique = state.historique?.[chantierId] ?? { heures: 0, cout: 0 };
  let heures = nombrePositif(historique.heures);
  let cout = nombrePositif(historique.cout);
  for (const pointage of state.pointages ?? []) {
    if (pointage.chantierId !== chantierId) continue;
    const compagnon = state.compagnons.find((item) => item.id === pointage.compagnonId);
    const heuresJour = nombrePositif(pointage.heures);
    heures += heuresJour;
    cout += heuresJour * nombrePositif(compagnon?.taux);
  }
  return { heures: arrondir(heures), cout: arrondir(cout) };
}

export function achatsChantier(state, chantierId) {
  const rows = (state.achats ?? []).filter((achat) => achat.chantierId === chantierId);
  let materiaux = 0;
  let sousTraitance = 0;
  for (const achat of rows) {
    const montant = nombrePositif(achat.montantHT);
    if (achat.typologie === "sous_traitance") sousTraitance += montant;
    else materiaux += montant;
  }
  return {
    rows,
    materiaux: arrondir(materiaux),
    sousTraitance: arrondir(sousTraitance),
    total: arrondir(materiaux + sousTraitance),
  };
}

export function depense(state, chantierId) {
  const mo = moReelle(state, chantierId);
  const achats = achatsChantier(state, chantierId);
  return {
    mo: mo.cout,
    heures: mo.heures,
    materiaux: achats.materiaux,
    sousTraitance: achats.sousTraitance,
    total: arrondir(mo.cout + achats.total),
  };
}

export function situationsChantier(state, chantierId) {
  return (state.situations ?? [])
    .filter((situation) => situation.chantierId === chantierId)
    .slice()
    .sort((a, b) => a.numero - b.numero);
}

export function cumulSituation(devis, situation) {
  if (!devis) return { lignes: [], cumul: 0 };
  let cumul = 0;
  const lignes = devis.lignes.map((ligne) => {
    const avancement = borner(situation.avancement?.[ligne.id] ?? 0);
    const montants = ligneMontants(ligne, devis);
    const pv = situation.prixFige?.[ligne.id] ?? montants.pv;
    const montant = arrondir(pv * avancement);
    cumul = arrondir(cumul + montant);
    return { ligne, avancement, ...montants, pv, montant };
  });
  return { lignes, cumul };
}

export function detailSituation(state, situation) {
  const devis = state.devis.find((item) => item.id === situation.devisId) ?? null;
  const chantier = state.chantiers.find((item) => item.id === situation.chantierId) ?? null;
  const toutes = situationsChantier(state, situation.chantierId);
  const index = toutes.findIndex((item) => item.id === situation.id);
  const precedent = index > 0 ? cumulSituation(devis, toutes[index - 1]).cumul : 0;
  const { lignes, cumul } = cumulSituation(devis, situation);
  const mois = arrondir(cumul - precedent);
  const tauxRetenue = nombrePositif(chantier?.retenueGarantie);
  const tauxProrata = nombrePositif(chantier?.compteProrata);
  const retenue = arrondir(mois * tauxRetenue);
  const prorata = arrondir(mois * tauxProrata);
  let retenuesAvant = 0;
  for (let i = 0; i < index; i += 1) {
    const cumulLigne = cumulSituation(devis, toutes[i]).cumul;
    const cumulPrecedent = i > 0 ? cumulSituation(devis, toutes[i - 1]).cumul : 0;
    retenuesAvant = arrondir(retenuesAvant + (cumulLigne - cumulPrecedent) * tauxRetenue);
  }
  const retenueAppliquee = situation.libereRetenue ? 0 : retenue;
  const liberation = situation.libereRetenue ? retenuesAvant : 0;
  const netHT = arrondir(mois - retenueAppliquee - prorata + liberation);
  const tauxTva = chantier?.autoliquidation ? 0 : nombrePositif(chantier?.tva);
  const tva = arrondir(netHT * tauxTva);
  return {
    devis,
    chantier,
    lignes,
    cumul,
    precedent,
    mois,
    retenue,
    prorata,
    retenuesAvant,
    retenueAppliquee,
    liberation,
    netHT,
    tva,
    ttc: arrondir(netHT + tva),
    autoliquidation: Boolean(chantier?.autoliquidation),
  };
}

export function factureValidee(state, chantierId) {
  return situationsChantier(state, chantierId)
    .filter((situation) => situation.statut !== "brouillon")
    .reduce((total, situation) => arrondir(total + detailSituation(state, situation).mois), 0);
}

export function resumeChantier(state, chantierId) {
  const chantier = state.chantiers.find((item) => item.id === chantierId);
  const devis = devisPrincipal(state, chantierId);
  const totaux = devisTotaux(devis);
  const cout = depense(state, chantierId);
  const facture = factureValidee(state, chantierId);
  const margeReelle = facture > 0 ? (facture - cout.total) / facture : null;
  const ecartMarge = margeReelle == null ? null : totaux.marge - margeReelle;
  const depassementHeures = totaux.heures > 0 && cout.heures > totaux.heures * 1.1;
  return {
    chantier,
    devis,
    totaux,
    dep: cout,
    facture,
    resteFacturer: arrondir(totaux.pv - facture),
    resteDepenser: arrondir(totaux.ds - cout.total),
    margeReelle,
    ecartMarge,
    attentionMarge: ecartMarge != null && ecartMarge > 0.03,
    depassementHeures,
  };
}

export function resumeEntreprise(state) {
  const rows = state.chantiers.map((chantier) => resumeChantier(state, chantier.id));
  const actifs = rows.filter((row) => row.chantier.statut !== "etude");
  const facture = arrondir(somme(actifs, (row) => row.facture));
  const depenseTotale = arrondir(somme(actifs, (row) => row.dep.total));
  return {
    rows,
    actifs,
    facture,
    depense: depenseTotale,
    resteFacturer: arrondir(somme(actifs, (row) => row.resteFacturer)),
    resteDepenser: arrondir(somme(actifs, (row) => row.resteDepenser)),
    pv: arrondir(somme(actifs, (row) => row.totaux.pv)),
    ecart: arrondir(facture - depenseTotale),
    margeReelle: facture > 0 ? (facture - depenseTotale) / facture : null,
  };
}

export function peutCreerDgd(state, chantierId) {
  const devis = devisPrincipal(state, chantierId);
  const situations = situationsChantier(state, chantierId);
  if (!devis || devis.statut !== "signe" || devis.lignes.length === 0) {
    return { ok: false, raison: "Un devis signé est nécessaire." };
  }
  if (situations.some((situation) => situation.type === "dgd")) {
    return { ok: false, raison: "Le décompte général et définitif est déjà établi." };
  }
  if (situations.some((situation) => situation.statut === "brouillon")) {
    return { ok: false, raison: "Validez la situation en brouillon avant le DGD." };
  }
  return { ok: true, devis, situations };
}

export function avancementPrecedent(state, situation, ligneId) {
  const toutes = situationsChantier(state, situation.chantierId);
  const index = toutes.findIndex((item) => item.id === situation.id);
  if (index <= 0) return 0;
  return borner(toutes[index - 1].avancement?.[ligneId] ?? 0);
}

function somme(liste, lire) {
  return liste.reduce((total, item) => total + lire(item), 0);
}

function arrondir(valeur) {
  return Math.round((valeur + Number.EPSILON) * 100) / 100;
}

function nombrePositif(valeur) {
  const nombreLu = Number(valeur);
  if (!Number.isFinite(nombreLu) || nombreLu < 0) return 0;
  return nombreLu;
}

function borner(valeur) {
  return Math.min(1, Math.max(0, nombrePositif(valeur)));
}
