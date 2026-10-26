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

### Exercice 2.1

La boucle agent permet de rappeler le LLM autant de fois que nécessaire, en lui renvoyant à chaque tour tout l'enchaînement de la conversation, c'est-à-dire la question de l'utilisateur, ses demandes d'outils et les résultats obtenus. Contrairement à l'exercice 1.2, où on faisait exactement deux appels, le LLM peut ainsi enchaîner plusieurs outils avant de donner sa réponse. La boucle s'arrête dès que la réponse du LLM ne contient plus de tool_calls, et on renvoie alors son contenu.

J'ai testé l'agent avec trois questions de calcul et les réponses étaient toutes correctes. Pour une question avec un seul calcul comme 15 fois 8, il faut deux tours, le premier pour demander l'outil et le second pour répondre avec le résultat. Pour une question avec deux calculs comme (15 fois 8) plus 20, il faut trois tours, car on ajoute un message assistant et un message tool de plus avant la réponse finale. En affichant le rôle et le contenu des messages à chaque tour, j'ai pu voir la liste grandir au fur et à mesure.

Le paramètre max_iterations limite le nombre de tours de la boucle, ce qui permet d'éviter une boucle infinie si le LLM continuait à demander des outils sans jamais répondre. Pour le vérifier, je l'ai mis à 2. La question qui demandait deux calculs a alors renvoyé « Max iterations reached », car le LLM avait fait ses deux calculs mais n'avait plus de tour pour donner sa réponse.

J'ai aussi remarqué que le LLM n'utilise pas toujours l'outil, même quand il est disponible. Lors d'un test, il a répondu à la question avec deux calculs en un seul tour, en faisant le calcul lui-même. Dans un autre test, il a utilisé l'outil pour la division mais a fait la soustraction tout seul. Les résultats étaient justes, mais rien ne le garantissait, et une consigne dans un system prompt pourrait l'obliger à toujours utiliser l'outil.

### Exercice 2.2

Pour l'agent SQL, j'ai repris la boucle de l'exercice 2.1 en remplaçant Calculator par les trois outils créés par make_sql_tools, qui sont ListTables, DescribeTable et SQLQuery. Ces outils sont créés à l'intérieur d'une fonction qui reçoit la base de données, car le LLM ne peut envoyer que du texte et ne pourrait pas leur transmettre la base lui-même. J'ai aussi ajouté le system prompt de base donné dans le TP, qui demande au LLM d'explorer le schéma avant d'écrire une requête.

En affichant les outils appelés, j'ai pu voir comment l'agent trouve une réponse. Il commence par lister les tables, puis il décrit celles qui l'intéressent pour savoir quelles colonnes elles contiennent, un peu comme il lisait la description des outils dans les exercices précédents. Il transforme ensuite la question de l'utilisateur en requête SQL, l'exécute et répond à partir du résultat. Lors d'un test, il a même décrit les tables authors et books dans le même tour, ce qui montre l'intérêt de traiter chaque tool_call avec une boucle. Chaque question a demandé entre 4 et 5 tours, donc la limite de 5 itérations a été respectée, mais parfois de justesse.

Pour vérifier les réponses, j'ai ouvert la base avec sqlite3 et j'ai écrit moi-même les requêtes correspondant aux cinq questions. Les résultats étaient identiques pour les quatre premières. Pour la dernière, l'agent a répondu que l'auteur ayant écrit le plus de livres était Ursula K. Le Guin, alors que ma requête montrait que quatre auteurs étaient à égalité avec 3 livres. En affichant sa requête, j'ai vu qu'il avait utilisé ORDER BY avec LIMIT 1, qui ne garde que la première ligne. Comme le résultat ne contenait qu'un seul auteur, il ne pouvait pas savoir qu'il y avait une égalité, et sa réponse était donc incomplète.

### Exercice 2.3

J'ai testé les trois variantes du system prompt sur les cinq questions et j'ai comparé leurs résultats avec ceux de la version de base.

La variante A, qui demande d'utiliser des JOIN, n'a rien apporté, car l'agent en utilisait déjà quand c'était nécessaire. Elle a même été moins bonne, puisqu'une question a atteint la limite de 5 tours sans obtenir de réponse. La variante C, qui demande d'expliquer le raisonnement avant chaque outil, n'a presque rien changé, car le LLM n'a écrit qu'une seule explication en plus. Ce modèle raisonne déjà tout seul dans reasoning_content, donc lui demander de penser étape par étape a peu d'effet visible, même si c'est possible et déjà présent dans la version de base.

J'ai retenu la variante B, qui demande de corriger la requête en cas d'erreur. C'est celle qui a donné toutes les bonnes réponses avec le moins de tours, 19 contre 23 pour les autres. Le prompt a donc une influence sur le nombre d'itérations, même si l'écart reste faible et peut aussi venir du fait que le LLM ne répond pas toujours de la même façon. Aucune requête n'a échoué pendant mes tests, mais cette consigne reste la plus utile en pratique, car elle permet à l'agent de se corriger grâce au vrai message d'erreur de SQLite au lieu de s'arrêter.

## Difficultés rencontrées

Au début, mon script semblait bloqué parce que l'appel au LLM ne finissait jamais. J'ai aussi eu un problème avec git, car GitHub refusait mon mot de passe au moment du push.

Sur le TP lui-même, j'ai d'abord eu du mal à comprendre le rôle de chaque message, car je pensais que c'était l'assistant qui exécutait l'outil. J'ai aussi obtenu une erreur 400 Bad Request quand le résultat de l'outil n'était pas ajouté à l'historique. Enfin, le LLM ne se comporte pas toujours de la même façon, puisqu'il a parfois donné une réponse vide, n'a pas toujours utilisé l'outil disponible et a donné une réponse incomplète à la question sur l'auteur ayant écrit le plus de livres.

