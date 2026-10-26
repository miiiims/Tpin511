# Rapport TP Agents IA

Réalisé par Meriame El Ouahabi

## Exercices

### Exercice 1.1

Le raisonnement dans reasoning_content est correct. Le modèle a d'abord compris que l'utilisateur voulait le résultat de 15 fois 8, puis il a regardé les outils qu'on lui avait donnés et il a choisi Calculator avec l'opération multiply, a = 15 et b = 8. Ses étapes sont logiques et ce qu'il prépare dans son raisonnement correspond exactement à ce qu'on retrouve ensuite dans tool_calls.

Le champ tool_calls contient l'appel que le LLM veut faire, avec le nom de la fonction (Calculator), les arguments à lui donner sous forme de texte JSON, un id et le type, qui est function. Je pense que l'id sert à relier le résultat de l'outil à cet appel quand on le renverra au LLM. Le champ content est vide, ce qui veut dire que le LLM ne répond pas encore à la question et qu'il demande d'abord qu'on utilise l'outil.

Le LLM a choisi d'appeler Calculator parce qu'on lui a donné cet outil dans la requête avec tools=tools. Il se base sur les outils qu'on lui propose, et comme la description de Calculator correspond à ce que l'utilisateur demande, il fait cet appel. C'est aussi plus sûr, puisque le LLM ne calcule pas vraiment mais prédit du texte.

Sans l'argument tools, le LLM ne sait pas que l'outil existe, donc il fait le calcul lui-même et répond directement « 15 times 8 is 120 ». En regardant son raisonnement, j'ai vu qu'il s'était trompé dans une étape en écrivant 120 + 40 = 160, même si sa réponse finale était juste, ce qui montre bien l'intérêt d'utiliser un outil pour les calculs.

### Exercice 1.2

Dans cet exercice, c'est le programme qui exécute l'outil demandé par le LLM grâce à execute_tool. Le résultat obtenu est '120' et, une fois renvoyé au LLM, celui-ci a répondu « 15 times 8 is 120. ». Cette fois la réponse vient bien du résultat de l'outil et non d'un calcul fait par le LLM. Le programme sert donc d'intermédiaire entre le LLM et l'outil, et c'est ce qu'on appelle le harnais.

Il faut ajouter la réponse du LLM avant le résultat de l'outil parce que le LLM ne se souvient de rien entre deux appels et qu'il ne connaît que ce qu'on lui renvoie dans messages, c'est-à-dire l'historique de la conversation. Sans ce message, il recevrait un résultat sans savoir qu'il l'avait demandé et il risquerait d'inventer une réponse. Le plus important dans ce message est le champ tool_calls, qui garde la trace de sa demande.

Le champ tool_call_id permet de relier le résultat à l'appel qui a été fait avant, puisqu'on y met le même id que celui de l'appel. Ici il n'y avait qu'un seul appel, mais si le LLM demandait plusieurs outils en même temps, c'est cet id qui permettrait de savoir quel résultat correspond à quel appel.

Pour la dernière question, j'ai testé en enlevant l'ajout du résultat de l'outil et le serveur a renvoyé une erreur 400 Bad Request. En cherchant sur internet, j'ai vu que l'API d'OpenAI impose qu'un message assistant avec des tool_calls soit suivi d'un message tool pour chaque tool_call_id, et notre serveur llama.cpp applique la même règle.

### Exercice 1.3

J'ai créé un outil WordCounter sous forme de dataclass, sur le même modèle que Calculator. Il contient un docstring qui décrit ce qu'il fait (« Count the number of words in a text. »), un champ text de type str et une méthode __call__ qui renvoie len(self.text.split()). Le LLM a choisi cet outil tout seul et a trouvé 6 mots, ce qui est correct. Au début, j'avais pensé reprendre la description de Calculator, mais j'ai compris que le docstring doit être précis puisque c'est la seule information que le LLM utilise pour choisir l'outil.

Le LLM connaît les paramètres de l'outil grâce au schéma JSON que make_tools crée à partir des champs de la dataclass. Dans la partie parameters, properties donne le nom et le type de chaque paramètre (par exemple text est de type string), tandis que required indique ceux qui sont obligatoires. Le LLM ne voit donc jamais le code Python mais seulement ce schéma, ce qu'on retrouve dans son raisonnement quand il décrit l'outil avec un paramètre text obligatoire et un paramètre language optionnel.

Quand on ajoute un champ avec une valeur par défaut, il apparaît dans le schéma avec default et il n'est plus dans required, ce qui le rend facultatif. Dans mon test, le LLM a compris que language était optionnel et ne l'a pas mis dans ses arguments, si bien que Python a utilisé la valeur par défaut english.

On peut aussi ajouter un champ Literal["french", "english"], qui devient dans le schéma un enum avec la liste des valeurs autorisées, comme operation dans Calculator. Cependant, le LLM ne respecte pas toujours parfaitement le schéma, car dans un de ses raisonnements il a pensé à mettre « en », qui ne faisait pas partie de la liste.

Enfin, j'ai remarqué qu'en lançant deux fois le même programme, la première réponse finale était vide alors que la deuxième était une phrase complète, ce qui montre que le LLM ne donne pas toujours la même réponse.

## Difficultés rencontrées

Au début, mon script semblait bloqué parce que l'appel au LLM ne finissait jamais. J'ai aussi eu un problème avec git, car GitHub refusait mon mot de passe au moment du push.

## Démarche suivie

J'ai d'abord vérifié avec curl que le serveur fonctionnait, et il répondait bien. J'ai ensuite mesuré le temps d'une réponse simple, qui prenait presque une minute pour quelques mots. En regardant les ressources de ma machine virtuelle, j'ai vu qu'elle n'avait que 2 processeurs et 1,9 Go de RAM alors que le modèle fait 2,8 Go. Comme il ne tenait pas en mémoire, il utilisait le disque (swap), ce qui le rendait très lent.

## Solutions apportées et résultats

J'ai augmenté la mémoire de la VM à environ 6 Go et je lui ai donné 5 processeurs, ce qui a rendu le modèle environ 30 fois plus rapide, et le script s'exécute maintenant en moins d'une minute. Pour git, j'ai créé un token sur GitHub que j'utilise à la place du mot de passe.
