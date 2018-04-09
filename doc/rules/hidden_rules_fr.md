# Statistiques cachées en jeu - WIP

Les caractéristiques sont des valeurs pure. Référence: 100 = puissant. Elles peuvent être de n'importe quelle valeur positive, a mettre en relation avec **DiveVal**

Les modificateurs sont des bonus/malus directement aux caractéristiques, 0 correspond a un modificateur d'une maitrise normale de la compétence (rien d'exceptionel ni médiocre). Positif ou négatif.

Les coefficients sont des pourcentages, ils multiplient les valeurs qu'ils affectent. **Attention**, si ils sont trop loin de 100, ils peuvent influencer trop drastiquement. 100 est une valeur normale, d'une maitrise normale

Les **valeurs**, ou **caractéristiques**, sont directement utilisées, affectées par les bonus et les coefficients. Elles sont représentative de la capacité d'effectuer l'action, et seront confronté a celle de l'adversaire: la réussite sera la différence entre une valeur d'attaque et une de défense

L'**accuracy** c'est la précision, elle représente en pourcentage la précision qu'aura la créature a effectuer l'action aussi bien qu'elle sait normalement le faire -> elle représente en quelle que sort l'entraînement. Une valeur de 100 représente une action effectuée toujours aussi bien... ou aussi mal. Elle n'est donc pas choquante, meme pour une créature faible. Le produit des accuracy affectant une action sera majoré par 100%. Enfin, elle indique que si une créature a une valeur de X pour une action, et une accuracy de A%, alors elle fera toujours un résultat entre (A*X)/100, et X.

- CAC = Corps a Corps

## Constantes

- DiceVal = 2 *Valeur d'attaque correspondant a '1' de plus ou de moins au dé'*
- DamageCoeffPerPoints = 5/100 *Coeff appliqué aux dégats bonus pour chaque point de reussite en plus*

## Créatures

### Stats

#### Statistiques de base

- Santé *(nombre de points de vie aussi grand que l'on veut)*
- pv *Nombre de blessures que la créature peut subir: la santé est répartie entre les pv*
- force
- esquive *Caractéristique | Facilité a esquiver*
- esquive_accuracy 
- parade
- parade_accuracy
- Attaque CAC
- Attaque CAC accuracy

#### Statistiques générées

- Santé par PV = Santé / pv *Nombre de dégats pour enlever 1 pv*

### Armes

- Type d'attaque
- Bonus d'attaque *Ajouté a la valeur de l'attaque, dépend uniquement de l'arme*
- Coeff de maitrise *Maitrise de l'arme par son porteur -> multiplie l'attaque, 100 est une valeur standard*
- bonus force parade *Bonus/malus ajouté a la force du porteur pour parer au CAC: au plus il est haut, au plus on peut parer des adversaires forts*
- base_accuracy de l'arme *(100 pour une arme standard, sa précision naturelle)*
- maitrise_accrucy de l'arme *(100 pour une arme standard, représente l'entrainement)*
- parade_CAC_bonus *Quand l'arme permet de parer un peu plus facilement/difficilement*
- parade_CAC_coeff *Quand l'arme affecte de part sa surface drastiquement la manière de parer (ex: lance pierre => 0%)"

### Armures et résistances naturelles (peau, écaille)

- Bonus d'esquive
- Valeur de protection

## Gérer une attaque

### Attaques de CAC

Soient les créatures **attaquant** et **défenseur**

**attaquant**:
=> attaque_max = ( attaque CAC + arme->bonus_attaque) * (arme->maitrise / 100)
=> accuracy = min(1, attaque_CAC_accuracy * arme->base_accuracy * arme->maitrise_accuracy / 100^3)
=> attaque_min = attaque_max * accuracy

**défenseur**
Parer avec une arme:
=> parade_max = ( parade + arme->parade_CAC_bonus) * (arme->maitrise / 100) * (arme->parade_CAC_coeff / 100)
=> parade_accuracy = min(1, parade_accuracy * arme->maitrise_accuracy / 100^2)
=> parade_min = parade_max * parade_accuracy
Esquiver:
=> esquive_max = max(0, esquive + SUM(armures->bonus_esquive))
=> esquive_min = min(1, esquive_accuracy/100) * esquive_max

**combat** *Attaque réussie si la réussite est >= 0*
=> reussite_max = attaque_max - max(parade_min, esquive_min)
=> reussite_min = attaque_min - max(parade_max, esquive_max)
=> delta_reussite = reussite_max - reussite_min



**résulat**
=> **dé** = plus_proche_de(delta_reussite / DiceVal)
=> bonus pour pv en plus  = degats_purs * DamageCoeffPerPoints *| Nombre de points ajoutés au dé nécessaires pour faire un dégât de plus*
=> **table** = plus_proche_de(bonus pour pv en plus)
=> **bonus_degats** = round( 9SUM [pour i de 10 a 20] ( abs( table[i] - (degats_pur + degats pur/ bonus pour pv en plus) / 10) *| Difference moyenne entre dégats théoriques et donnés par la table*
=> **Bonus dé** = 10 + round( reussite_max / DiceVal ) - dé



































