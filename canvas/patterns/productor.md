## Productor

Le pattern de base. Un persona produit dans son perimetre, l'orchestrateur recoit.

### Structure

1. L'orchestrateur ouvre une session avec le persona
2. Il donne une directive ou un contexte
3. Le persona produit dans son espace
4. L'orchestrateur recoit le resultat

### Quand l'utiliser

Quand un persona doit produire un artefact (spec, code, analyse, redaction) sans qu'un challenge inter-personas soit necessaire. C'est le mode par defaut d'une session.

### Limites

Le productor seul n'a pas de friction — le persona execute, l'orchestrateur recoit. Si toutes les sessions sont en mode productor, la methode perd son mecanisme central. Le productor se combine generalement avec l'inspector (l'orchestrateur verifie avant de transmettre) ou le challenger (un autre persona conteste).
