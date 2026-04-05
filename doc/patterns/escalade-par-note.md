## Escalade par note

![Pattern — Escalade par note](../figures/fig-pattern-escalade-note.svg)

Quand un persona rencontre un probleme hors de son perimetre, il depose une note. Le PO route.

### Structure

1. Un persona identifie un probleme qui ne releve pas de son axe.
2. Il redige une note factuelle dans `shared/notes/` avec le format `note-{destinataire}-{sujet}-{auteur}.md`.
3. Il ne tente pas de resoudre le probleme lui-meme.
4. Le PO lit la note, ajoute le contexte necessaire, et la transmet au persona competent.
5. Le destinataire traite et repond via le meme mecanisme si besoin.

Il n'y a pas de communication directe inter-personas. Le PO est le seul routeur. Cela preserve l'isolation des contextes et evite les boucles de coordination non supervisees.

### Quand le reconnaitre

- Un persona bute sur une question qui sort de son perimetre.
- Deux personas auraient besoin de se coordonner sur un sujet transverse.
- Un probleme detecte dans un workspace concerne un autre workspace.

### Exemple

Axel identifie une incoherence dans la spec CVM pendant l'implementation. Il depose `note-mira-incoherence-spec-cvm-axel.md` dans `shared/notes/`. Le PO lit, confirme le contexte, et ouvre une session avec Mira pour traiter le point. Mira corrige la spec ou justifie le choix existant.

### Variantes

- **Note informative** : pas de probleme a resoudre, juste un signal (ex. "j'ai observe que..."). Le PO decide s'il y a suite.
- **Note urgente** : le persona signale un bloquant dans le titre. Le PO priorise.

### Risques

- **Engorgement PO** : trop de notes non traitees s'accumulent. Le PO doit trier regulierement.
- **Sur-formalisme** : deposer une note pour un detail trivial que le persona pourrait ignorer.
- **Perte de contexte** : la note est trop courte et le PO ne peut pas router correctement.