## Démarche suivie

J'ai d'abord vérifié avec curl que le serveur fonctionnait, et il répondait bien. J'ai ensuite mesuré le temps d'une réponse simple, qui prenait presque une minute pour quelques mots. En regardant les ressources de ma machine virtuelle, j'ai vu qu'elle n'avait que 2 processeurs et 1,9 Go de RAM alors que le modèle fait 2,8 Go. Comme il ne tenait pas en mémoire, il utilisait le disque (swap), ce qui le rendait très lent.

Pour les exercices, j'ai avancé étape par étape en affichant à chaque fois ce que renvoyait le LLM, comme le schéma des outils, le contenu de messages à chaque tour et les outils appelés par l'agent. J'ai aussi fait des tests en enlevant volontairement des éléments du code ou en baissant max_iterations pour voir ce qui se passait. J'ai travaillé sur des branches git pour tester sans abîmer la version principale.

## Solutions apportées et résultats

J'ai augmenté la mémoire de la VM à environ 6 Go et je lui ai donné 5 processeurs, ce qui a rendu le modèle environ 30 fois plus rapide, et le script s'exécute maintenant en moins d'une minute. Pour git, j'ai créé un token sur GitHub que j'utilise à la place du mot de passe.

En affichant l'historique des messages, j'ai compris que l'assistant demande l'outil et que c'est notre programme qui l'exécute. L'erreur 400 a disparu une fois le message tool ajouté avec le bon tool_call_id. Pour vérifier les réponses de l'agent SQL, j'ai écrit moi-même les requêtes dans sqlite3, ce qui m'a permis de repérer le problème du LIMIT 1. Comme le LLM varie d'une exécution à l'autre, j'ai lancé certains tests plusieurs fois avant de tirer des conclusions.

## Réflexions

Je pense que le tool calling est un pilier du fonctionnement d'un agent. Sans lui, le LLM ne fait que prédire du texte et peut se tromper, comme l'erreur 120 + 40 = 160 que j'ai vue au début du TP. Avec les outils, c'est du vrai code qui calcule ou qui lit la base, donc les résultats sont fiables. Le mécanisme est aussi assez simple, puisque le LLM ne fait que demander un outil et que c'est notre programme qui l'exécute, l'id permettant ensuite de relier chaque résultat à la bonne demande.

Le principal risque d'un agent SQL est qu'il puisse modifier ou effacer la base. Avec la base du TP, une demande comme « supprime tous les livres » pourrait vider une table, et ce serait comme une attaque si quelqu'un le faisait volontairement. Une consigne dans le system prompt ne suffit pas, car un utilisateur peut demander à l'agent d'ignorer ses consignes. Il faut donc protéger l'agent dans le code, par exemple en ouvrant la base en lecture seule et en n'acceptant que les requêtes de lecture.

Pour la gestion du contexte, la liste des messages grossit à chaque tour alors que le serveur est limité à 16 000 tokens. On pourrait compresser la conversation, comme le font certains agents que j'ai déjà utilisés, en résumant les anciens messages et en ne gardant que ce qui est important. On peut aussi couper les résultats d'outils trop longs et garder une limite sur le nombre de tours.

J'aimerais ajouter une couche de sécurité à l'agent, car la sécurité des agents IA m'intéresse beaucoup. C'est ce que je compte faire ensuite avec l'extension sur les garde-fous de sécurité.

## Annexe

Code de sqlite_agent.py avec des commentaires.

    from utils import Database
    from utils import make_sql_tools
    from utils import make_registry
    from utils import make_tools
    from utils import call_llm
    from utils import execute_tool

    # consigne pour le LLM (variante B)
    SYSTEM_PROMPT = """You are a SQL assistant with access to a SQLite database.

    Tools:
    - ListTables: list all tables
    - DescribeTable: get table structure
    - SQLQuery: execute any SQL query

    Think step by step. Explore the schema first, then query.
    If a query fails, analyze the error and try again with a corrected query."""


    def extract_message(response):
        return response['choices'][0]['message']


    # la boucle agent
    def boucle_agent(question, tools, registry, max_iterations=5):
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ]

        i = 0
        while i < max_iterations:
            print("Number", i + 1)
            CALL = call_llm(messages, tools=tools)
            message = extract_message(CALL)
            messages.append(message)

            # pas d'outil demande donc le LLM a fini
            if not message.get('tool_calls'):
                return message['content']

            # on execute les outils et on renvoie le resultat au LLM
            for tool_call in message['tool_calls']:
                resultat = execute_tool(tool_call, registry)
                print("   ", tool_call['function']['name'], tool_call['function']['arguments'])
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call['id'],
                    "content": resultat,
                })

            i = i + 1

        return "Max iterations reached"


    # la base, les outils et les 5 questions
    if __name__ == "__main__":
        db = Database("library.db")
        sql_tools = make_sql_tools(db)

        tools = make_tools(sql_tools)
        registry = make_registry(sql_tools)

        questions = [
            "What are the books written after 1970?",
            "Who is the author of 'Dune' and when were they born?",
            "How many books are there per genre?",
            "What is the average rating per publisher?",
            "Which author has written the most books?",
        ]

        for question in questions:
            print("Question :", question)
            reponse = boucle_agent(question, tools, registry)
            print("Reponse a la question :", reponse)
            print()
