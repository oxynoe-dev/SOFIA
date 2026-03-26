# Artefacts comme protocole

> Les personas communiquent par fichiers, pas par chat.

---

## Le principe

Dans Voix, les personas ne "parlent" pas entre eux. Ils déposent
des **artefacts** — des fichiers structurés, versionnés, dans des
emplacements convenus.

C'est plus lent qu'une conversation. C'est le but.

## Pourquoi des fichiers ?

### L'écriture force la clarté

Un architecte qui dépose une review a pris le temps de structurer
sa pensée. Un dev qui dépose un signalement de friction a formulé
le problème clairement. Un stratège qui dépose 3 questions a choisi
les 3 qui comptent.

Le chat encourage le flux de conscience. Le fichier encourage la
synthèse.

### Les fichiers persistent

Une conversation se ferme, un contexte se compresse. Un fichier
reste. Il est versionné par git. Il peut être relu dans 6 mois.

### Les fichiers sont adressables

"Voir la review de Mira sur l'ADR-057" est une référence précise.
"Ce qu'on a dit en session mardi" ne l'est pas.

## Types d'artefacts

| Type | Convention de nommage | Emplacement |
|------|----------------------|-------------|
| Review | `review-{sujet}-{auteur}.md` | `shared/review/` |
| Note | `note-{destinataire}-{sujet}-{auteur}.md` | `shared/notes/` |
| Résumé de session | `{YYYY-MM-DD}-{HHmm}-{persona}.md` | `{workspace}/sessions/` |
| ADR | `adr-{NNN}.md` | Selon le projet |
| Spec | `spec-{composant}.md` | `{workspace}/doc/` |

## Flux type

```
Architecte                    shared/                     Dev
──────────                    ───────                     ───
rédige review           ───→  review/review-xyz-mira.md
                                                    ←───  lit la review
                                                          rédige réponse
                         ←──  notes/note-mira-xyz-axel.md
lit la note
                              ↓
                        PO lit les deux, tranche
```

## Conventions

- Un artefact = un sujet. Pas de fichier fourre-tout.
- Le nom du fichier dit qui l'a écrit et pour qui/quoi.
- Les artefacts sont courts. Si ça dépasse 2 pages, c'est un doc, pas une note.
- Les artefacts ne sont jamais modifiés après dépôt — on en crée un nouveau (v2) si nécessaire.
