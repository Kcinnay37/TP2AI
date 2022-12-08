Control:
	wasd : bouger
	click gauche: tirer
	click gauche sur agent: le selectionner
	Interface en haut a gauche: changer les etat de l'agent selectionné

a savoir:
	Les AIs peuvent voir devant eux a une distance d'environs deux case, 128p
	
	Les AIs peuvent entendre autour de eux a une distance d'envrions deux case, 128p
	
	Tout les deplacements sont calculé avec astar donc ca peut entrainé des probleme de 
	performance si la config est moin elevé
	
	Defend, objectif: vont a un point pendant un certain temp
	
	Wander: bouge aleatoirement
	
	Search: regarde autour de lui (si il a entendu un coup de feu)
	
	Flee: fuit vert la safe zone, civil(si il a vue le joueur armé, un corp mort ou entendu un coup de feu),
		Garde(si il est low en vie)
		
	Attack: si il recoit une ball, si l'alarm est sonné, ou bien si le joueur est armé trop longtemp
	
	Warn: si il voit le joueur armé il le suit et l'avertie pendant 3 seconde
	
	dead: l'agent vien gris et ne bouge plus, lorsqu'il na plus de vie