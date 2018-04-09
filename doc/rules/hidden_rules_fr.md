# Statistiques cachées en jeu - WIP

Les caractéristiques sont des valeurs pure. Référence: 100 = puissant. Elles peuvent être de n'importe quelle valeur positive, a mettre en relation avec **DiveVal**

Les modificateurs sont des bonus/malus directement aux caractéristiques, 0 correspond a un modificateur d'une maitrise normale de la compétence (rien d'exceptionel ni médiocre). Positif ou négatif.

Les coefficients sont des pourcentages, ils multiplient les valeurs qu'ils affectent. **Attention**, si ils sont trop loin de 100, ils peuvent influencer trop drastiquement. 100 est une valeur normale, d'une maitrise normale

Les **valeurs**, ou **caractéristiques**, sont directement utilisées, affectées par les bonus et les coefficients. Elles sont représentative de la capacité d'effectuer l'action, et seront confronté a celle de l'adversaire: la réussite sera la différence entre une valeur d'attaque et une de défense

L'**accuracy** c'est la précision, elle représente en pourcentage la précision qu'aura la créature a effectuer l'action aussi bien qu'elle sait normalement le faire -> elle représente en quelle que sort l'entraînement. Une valeur de 100 représente une action effectuée toujours aussi bien... ou aussi mal. Elle n'est donc pas choquante, meme pour une créature faible. Le produit des accuracy affectant une action sera majoré par 100%. Enfin, elle indique que si une créature a une valeur de X pour une action, et une accuracy de A%, alors elle fera toujours un résultat entre (A*X)/100, et X.

- CAC = Corps a Corps
- DIST = Attaque a distance

## Constantes

- DiceVal = 2 *Valeur d'attaque correspondant a '1' de plus ou de moins au dé'*
- DamageCoeffPerPoints = 5/100 *Coeff appliqué aux dégats bonus pour chaque point de reussite en plus*
- HumanSize = 3 *Taille standard, sert de référance*
- ProjectilFacilityOnDiffSize = 4 *Bonus/malus attributé aux projectiles quand ils visent des cibles de tailles différentes d'un humain*

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

- Type d'attaque ['contact', 'distance']
- Type de dégats ['contondant', 'tranchant', 'perçant']
- Bonus d'attaque *Ajouté a la valeur de l'attaque, dépend uniquement de l'arme*
- Coeff de maitrise *Maitrise de l'arme par son porteur -> multiplie l'attaque, 100 est une valeur standard*
- bonus force parade *Bonus/malus ajouté a la force du porteur pour parer au CAC: au plus il est haut, au plus on peut parer des adversaires forts*
- base_accuracy de l'arme *(100 pour une arme standard, sa précision naturelle)*
- maitrise_accrucy de l'arme *(100 pour une arme standard, représente l'entrainement)*
- parade_bonus *Quand l'arme permet de parer un peu plus facilement/difficilement*
- parade_CAC_coeff *Quand l'arme affecte de part sa surface drastiquement la manière de parer (ex: lance pierre => 0%)"
- parade_DIST_coeff *Pour parer un projectile. Default: 0%, une arme ne peut pas. Peut valoir > 100% pour un bouclier*
- bonus_force_attaque *Armes lourdes, dont le poid va augmenter leur force de frappe*
- bonus_force_parade *Armes permettant de bloquer plus efficacement un coup trop puissant*
- esquive_difficulté *100 de base. Les armes particulièrement rapides sont plus difficile a esquive. Mutliplier par 2 divise l'esquive adverse par 2*

Pour une arme de tir:

- force projectile
- coeff_bonus_force_creature *0% par defaut. Ce coeff fois la force de la créature est ajouté a la force du projectile*
- 

### Armures et résistances naturelles (peau, écaille)

- Bonus d'esquive
- Valeur de protection
- Bonus de résistance contre
	- Tranchant
	- Perçant
	- Contondant

## Gérer une attaque

### Attaques de CAC - DIST

Soient les créatures **attaquant** et **défenseur**
TYPE = CAC ou DIST

**attaquant**
=> attaque_max = ( attaque TYPE + arme->bonus_attaque) * (arme->maitrise / 100)

*Attaque DIST contre une grosse créature*
SI attaque a distance:
= = = => attaque_max += (cible->taille - HumanSize) * ProjectilFacilityOnDiffSize

=> accuracy = min(1, attaque_TYPE_accuracy * arme->base_accuracy * arme->maitrise_accuracy / 100^3)
=> attaque_min = attaque_max * accuracy

**défenseur**

**Parer avec une arme:**
=> parade_max = ( parade + arme->parade_bonus) * (arme->maitrise / 100) * (arme->parade_TYPE_coeff / 100)

*Prise en compte du choc*
=> force_attaque = attaquant->force + arme->bonus_force_attaque
OU si DIST: force_attaque = force projectile + attaquant->force * projectile->coeff_bonus_force_creature
=> force_defense = attaquant->force + (arme->bonus_force_parade)
=> delta_force = force_attaque - force_defense
SI attaquant->arme->type_de_degats = contondant / Choc ET delta_force > 0:
= = = => parade_max  = parade_max - delta_force

=> parade_accuracy = min(1, parade_accuracy * arme->maitrise_accuracy / 100^2)
=> parade_min = parade_max * parade_accuracy


**Esquiver:**
=> esquive_max = max(0, (esquive + SUM(armures->bonus_esquive) )  / (attaque->esquive_difficulté / 100) )
=> esquive_min = min(1, esquive_accuracy/100) * esquive_max

**combat** *Attaque réussie si la réussite est >= 0*
=> reussite_max = attaque_max - max(parade_min, esquive_min)
=> reussite_min = attaque_min - max(parade_max, esquive_max)
=> delta_reussite = reussite_max - reussite_min

=> degats_purs = attaquant->arme->defense
=> resistance = SUM( defenseur->armure->resistance + defenseur->armure->bonus_resistance_contr(attaquant->arme->type_de_dégat) )
=> degats_base = degats_purs - resistance *Dégats avec l'armure*

**résulat**
=> **dé** = plus_proche_de(delta_reussite / DiceVal)
=> bonus pour pv en plus  = degats_purs * DamageCoeffPerPoints *| Nombre de points ajoutés au dé nécessaires pour faire un dégât de plus*
=> **table** = plus_proche_de(bonus pour pv en plus / cible->Santé par PV)
=> **bonus_degats** = round( 9SUM [pour i de 10 a 20] ( abs( table[i] - ( (degats_base + degats pur/ bonus pour pv en plus) / cible->Santé par PV ) / 10) *| Difference moyenne entre dégats théoriques et donnés par la table*
=> **Bonus dé** = 10 + round( reussite_max / DiceVal ) - dé



































