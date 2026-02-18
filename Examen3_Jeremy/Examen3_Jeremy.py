def afficher_memoires(memories):
    print("\n--- Mémoires ---")
    for k, v in memories.items():
        etat = "vide" if v is None else v
        print(f"{k} : {etat}")


def demander_nombre_avec_memoire(memories, prompt):
    """
    Demande un nombre à l'utilisateur, avec option d'utiliser une mémoire.
    Retourne un float.
    Peut lever ValueError si l'entrée est invalide.
    """
    reponse = input("Utiliser une mémoire ? (o/n) : ").strip().lower()

    if reponse == "o":
        afficher_memoires(memories)
        mem = input("Choisir une mémoire (M1..M5) : ").strip().upper()

        if mem not in memories:
            raise ValueError("Mémoire invalide. Choisissez entre M1 et M5.")

        if memories[mem] is None:
            raise ValueError("Cette mémoire est vide. Impossible de l'utiliser.")

        return float(memories[mem])

    # sinon : saisie normale
    return float(input(prompt))


def operations_multiples(memories):
    """
    Permet de faire des opérations (+, -, *, /) avec plusieurs nombres
    Retourne le résultat (float) ou None si erreur.
    """
    try:
        op = input("Choisissez une opération (+, -, *, /) : ").strip()
        if op not in ["+", "-", "*", "/"]:
            raise ValueError("Opération invalide. Choisissez +, -, * ou /.")

        n = int(input("Combien de nombres voulez-vous utiliser (minimum 2) ? "))
        if n < 2:
            raise ValueError("Vous devez entrer au moins 2 nombres.")

        nombres = []
        for i in range(n):
            while True:
                try:
                    val = demander_nombre_avec_memoire(memories, f"Entrez le nombre {i+1} : ")
                    nombres.append(val)
                    break
                except ValueError as ve:
                    print(f"Erreur : {ve} Recommencez.")

        resultat = nombres[0]

        if op == "+":
            for x in nombres[1:]:
                resultat += x
        elif op == "-":
            for x in nombres[1:]:
                resultat -= x
        elif op == "*":
            for x in nombres[1:]:
                resultat *= x
        elif op == "/":
            for x in nombres[1:]:
                if x == 0:
                    raise ZeroDivisionError("Division par zéro est impossible !")
                resultat /= x

        calcul_str = f" {op} ".join(str(x) for x in nombres)
        print(f"Calcul : {calcul_str} = {resultat}")

        return resultat

    except ValueError as ve:
        print(f"Erreur : {ve}")
    except ZeroDivisionError as zde:
        print(f"Erreur : {zde}")
    except Exception as e:
        print(f"Erreur inattendue : {e}")

    return None


def gestion_memoire(memories, dernier_resultat):
    """
    Menu de gestion des mémoires M1..M5
    Retourne rien (modifie directement le dict memories)
    """
    while True:
        print("\n=== GESTION DE LA MÉMOIRE ===")
        print("a. Stocker le dernier résultat dans une mémoire")
        print("b. Afficher toutes les mémoires")
        print("c. Effacer une mémoire")
        print("d. Effacer toutes les mémoires")
        print("e. Retour au menu principal")

        choix = input("Votre choix (a-e) : ").strip().lower()

        if choix == "a":
            if dernier_resultat is None:
                print("Erreur : aucun résultat à stocker (fait un calcul avant).")
                continue

            mem = input("Dans quelle mémoire stocker ? (M1..M5) : ").strip().upper()
            if mem not in memories:
                print("Erreur : mémoire invalide.")
                continue

            memories[mem] = dernier_resultat
            print(f"✅ {dernier_resultat} stocké dans {mem}")

        elif choix == "b":
            afficher_memoires(memories)

        elif choix == "c":
            mem = input("Quelle mémoire effacer ? (M1..M5) : ").strip().upper()
            if mem not in memories:
                print("Erreur : mémoire invalide.")
                continue
            memories[mem] = None
            print(f"✅ {mem} effacée.")

        elif choix == "d":
            for k in memories:
                memories[k] = None
            print("✅ Toutes les mémoires ont été effacées.")

        elif choix == "e":
            break

        else:
            print("Choix invalide.")


def calcularice():
    """
    Fonction principale de la calculatrice
    """
    print("=== CALCULATRICE SIMPLE ===")

    # Mémoires M1..M5
    memories = {"M1": None, "M2": None, "M3": None, "M4": None, "M5": None}
    dernier_resultat = None

    while True:
        print("\nOpérations disponibles :")
        print("1. Addition (+)")
        print("2. Soustraction (-)")
        print("3. Multiplication (*)")
        print("4. Division (/)")
        print("5. Quitter")
        print("6. Opérations multiples (+, -, *, /)")
        print("7. Gestion de la mémoire")

        try:
            choix = input("Quel est votre choix (1-7) : ").strip()

            if choix == '5':
                print("Merci d'avoir utilisé la calculatrice. Au revoir !")
                break

            if choix not in ['1', '2', '3', '4', '6', '7']:
                raise ValueError("Choix invalide. Veuillez entrer un nombre entre 1 et 7.")

            # --- Options 1 à 4 (avec option mémoire avant chaque nombre) ---
            if choix in ['1', '2', '3', '4']:
                try:
                    num1 = demander_nombre_avec_memoire(memories, "Entrez le premier nombre : ")
                    num2 = demander_nombre_avec_memoire(memories, "Entrez le deuxième nombre : ")
                except ValueError:
                    raise ValueError("Veuillez entrer un nombre valide (ou une mémoire valide).")

                if choix == '1':
                    resultat = num1 + num2
                    operateur = "+"
                elif choix == '2':
                    resultat = num1 - num2
                    operateur = "-"
                elif choix == '3':
                    resultat = num1 * num2
                    operateur = "*"
                elif choix == '4':
                    if num2 == 0:
                        raise ZeroDivisionError("Division par zéro est impossible !")
                    resultat = num1 / num2
                    operateur = "/"

                print(f"Résultat : {num1} {operateur} {num2} = {resultat}")
                dernier_resultat = resultat  # ✅ sauvegarde du dernier résultat

            # --- Option 6 (opérations multiples) ---
            elif choix == '6':
                res = operations_multiples(memories)
                if res is not None:
                    dernier_resultat = res  # ✅ sauvegarde du dernier résultat

            # --- Option 7 (gestion mémoire) ---
            elif choix == '7':
                gestion_memoire(memories, dernier_resultat)

        except ValueError as ve:
            print(f"Erreur : {ve}")
        except ZeroDivisionError as zde:
            print(f"Erreur: {zde}")
        except Exception as e:
            print(f"Erreur inattendue : {e}")


calcularice()
