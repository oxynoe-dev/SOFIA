# Transfert de contexte post-reorganisation

> Creer les personas ne suffit pas. Il faut transferer ce qu'ils doivent savoir.

---

## Le cas

Split d'une instance de 7 personas en 3 instances. Le diagnostic : le probleme n'etait pas le bus qui sature — c'etait la granularite des personas (deux metiers dans le meme contexte). Le split regle la granularite. Mais les 6 nouveaux personas demarrent sans contexte — pas d'historique des decisions, des etudes, des echecs.

C'est exactement le probleme de l'onboarding humain dans une equipe existante.

## Ce qu'on a observe

1. **Le premier transfert a fonctionne.** Mira a produit une note structuree (9 etudes + figures, avec quoi/ou/pourquoi/priorites). Aurele a pu demarrer immediatement.

2. **Le transfert n'etait pas prevu dans le plan de migration.** L'etude cible decrivait la topologie, les personas, les scripts. Pas le transfert de contexte. On l'a decouvert apres coup.

3. **Le mapping n'est pas 1:1.** Un emetteur peut alimenter plusieurs destinataires (Mira → Aurele + Emile + Livia). L'orchestrateur a identifie un transfert manquant que l'architecte n'avait pas vu.

4. **L'auto-transfert est un cas particulier.** Quand un persona change d'instance mais garde son nom (Marc), il doit documenter lui-meme ce qui change dans son perimetre. Pas de note externe — travail reflexif.

## Protocole de transfert

Quand un perimetre change de main :

1. **L'ancien owner produit une note structuree** — quoi, ou, pourquoi, ce qui reste chez lui. Format libre, contenu obligatoire.
2. **L'orchestrateur verifie la completude** — tous les flux de connaissance sont-ils couverts ? Le mapping emetteur/destinataire n'est pas evident.
3. **Distinguer contexte operationnel et historique** — les fichiers se transferent. Le "pourquoi on a fait ce choix" est plus dur a capturer. Les sessions contiennent ce contexte mais ne sont pas structurees pour le transfert.

## Memoire Claude

La memoire projet Claude (`~/.claude/projects/`) ne se transfere pas automatiquement lors d'un split. Apres une reorg :

- **Nettoyer** — retirer les memories qui concernent l'ancien perimetre
- **Differencier** — chaque nouvelle instance a sa propre memoire, meme si le persona garde le meme nom
- **Ne pas copier en bloc** — la memoire de l'ancienne instance melange les domaines qu'on vient de separer

**Signe** : un persona qui "se souvient" de decisions prises dans un perimetre qui n'est plus le sien. La memoire est devenue du bruit.

## La regle

**Le transfert de contexte est une etape explicite de toute reorganisation**, au meme titre que la creation des personas et des conventions. Ne pas le planifier = laisser les nouveaux personas naviguer a l'aveugle.
