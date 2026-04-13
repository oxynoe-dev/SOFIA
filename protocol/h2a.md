# H2A — Human-to-Assistant Protocol

> Le protocole de coordination entre l'humain et ses assistants.

---

## Positionnement

H2A formalise la couche de coordination entre un humain (orchestrateur) et des assistants contraints (personas) dans une instance de travail. Il ne remplace ni les guardrails techniques ni les interfaces : il structure la collaboration elle-meme.

| Protocole | Couche | Nature |
|-----------|--------|--------|
| MCP (Anthropic) | Agent ↔ Outils | Technique — wire protocol |
| A2A (Google) | Agent ↔ Agent | Technique — communication |
| **H2A** | **Humain ↔ Assistant** | **Organisationnel — coordination** |

H2A n'est pas un protocole technique — il definit la semantique des interactions, pas leur implementation. Voir `implementation.md` pour les choix d'implementation courants.

## Entites

H2A repose sur 7 entites constitutives. Voir `core/modele.md` pour le detail.

| Entite | Doc protocol/ |
|--------|---------------|
| Instance, Espace, Persona, Orchestrateur | ce document |
| Echange | `exchange.md` |
| Friction | `friction.md` |
| Contribution | `contribution.md` |

## Invariants

1. **Friction constitutive** — la friction n'est pas un defaut a corriger mais un signal structurant. Le protocole DOIT la capturer, la qualifier et la conserver.
2. **Humain arbitre** — l'orchestrateur DOIT trancher les divergences entre personas. Aucun persona ne tranche pour un autre.
3. **Isolation** — un persona NE DOIT PAS interagir en dehors de son espace et de l'espace partage. L'orchestrateur est le seul a traverser les frontieres.
4. **Tracabilite** — tout echange DOIT produire une trace identifiable.

## Distinction protocole / observation

Le protocole distingue deux couches de formalisation :

| Couche | Statut | Verification | Exemples |
|--------|--------|-------------|----------|
| **Protocolaire** | Garanti | Computationnelle (deterministe, automatisable) | Artefacts produits, notes deposees, traces de session |
| **Observationnelle** | Best-effort | Inferentielle (jugement semantique, non-deterministe) | Friction qualifiee, flux epistemique, tags d'apport |

La couche protocolaire definit ce que l'audit peut verifier mecaniquement. La couche observationnelle est remplie par l'assistant et validee par l'humain.

## Audit

### Principe d'auditabilite

> Ce qui est dans le protocole est ce qu'un outil d'audit peut verifier cross-instance sans configuration specifique.

### Points de controle computationnels (DOIT)

| Point | Verification |
|-------|-------------|
| Presence de traces de session | Chaque session a produit une trace identifiable |
| Metadonnees de session | Chaque trace porte : persona, date, identifiant de session |
| Sections protocolaires | Chaque trace contient : Produit, Decisions, Notes deposees, Ouvert |
| Metadonnees d'artefact | Chaque artefact porte : emetteur, destinataire, nature, statut, date |
| Cycle de vie statut | Valeurs dans {nouveau, lu, traite} |
| Isolation | Aucun persona n'a produit en dehors de son espace et de l'espace partage |

### Signaux observationnels (PEUT)

| Signal | Interpretation |
|--------|---------------|
| Absence de friction sur N sessions consecutives | Friction possiblement absente — domestication ? |
| Que des `[juste]` | Persona en mode validation |
| Messages non routes depuis N echanges | Echange bloque |
| Persona sans session depuis N jours | Persona inactif |

Ces signaux ne sont pas des violations du protocole — ce sont des indicateurs a l'attention de l'orchestrateur.

## Terminologie

Les mots-cles "DOIT", "NE DOIT PAS", "DEVRAIT", "NE DEVRAIT PAS", "PEUT" sont a interpreter au sens de la RFC 2119 (MUST, MUST NOT, SHOULD, SHOULD NOT, MAY).

## Filiation theorique

| Reference | Apport a H2A |
|-----------|-------------|
| Sheridan & Verplank (1978) | 10 niveaux d'autonomie — cadre historique HITL |
| Toulmin (1958) | Modele d'argumentation — eclairage des 5 marqueurs |
| Searle (1995) | Regles constitutives vs regulatives — distinction core/protocol/doc |
| Böckeler (2026) | Computationnel vs inferentiel — distinction couche protocolaire/observationnelle |
| Wood, Bruner & Ross (1976) | Scaffolding — collaboration asymetrique |
| Elster (1979) | Precommitment — contrainte productive |

## Specification complete

Voir `doc/h2a-proposal.md` pour le document complet (positionnement, discussion, questions ouvertes).
