import assert from "node:assert/strict";
import test from "node:test";
import {
  detailSituation,
  devisTotaux,
  factureValidee,
  ligneMontants,
  peutCreerDgd,
  resumeChantier,
  resumeEntreprise,
} from "./calc.js";
import { seed } from "./seed.js";

test("le prix de vente au déboursé ignore les frais généraux", () => {
  const montants = ligneMontants(
    { qte: 10, debourseUnitaire: 40, coefficient: 1.5, prixVenteForce: 90 },
    { methode: "debourse", fraisGeneraux: 0.2 },
  );
  assert.equal(montants.ds, 400);
  assert.equal(montants.pv, 600);
  assert.equal(montants.marge, 200 / 600);
});

test("le prix de revient applique les frais généraux puis le coefficient", () => {
  const montants = ligneMontants(
    { qte: 10, debourseUnitaire: 40, coefficient: 1.25 },
    { methode: "revient", fraisGeneraux: 0.1 },
  );
  assert.equal(montants.pr, 440);
  assert.equal(montants.pv, 550);
});

test("la méthode prix de vente utilise le prix forcé", () => {
  const montants = ligneMontants(
    { qte: 2, debourseUnitaire: 40, coefficient: 3, prixVenteForce: 70 },
    { methode: "vente", fraisGeneraux: 0 },
  );
  assert.equal(montants.pv, 140);
  assert.equal(montants.marge, (140 - 80) / 140);
});

test("une situation déduit la précédente, la retenue, le prorata et la TVA", () => {
  const state = {
    compagnons: [],
    pointages: [],
    achats: [],
    historique: {},
    chantiers: [
      {
        id: "ch",
        retenueGarantie: 0.05,
        compteProrata: 0.02,
        autoliquidation: false,
        tva: 0.1,
      },
    ],
    devis: [
      {
        id: "dv",
        chantierId: "ch",
        methode: "debourse",
        fraisGeneraux: 0,
        lignes: [{ id: "l1", qte: 1, debourseUnitaire: 100, coefficient: 2, nature: "materiaux", unite: "u" }],
      },
    ],
    situations: [
      { id: "s1", chantierId: "ch", devisId: "dv", numero: 1, statut: "envoyee", avancement: { l1: 0.5 } },
      { id: "s2", chantierId: "ch", devisId: "dv", numero: 2, statut: "envoyee", avancement: { l1: 1 } },
    ],
  };
  const detail = detailSituation(state, state.situations[1]);
  assert.equal(detail.precedent, 100);
  assert.equal(detail.mois, 100);
  assert.equal(detail.retenue, 5);
  assert.equal(detail.prorata, 2);
  assert.equal(detail.netHT, 93);
  assert.equal(detail.tva, 9.3);
  assert.equal(detail.ttc, 102.3);
});

test("l'autoliquidation annule la TVA", () => {
  const state = {
    chantiers: [{ id: "ch", retenueGarantie: 0, compteProrata: 0, autoliquidation: true, tva: 0.2 }],
    devis: [
      {
        id: "dv",
        methode: "debourse",
        fraisGeneraux: 0,
        lignes: [{ id: "l1", qte: 1, debourseUnitaire: 50, coefficient: 2, nature: "mo", unite: "h" }],
      },
    ],
    situations: [
      { id: "s1", chantierId: "ch", devisId: "dv", numero: 1, statut: "validee", avancement: { l1: 1 } },
    ],
  };
  const detail = detailSituation(state, state.situations[0]);
  assert.equal(detail.tva, 0);
  assert.equal(detail.ttc, detail.netHT);
});

test("le DGD libère les retenues déjà constituées", () => {
  const state = {
    chantiers: [{ id: "ch", retenueGarantie: 0.05, compteProrata: 0, autoliquidation: true, tva: 0.2 }],
    devis: [
      {
        id: "dv",
        methode: "debourse",
        fraisGeneraux: 0,
        lignes: [{ id: "l1", qte: 1, debourseUnitaire: 100, coefficient: 1, nature: "mo", unite: "h" }],
      },
    ],
    situations: [
      { id: "s1", chantierId: "ch", devisId: "dv", numero: 1, statut: "envoyee", libereRetenue: false, avancement: { l1: 1 } },
      { id: "s2", chantierId: "ch", devisId: "dv", numero: 2, statut: "validee", type: "dgd", libereRetenue: true, avancement: { l1: 1 } },
    ],
  };
  const detail = detailSituation(state, state.situations[1]);
  assert.equal(detail.mois, 0);
  assert.equal(detail.liberation, 5);
  assert.equal(detail.netHT, 5);
});

test("la démo signale la Halle quand la marge réelle décroche", () => {
  const halle = resumeChantier(seed, "ch-halle");
  const ecole = resumeChantier(seed, "ch-ecole");
  assert.ok(halle.totaux.pv > halle.totaux.ds);
  assert.equal(halle.attentionMarge, true);
  assert.equal(ecole.attentionMarge, false);
  assert.ok(factureValidee(seed, "ch-halle") < halle.totaux.pv);
  assert.equal(peutCreerDgd(seed, "ch-halle").ok, false);
  assert.equal(peutCreerDgd(seed, "ch-ecole").ok, true);
  const entreprise = resumeEntreprise(seed);
  assert.equal(entreprise.actifs.length, 3);
  assert.ok(entreprise.facture > 0);
  assert.ok(entreprise.depense > 0);
});

test("un prix figé ne bouge plus quand le devis change", () => {
  const state = structuredClone(seed);
  const envoyee = state.situations.find((situation) => situation.id === "sit-halle-1");
  const brouillon = state.situations.find((situation) => situation.id === "sit-halle-3");
  const avant = detailSituation(state, envoyee).mois;
  const brouillonAvant = detailSituation(state, brouillon).mois;
  const devis = state.devis.find((item) => item.id === "dv-halle");
  for (const ligne of devis.lignes) ligne.coefficient = 2;
  assert.equal(detailSituation(state, envoyee).mois, avant);
  assert.notEqual(detailSituation(state, brouillon).mois, brouillonAvant);
});

test("les totaux de devis comptent les heures de main-d'œuvre", () => {
  const totaux = devisTotaux(seed.devis[0]);
  assert.equal(totaux.heures, 520);
  assert.ok(totaux.marge > 0.15 && totaux.marge < 0.35);
});
