# Rapport TP Agents IA

Étudiante : Meriame El Ouahabi

## Exercices

### Exercice 1.1

Le raisonnement dans reasoning_content est correct. Le modèle a compris que l'utilisateur voulait le résultat de 15 fois 8. Ensuite il a regardé les outils qu'on lui a donnés et il a choisi Calculator avec l'opération multiply, a = 15 et b = 8. Les étapes sont logiques et ce qu'il prépare dans son raisonnement est la même chose que ce qu'on retrouve dans tool_calls.

Le champ tool_calls contient l'appel que le LLM veut faire. On y trouve le nom de la fonction (Calculator), les arguments à lui donner (sous forme de texte JSON), un id et le type, qui est function. Je pense que l'id sert à relier le résultat de l'outil à cet appel quand on le renverra au LLM. Le champ content est vide, donc le LLM ne répond pas encore à la question : il demande d'abord qu'on utilise l'outil.

Le LLM a choisi d'appeler Calculator parce qu'on lui a donné cet outil dans la requête avec tools=tools. Il se base sur les outils qu'on lui propose, et comme la description de Calculator correspond à ce que l'utilisateur demande, il fait cet appel. C'est aussi plus sûr, parce que le LLM ne calcule pas vraiment, il prédit du texte.

Sans l'argument tools, le LLM ne sait pas que l'outil existe. Il fait donc le calcul lui-même et répond directement « 15 times 8 is 120 ». En regardant son raisonnement, j'ai vu qu'il s'était trompé dans une étape (il a écrit 120 + 40 = 160), même si la réponse finale était juste. Ça montre bien l'intérêt d'utiliser un outil pour les calculs.

## Difficultés rencontrées

Au début, mon script semblait bloqué : l'appel au LLM ne finissait pas. J'ai aussi eu un problème avec git, car GitHub refusait mon mot de passe au moment du push.

## Démarche suivie

J'ai d'abord vérifié que le serveur marchait bien avec curl, et il répondait. J'ai ensuite mesuré le temps d'une réponse simple : presque une minute pour quelques mots. En regardant les ressources de ma machine virtuelle, j'ai vu qu'elle n'avait que 2 processeurs et 1,9 Go de RAM, alors que le modèle fait 2,8 Go. Il ne tenait donc pas en mémoire et utilisait le disque (swap), ce qui le rendait très lent.

## Solutions apportées et résultats

J'ai augmenté la mémoire de la VM à environ 6 Go et je lui ai donné 5 processeurs. Le modèle est devenu environ 30 fois plus rapide et le script s'exécute maintenant en moins d'une minute. Pour git, j'ai créé un token sur GitHub et je l'ai utilisé à la place du mot de passe.
