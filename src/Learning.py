""" pseudo code : 

cr�er un dict[hashcode]=relevant (relevant est un sous dict de data)
avec hashcode  = mois+heure+nombre(ASS_ASSIGNMENT)+WEEK_DAY

Parcourir le fichier csv (le dict data qui en est extrait cf main)
    
    pour chaque ligne : placer sa valeur dans le dict au hashcode correspondant (mois+heure+nombre(ASS_ASSIGNMENT)+WEEK_DAY)
    
calculer quantile(0.95) pour chaque value du dict et en d�duire un autre dict du m�me hashcode : learning, le conserver

dans main : associer � chaque ligne de submission.txt la valeur contenue dans learnign[hashcode(ligne)]


"""


""" � noter : taille du dict 15000 environ en regroupant les dates par mois.Il contient des int �a devrait passer ? """