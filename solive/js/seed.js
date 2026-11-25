import { ligneMontants } from "./calc.js";

export const seed = {
  entreprise: {
    nom: "Atelier des Cimes",
    metier: "Couverture, charpente et étanchéité",
    ville: "Lyon",
  },
  semaine: "2026-11-23",
  compagnons: [
    { id: "cp-nina", nom: "Nina Pellier", metier: "Couvreuse", taux: 39 },
    { id: "cp-malik", nom: "Malik Ferhat", metier: "Couvreur", taux: 37 },
    { id: "cp-ines", nom: "Inès Talbot", metier: "Charpentière", taux: 36 },
    { id: "cp-hugo", nom: "Hugo Sanz", metier: "Étancheur", taux: 35 },
    { id: "cp-claire", nom: "Claire Monin", metier: "Apprentie", taux: 22 },
    { id: "cp-yanis", nom: "Yanis Khelf", metier: "Zingueur", taux: 38 },
  ],
  bibliotheque: [
    { designation: "Compagnon couvreur", unite: "h", nature: "mo", debourseUnitaire: 38 },
    { designation: "Compagnon charpentier", unite: "h", nature: "mo", debourseUnitaire: 36 },
    { designation: "Compagnon étancheur", unite: "h", nature: "mo", debourseUnitaire: 35 },
    { designation: "Tuile terre cuite", unite: "m²", nature: "materiaux", debourseUnitaire: 48 },
    { designation: "Écran sous-toiture", unite: "m²", nature: "materiaux", debourseUnitaire: 9 },
    { designation: "Liteaux et contre-liteaux", unite: "m²", nature: "materiaux", debourseUnitaire: 11 },
    { designation: "Étanchéité bicouche", unite: "m²", nature: "materiaux", debourseUnitaire: 27 },
    { designation: "Isolant toiture 140 mm", unite: "m²", nature: "materiaux", debourseUnitaire: 22 },
    { designation: "Zinguerie façonnée", unite: "ml", nature: "materiaux", debourseUnitaire: 34 },
    { designation: "Sous-traitance échafaudage", unite: "forfait", nature: "sous_traitance", debourseUnitaire: 4200 },
    { designation: "Sous-traitance zinguerie", unite: "forfait", nature: "sous_traitance", debourseUnitaire: 16000 },
    { designation: "Évacuation des gravats", unite: "forfait", nature: "sous_traitance", debourseUnitaire: 1800 },
  ],
  chantiers: [
    {
      id: "ch-halle",
      nom: "Halle des Tisserands",
      client: "SCI Les Berges",
      ville: "Villeurbanne",
      statut: "en_cours",
      debut: "2026-03-02",
      fin: "2026-11-28",
      retenueGarantie: 0.05,
      compteProrata: 0.015,
      autoliquidation: false,
      tva: 0.1,
    },
    {
      id: "ch-ecole",
      nom: "École Anatole France",
      client: "Mairie de Caluire",
      ville: "Caluire-et-Cuire",
      statut: "en_cours",
      debut: "2026-05-04",
      fin: "2026-12-18",
      retenueGarantie: 0.05,
      compteProrata: 0,
      autoliquidation: true,
      tva: 0.2,
      },
    {
      id: "ch-berges",
      nom: "Immeuble Berges du Rhône",
      client: "Habitat Rhône",
      ville: "Lyon 6e",
      statut: "en_cours",
      debut: "2026-06-15",
      fin: "2027-02-27",
      retenueGarantie: 0.05,
      compteProrata: 0.02,
      autoliquidation: false,
      tva: 0.2,
    },
    {
      id: "ch-charvet",
      nom: "Maison Charvet",
      client: "Famille Charvet",
      ville: "Sainte-Foy-lès-Lyon",
      statut: "etude",
      debut: "2027-03-01",
      fin: "2027-06-30",
      retenueGarantie: 0.05,
      compteProrata: 0,
      autoliquidation: false,
      tva: 0.1,
    },
  ],
  devis: [
    {
      id: "dv-halle",
      chantierId: "ch-halle",
      numero: "D-2026-014",
      statut: "signe",
      methode: "debourse",
      fraisGeneraux: 0.08,
      lignes: [
        ligne("h-mo", "Couverture", "Compagnon couvreur", "h", 400, "mo", 38, 1.32),
        ligne("h-tuile", "Couverture", "Tuile terre cuite", "m²", 500, "materiaux", 48, 1.3),
        ligne("h-ecran", "Couverture", "Écran sous-toiture", "m²", 500, "materiaux", 9, 1.28),
        ligne("h-zinc", "Zinguerie", "Sous-traitance zinguerie", "forfait", 1, "sous_traitance", 16000, 1.22),
        ligne("h-charp", "Charpente", "Compagnon charpentier", "h", 120, "mo", 36, 1.34),
      ],
    },
    {
      id: "dv-ecole",
      chantierId: "ch-ecole",
      numero: "D-2026-021",
      statut: "signe",
      methode: "debourse",
      fraisGeneraux: 0.1,
      lignes: [
        ligne("e-mo", "Étanchéité", "Compagnon étancheur", "h", 280, "mo", 35, 1.38),
        ligne("e-bi", "Étanchéité", "Étanchéité bicouche", "m²", 640, "materiaux", 27, 1.36),
        ligne("e-iso", "Étanchéité", "Isolant toiture 140 mm", "m²", 640, "materiaux", 22, 1.33),
        ligne("e-echaf", "Installation", "Sous-traitance échafaudage", "forfait", 1, "sous_traitance", 4200, 1.2),
      ],
    },
    {
      id: "dv-berges",
      chantierId: "ch-berges",
      numero: "D-2026-027",
      statut: "signe",
      methode: "revient",
      fraisGeneraux: 0.12,
      lignes: [
        ligne("b-mo", "Charpente", "Compagnon charpentier", "h", 220, "mo", 36, 1.25),
        ligne("b-liteau", "Couverture", "Liteaux et contre-liteaux", "m²", 380, "materiaux", 11, 1.22),
        ligne("b-tuile", "Couverture", "Tuile terre cuite", "m²", 380, "materiaux", 48, 1.18),
        ligne("b-zinc", "Zinguerie", "Zinguerie façonnée", "ml", 90, "materiaux", 34, 1.3),
      ],
    },
    {
      id: "dv-charvet",
      chantierId: "ch-charvet",
      numero: "D-2026-033",
      statut: "brouillon",
      methode: "debourse",
      fraisGeneraux: 0.08,
      lignes: [
        ligne("c-mo", "Couverture", "Compagnon couvreur", "h", 90, "mo", 38, 1.4),
        ligne("c-tuile", "Couverture", "Tuile terre cuite", "m²", 120, "materiaux", 48, 1.35),
        ligne("c-grav", "Dépose", "Évacuation des gravats", "forfait", 1, "sous_traitance", 1800, 1.25),
      ],
    },
  ],
  situations: [
    situation("sit-halle-1", "ch-halle", "dv-halle", 1, "2026-06-30", "envoyee", {
      "h-mo": 0.45,
      "h-tuile": 0.4,
      "h-ecran": 0.4,
      "h-zinc": 0.25,
      "h-charp": 0.6,
    }),
    situation("sit-halle-2", "ch-halle", "dv-halle", 2, "2026-09-30", "envoyee", {
      "h-mo": 0.78,
      "h-tuile": 0.72,
      "h-ecran": 0.72,
      "h-zinc": 0.6,
      "h-charp": 0.9,
    }),
    situation("sit-halle-3", "ch-halle", "dv-halle", 3, "2026-11-25", "brouillon", {
      "h-mo": 0.9,
      "h-tuile": 0.84,
      "h-ecran": 0.84,
      "h-zinc": 0.75,
      "h-charp": 1,
    }),
    situation("sit-ecole-1", "ch-ecole", "dv-ecole", 1, "2026-07-31", "envoyee", {
      "e-mo": 0.5,
      "e-bi": 0.45,
      "e-iso": 0.45,
      "e-echaf": 1,
    }),
    situation("sit-ecole-2", "ch-ecole", "dv-ecole", 2, "2026-10-31", "envoyee", {
      "e-mo": 0.8,
      "e-bi": 0.76,
      "e-iso": 0.7,
      "e-echaf": 1,
    }),
    situation("sit-berges-1", "ch-berges", "dv-berges", 1, "2026-10-31", "envoyee", {
      "b-mo": 0.42,
      "b-liteau": 0.55,
      "b-tuile": 0.3,
      "b-zinc": 0.2,
    }),
  ],
  achats: [
    achat("ach-1", "ch-halle", "Négoce du Plateau", "Tuiles et écran, livraison 2", "materiaux", 21400, "2026-05-12", "payee"),
    achat("ach-2", "ch-halle", "Atelier Zinc Loire", "Acompte zinguerie", "sous_traitance", 9600, "2026-08-03", "payee"),
    achat("ach-3", "ch-halle", "Négoce du Plateau", "Complément tuiles", "materiaux", 6800, "2026-10-09", "a_payer"),
    achat("ach-4", "ch-ecole", "Étanchéité Rhône", "Bicouche et isolant", "materiaux", 18600, "2026-06-20", "payee"),
    achat("ach-5", "ch-ecole", "Échafaudages Caluire", "Montage et location", "sous_traitance", 4200, "2026-05-18", "payee"),
    achat("ach-6", "ch-berges", "Scierie des Monts", "Liteaux et voliges", "materiaux", 3900, "2026-09-02", "payee"),
    achat("ach-7", "ch-berges", "Négoce du Plateau", "Première tranche de tuiles", "materiaux", 7200, "2026-10-14", "a_payer"),
  ],
  historique: {
    "ch-halle": { heures: 620, cout: 23560 },
    "ch-ecole": { heures: 210, cout: 7350 },
    "ch-berges": { heures: 96, cout: 3456 },
    "ch-charvet": { heures: 0, cout: 0 },
  },
  pointages: [
    { compagnonId: "cp-nina", chantierId: "ch-halle", date: "2026-11-23", heures: 8 },
    { compagnonId: "cp-nina", chantierId: "ch-halle", date: "2026-11-24", heures: 8 },
    { compagnonId: "cp-nina", chantierId: "ch-halle", date: "2026-11-25", heures: 7 },
    { compagnonId: "cp-malik", chantierId: "ch-halle", date: "2026-11-23", heures: 8 },
    { compagnonId: "cp-malik", chantierId: "ch-halle", date: "2026-11-24", heures: 8 },
    { compagnonId: "cp-ines", chantierId: "ch-berges", date: "2026-11-23", heures: 8 },
    { compagnonId: "cp-ines", chantierId: "ch-berges", date: "2026-11-24", heures: 8 },
    { compagnonId: "cp-ines", chantierId: "ch-berges", date: "2026-11-25", heures: 8 },
    { compagnonId: "cp-hugo", chantierId: "ch-ecole", date: "2026-11-24", heures: 7 },
    { compagnonId: "cp-hugo", chantierId: "ch-ecole", date: "2026-11-25", heures: 7 },
    { compagnonId: "cp-yanis", chantierId: "ch-halle", date: "2026-11-25", heures: 8 },
    { compagnonId: "cp-claire", chantierId: "ch-ecole", date: "2026-11-23", heures: 7 },
  ],
};

function ligne(id, lot, designation, unite, qte, nature, debourseUnitaire, coefficient) {
  return { id, lot, designation, unite, qte, nature, debourseUnitaire, coefficient, prixVenteForce: null };
}

function situation(id, chantierId, devisId, numero, date, statut, avancement) {
  return { id, chantierId, devisId, numero, date, statut, type: "situation", libereRetenue: false, avancement };
}

function achat(id, chantierId, fournisseur, designation, typologie, montantHT, date, statut) {
  return { id, chantierId, fournisseur, designation, typologie, montantHT, date, statut };
}

for (const situationCourante of seed.situations) {
  if (situationCourante.statut === "brouillon") continue;
  const devis = seed.devis.find((item) => item.id === situationCourante.devisId);
  situationCourante.prixFige = Object.fromEntries(
    devis.lignes.map((ligne) => [ligne.id, ligneMontants(ligne, devis).pv]),
  );
}
