
## Limite découverte : sur-généralisation du modèle sur le port de destination

Testé le pipeline de capture en direct (NFStream + Init_Win plugin) contre deux
attaques réelles générées sur le réseau local :

1. **Scan de ports (nmap -p 1-100)** — capturé correctement (100+ flows distincts,
   un port différent chacun), mais classé BENIGN par le modèle avec confiance
   0.82-0.97. Comparaison avec un vrai exemple PortScan du CSV d'entraînement :
   le flow nmap réel dure ~7ms avec 2 paquets et les flags SYN/RST/ACK explicites,
   alors que l'exemple d'entraînement dure ~5s avec 11 paquets, de vraies données
   échangées, et aucun flag SYN/RST/ACK. Vraisemblablement deux outils de scan
   différents ont généré des profils de flow très différents.

2. **Brute-force HTTP (curl en boucle, port 80)** — confiance BENIGN dégradée
   (0.86-0.89 au lieu de 0.96-1.0 habituel) mais jamais basculée en attaque.
   Hypothèse : Destination Port est la feature la plus importante du modèle
   (importance 0.0797) ; FTP-Patator/SSH-Patator n'ont été entraînés que sur les
   ports 21/22, jamais 80 — le modèle associe fortement port 80 à BENIGN peu
   importe le comportement du flow.

**Conclusion** : le modèle généralise mal aux techniques d'attaque ou aux ports
qui diffèrent de ceux utilisés pour générer CICIDS2017 en 2017. C'est une limite
connue des datasets de ce type — utile à mentionner explicitement dans le
rapport final plutôt que de la découvrir en prod. Piste d'amélioration possible :
réentraîner ou fine-tuner avec des exemples de trafic capturés en direct sur ce
réseau, pour réduire la dépendance excessive au port de destination brut.
