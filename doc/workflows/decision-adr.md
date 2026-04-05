## Decision ADR

![Workflow — Decision ADR](../figures/fig-workflow-decision-adr.svg)

Workflow de decision structurelle : de la tension identifiee a la trace dans l'index.

---

### Quand l'utiliser

Quand une tension structurelle est identifiee — un choix technique, un changement d'architecture, un arbitrage entre deux approches incompatibles. N'importe quel persona peut initier le processus.

### Etapes

1. **Tension identifiee** — un persona constate un probleme, une incoherence ou un choix a faire. Il formule la tension en une phrase
2. **Note deposee dans shared/** — le persona depose une note (cf. `core/artefacts.md`) decrivant le contexte, les options identifiees et sa recommandation
3. **Review multi-personas** — chaque persona concerne produit une review sur son axe : archi (coherence), dev (faisabilite), recherche (rigueur), UX (impact utilisateur), strategie (positionnement)
4. **Redaction ADR** — l'architecte redige l'ADR au statut **Proposed** : contexte, decision, consequences, alternatives rejetees
5. **Arbitrage PO** — le PO passe l'ADR a **Accepted** ou **Rejected**. La decision est tracee avec son contexte
6. **Trace dans l'index** — l'ADR est ajoute a l'index avec statut, resume et date

### Roles impliques

| Persona | Role |
|---------|------|
| N'importe quel persona | Identifie la tension, depose la note |
| Personas concernes | Review sur leur axe |
| Architecte | Redige l'ADR (Proposed) |
| PO | Arbitre (Accepted / Rejected) |

### Artefacts produits

- Note initiale (dans `shared/notes/`)
- Reviews par axe (dans `shared/review/`)
- ADR au format standard : Contexte, Decision, Consequences, Status
- Entree dans l'index ADR

### Pieges

- **Coder sur un ADR Proposed** — un ADR Proposed n'est pas une autorisation. Seul le statut Accepted autorise l'implementation. Coder avant l'arbitrage PO, c'est investir du temps sur une decision qui peut etre rejetee
- **ADR sans alternatives** — un ADR qui ne liste pas les alternatives rejetees n'est pas un ADR, c'est une annonce. Le contexte des alternatives est ce qui rend la decision comprehensible dans 6 mois
- **Confondre tension et preference** — une tension est un probleme objectif (incoherence, blocage, choix incompatible). Une preference est subjective. Les ADR traitent des tensions, pas des preferences
