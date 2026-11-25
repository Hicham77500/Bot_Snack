# Solive

Démonstration d'un suivi de marge chantier pour une PME du bâtiment. L'entreprise, les clients et les montants sont fictifs.

Solive relie quatre mouvements :

- le devis, chiffré en déboursé sec, en prix de revient ou en prix de vente ;
- les situations d'avancement, avec retenue de garantie, compte prorata, TVA ou autoliquidation, et décompte général définitif ;
- les factures d'achat, rattachées au chantier ;
- les heures des compagnons, valorisées à leur taux.

Le tableau de bord compare le facturé au dépensé et signale un chantier lorsque la marge réelle passe de plus de 3 points sous la marge du devis.

## Lancer

Ouvrir `index.html` dans un navigateur, ou servir le dossier :

```bash
python3 -m http.server 4173
```

Puis aller sur `http://127.0.0.1:4173`. Les modifications restent dans le navigateur. Le bouton « Revenir à la démo » recharge le jeu de données initial.

## Vérifier les calculs

```bash
npm test
```
