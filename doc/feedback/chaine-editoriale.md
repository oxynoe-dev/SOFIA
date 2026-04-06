# Retour d'expérience — Chaîne éditoriale

> La chaîne éditoriale multi-personas émerge naturellement. Il faut la documenter avant qu'elle ne se casse.

---

## Le pattern

Observé sur la production du livre bleu Voix. Reproductible pour tout
livrable éditorial : article, fragment, documentation publique.

```
Équipe réfléchit
  → fragments, échanges, frictions inter-personas
  → la matière brute s'accumule

Rédacteur rédige
  → distille les échanges en texte structuré
  → échange avec les experts pour calibrer le fond

Experts valident le fond
  → architecte : structure, cohérence argumentaire
  → chercheur : références, rigueur factuelle
  → stratège : positionnement, ton

Producteur met en forme
  → mise en page, déclinaison multi-support (PDF, web, réseaux)

Challenger vérifie l'output
  → UX, accessibilité, cohérence

PO valide avant sortie
  → en particulier la contextualisation des références académiques
```

## Ce qu'on a appris

- Le rédacteur ne publie pas seul. Il rédige, les experts valident le fond,
  le producteur livre la forme, le stratège décide du timing.
- Chaque persona a un rôle clair dans la chaîne :
  contenu → validation → production → diffusion.
- L'humain orchestre les transitions entre chaque étape.
- **Le PO est le dernier verrou** — une référence correcte peut être mal
  contextualisée et changer la thèse. Seul l'humain vérifie ça.

## Règle clé

Rien ne sort sans relecture et validation du PO avant publication.
Le rédacteur formule, le chercheur source, le PO valide que l'usage de
la référence est juste.

## Pour ton projet

Si ton équipe Voix produit du contenu public (articles, documentation,
présentations) :
- Identifie qui rédige, qui valide le fond, qui produit la forme,
  qui challenge, qui décide du timing
- Documente cette chaîne — elle émergera naturellement, mais sans
  documentation elle se cassera au premier changement de persona
- Le PO valide toujours en dernier, surtout sur les données factuelles
  et les références
