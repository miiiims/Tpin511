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

### Exercice 1.2

Dans cet exercice, c'est le  programme qui exécute l'outil demandé par le LLM avec execute_tool. Le résultat obtenu est '120'. On l'a ensuite renvoyé au LLM, qui a répondu « 15 times 8 is 120. ». Cette fois, la réponse vient bien du résultat de l'outil et non d'un calcul fait par le LLM. Le programme sert d'intermédiaire entre le LLM et l'outil, c'est ce qu'on appelle le harnais.

Il faut ajouter la réponse du LLM avant le résultat de l'outil parce que le LLM ne se souvient de rien entre deux appels. Il ne connaît que ce qu'on lui renvoie dans messages, c'est-à-dire l'historique de la conversation. Sans ce message, il recevrait un résultat sans savoir qu'il l'avait demandé, et il risquerait d'inventer une réponse. Le plus important dans ce message est le champ tool_calls, qui garde la trace de sa demande.

Le champ tool_call_id permet de relier le résultat à l'appel qui a été fait avant. On y met le même id que celui de l'appel. Ici il n'y avait qu'un seul appel, mais si le LLM demandait plusieurs outils en même temps, c'est cet id qui permettrait de savoir quel résultat correspond à quel appel.

Pour la dernière question, j'ai testé en enlevant l'ajout du résultat de l'outil. Le serveur a renvoyé une erreur 400 Bad Request. J'ai vérifié sur internet : l'API d'OpenAI impose qu'un message assistant avec des tool_calls soit suivi d'un message tool pour chaque tool_call_id, et notre serveur llama.cpp applique la même règle.
