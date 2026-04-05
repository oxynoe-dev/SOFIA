## Inspector

L'humain intercepte et vérifie avant de transmettre. Pas un persona — une responsabilité.

### Structure

Le pattern est complémentaire au Challenger. Le Challenger opère après la production (peer review). L'Inspector opère pendant la circulation — il intercepte les artefacts entre personas, vérifie, corrige si nécessaire, puis transmet.

Dans Voix, l'Inspector c'est l'humain. C'est implicite dans le rôle du PO : il lit tout, filtre, contextualise, corrige avant de transmettre. Trois fonctions cumulées sur une personne : orchestrateur, arbitre, inspecteur.

C'est le mécanisme le plus coûteux en attention — et le premier à lâcher quand la fatigue s'installe.

### Quand le reconnaître

- L'humain transmet un artefact d'un persona à un autre sans l'avoir relu → l'inspection est absente.
- Une erreur factuelle se propage entre 3+ documents sans être détectée → la chaîne d'inspection est rompue.
- L'humain approuve des sessions sans lire les résumés → le rôle d'inspecteur est abandonné.

### Ce que l'inspecteur vérifie

| Moment | Vérification |
|--------|-------------|
| Avant transmission | L'artefact dit-il ce que le producteur pense qu'il dit ? |
| Avant transmission | Le contexte est-il suffisant pour le destinataire ? |
| Après réception | La réponse traite-t-elle la question posée ? |
| En continu | Les faits (dates, chiffres, références) sont-ils corrects ? |

### Relation avec le Challenger

Le Challenger et l'Inspector couvrent deux moments différents :

- **Challenger** → après production, entre pairs. Horizontal.
- **Inspector** → pendant circulation, par l'humain. Vertical.

Combinés, ils récupèrent la grande majorité des erreurs. Séparément, chacun laisse passer ce que l'autre attraperait. L'Inspector attrape les erreurs factuelles que les personas ne peuvent pas vérifier (ils n'ont pas de mémoire fiable). Le Challenger attrape les erreurs de fond que l'humain peut manquer par fatigue.

### Risques

- **Surcharge** : l'humain cumule orchestration + arbitrage + inspection. C'est le facteur principal de décrochage (devoir n°6 : maintenir l'attention).
- **Faux sentiment de sécurité** : l'inspection existe dans le processus mais n'est pas exécutée — l'humain scanne au lieu de lire.
- **Pas de relève** : si l'humain décroche, personne ne prend le relais. Les personas continuent à produire avec la même assurance.

### Mitigation

- Réduire la surface d'inspection : moins de personas actifs en parallèle = moins d'artefacts à inspecter.
- Expliciter les moments d'inspection dans le protocole de session (devoir n°3 : relire ce qui sort).
- Tracer les inspections manquées : quand un artefact est transmis sans relecture, le noter. La trace rend le manque visible.

### Référence

Huang, J.-T. et al. (2025). "On the Resilience of LLM-Based Multi-Agent Collaboration with Faulty Agents." *ICML 2025*. https://arxiv.org/abs/2408.00989
