###################################################  La classe Automate : ###################################################
class Automate:
    def __init__(self, alphabet, etats, etat_initial, etats_finaux, instructions):
        self.alphabet = alphabet
        self.etats = etats
        self.etat_initial = etat_initial
        self.etats_finaux = etats_finaux
        self.instructions = instructions
    def getAlphabet(self):
        return self.alphabet
    def getEtats(self):
        return self.etats
    def getEtatInitial(self):
        return self.etat_initial
    def getEtatsFinaux(self):
        return self.etats_finaux
    def getInstructions(self):
        return self.instructions
    def setInstructions(self, instructions):
        self.instructions = instructions
    def setEtatsFinaux(self, etats_finaux):
        self.etats_finaux = etats_finaux
    def setEtats(self, etats):
        self.etats = etats
    def setEtatInitial(self, etat_initial):
        self.etat_initial = etat_initial
###################################################  Réduction d'un automate : ###################################################
def etat_accessible(automate):
    etat_acc=[]
    etat_deja_etudie=[]
    etat_acc.append(automate.getEtatInitial())
    for cle in automate.getInstructions().keys():
        if (cle[0]==automate.getEtatInitial()):
            for etat in automate.getInstructions().get(cle):
                if etat not in etat_acc:
                    etat_acc.append(etat)
    etat_deja_etudie.append(automate.getEtatInitial())
    for elt in etat_acc:
        if(elt not in etat_deja_etudie):
            for etat in automate.getInstructions().keys():
                if (etat[0]==elt):
                    for j in automate.getInstructions().get(etat):
                        if(j not in etat_deja_etudie) and (j not in etat_acc):
                            etat_acc.append(j)
                        etat_deja_etudie.append(elt)    
    return etat_acc

def successeur_etat(s,automate):
    successeur=[]
    etat_deja_etudie=[]
    for etat in automate.getInstructions().keys():
        if (etat[0]==s):
            for j in automate.getInstructions().get(etat):
                    successeur.append(j)
    etat_deja_etudie.append(s)
    for elt in successeur:
        if(elt not in etat_deja_etudie):
            for etat in automate.getInstructions().keys():
                if (etat[0]==elt):
                    for j in automate.getInstructions().get(etat):
                        if(j not in etat_deja_etudie) and (j not in successeur):
                            successeur.append(j)
                        etat_deja_etudie.append(elt)
    return successeur

def is_coaccessible(s,automate):
    if(s in automate.etats):
        if(s in automate.getEtatsFinaux()) or (intersection_2_listes(automate.getEtatsFinaux(),successeur_etat(s,automate))!=[]):
            return True
        else:
            return False

def etat_coaccessible(automate):
    etat_coacc=[]
    for etat in automate.getEtats():
        if (is_coaccessible(etat,automate)):
            etat_coacc.append(etat)
    return etat_coacc
        
def reduction_automate(automate):
    acc_coacc=[]
    instructions_new={}
    acc_coacc=intersection_2_listes(etat_coaccessible(automate),etat_accessible(automate))
    for key, value in automate.getInstructions().items():
        if( key[0] in acc_coacc):
            l=[]
            for val in value:
                if(val in acc_coacc):
                    l.append(val)
            if len(l)!=0:
                instructions_new[key]=l
    automate.setEtats(acc_coacc)
    automate.setInstructions(instructions_new)
    automate.setEtatsFinaux(intersection_2_listes(acc_coacc,automate.getEtatsFinaux()))
    return automate
#########################################  Transformation d'un automate non déterministe à un automate déterministe : #########################################
def elimination_epsilon(automate):
    etats = automate.getEtats()
    etatsf = automate.getEtatsFinaux()
    instructions = automate.getInstructions()
    ins = dict()
    ef = []
    alphabet = automate.getAlphabet()
    for i in range(len(etats)):
        l = fermeture(etats[i], automate)
        for j in range(len(l)):
            if ((l[j] in etatsf)==True and (etats[i] in etatsf)==False):
                ef.append(etats[i])
            for k in range(len(alphabet)):
                tuplet = (l[j], alphabet[k])
                if (tuplet in instructions):
                     ins[(etats[i], alphabet[k])] = instructions[tuplet]
    etatsf = etatsf + ef
    instructions1 = dict()
    for key in instructions.keys():
        if (key[1]!=""):
            instructions1[key] = instructions[key]
    instructions = instructions1
    for key in ins.keys():
        if key in instructions:
            for i in range(len(ins[key])):
                if (ins[key][i] in instructions[key])==False:
                    instructions[key] = instructions[key] + [ins[key][i]]
        else:
            instructions[key] = ins[key]
    automate.setEtatsFinaux(etatsf)
    automate.setInstructions(instructions)
    return automate

def fermeture(etat, automate):
    l = []
    tuplet = (etat, "")
    if (tuplet in automate.getInstructions()):
        liste = automate.getInstructions()[tuplet]
        for i in range(len(liste)):
            if (liste[i] in l)==False:
                l.append(liste[i])
            li = fermeture(liste[i], automate)
            for j in range(len(li)):
                if (li[j] in l)==False:
                    l.append(li[j])
    return l

def fonction(liste, lettre, automate):
    l = []
    for etat in liste:
        tuplet = (etat, lettre)
        if tuplet in automate.getInstructions():
            ll = automate.getInstructions()[tuplet]
            for element in ll:
                if (element in l)==False:
                    l.append(element)
    return l

def intersection_2_listes(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 

def non_deterministe_to_deterministe_complet(automate):
    a = automate_generalise_vers_partiellement_generalise(automate)
    a = elimination_epsilon(a)
    eff = a.getEtatsFinaux()
    ef = []
    ins = dict()
    liste = [ [a.getEtatInitial()] ]
    i = 0
    alphabet = automate.getAlphabet()
    while (True):
        try:
            for lettre in alphabet:
                l = fonction(liste[i], lettre, automate)
                e = str(liste[i])
                if len(l)==0:
                    d = ["Sp"]
                else:
                    l.sort()
                    d = [str(l)]
                ins[(e, lettre)] = d
                if (l in liste)==False and len(l)!=0:
                    liste.append(l)
            i = i + 1
        except:
            break
    for lettre in alphabet:
        ins[("['Sp']", lettre)] = ["Sp"]
    etats = []
    for element in liste:
        if len(intersection_2_listes(element, eff))!=0:
            ef.append(str(element))
        etats.append(str(element))
    etats.append("['Sp']")
    b = Automate(alphabet, etats, str([a.getEtatInitial()]), ef, ins)
    return b
####################################  Transformation d'un automate généralisé à un automate partiellement généralisé : ####################################
def automate_generalise_vers_partiellement_generalise(automate):
        automate = reduction_automate(automate)
        instructions = automate.getInstructions()
        etats = automate.getEtats()
        ins = dict()
        delete = []
        for instruction in instructions.keys():
            if len(instruction[1])>1:
                delete.append(instruction)
                s0 = instruction[0]
                lettres = list(instruction[1])
                for k in range(len(lettres)-1):
                    tuplet = (s0, lettres[k])
                    s0 = s0 + "." + str(k)
                    ins[tuplet] = [s0]
                    etats.append(s0)
                ins[(s0, lettres[len(lettres)-1])] = instructions[instruction]
        for instruction in delete:
            del instructions[instruction]
        for key in ins.keys():
            if key in instructions:
                instructions[key] = instructions[key] + ins[key]
            else:
                instructions[key] = ins[key]
        automate.setEtats(etats)  
        automate.setInstructions(instructions)
        return automate
###################################################  Complement d'un automate : ###################################################
def complement_automate(automate):
    automate = non_deterministe_to_deterministe_complet(automate)
    l = []
    for etat in automate.getEtats():
        if etat not in automate.getEtatsFinaux():
            l.append(etat)
    automate.setEtatsFinaux(l)
    return automate
###################################################  Miroir d'un automate : ###################################################
def miroir_automate(automate):
    ins = dict()
    automate = automate_generalise_vers_partiellement_generalise(automate)
    automate.setEtats(automate.getEtats()+["SI"])
    ins[("SI", "")] = automate.getEtatsFinaux()
    automate.setEtatsFinaux([automate.getEtatInitial()])
    automate.setEtatInitial(["SI"])
    for key, value in automate.getInstructions().items():
        for etat in value:
            if ((etat, key[1]) in ins):
                if (key[0] not in ins[(etat, key[1])]):
                    ins[(etat, key[1])] = ins[(etat, key[1])] + [key[0]]
            else:
                ins[(etat, key[1])] = [key[0]]
    automate.setInstructions(ins)
    return automate
#########################################  Reconnaissance d'un mot dans un automate non déterministe : #########################################
def word_recognition(mot, etati, l, etatsf, a):
    bl = False
    if len(mot)!=0:
        lettre = mot[0]
        mot = mot[1:len(mot)]
        s = (etati,lettre)
        try:
            for i in a[s]:
                bl = bl or word_recognition(mot, i, l, etatsf, a)
                if bl:
                    l.append(i)
                    break
        except:
            bl = False
    else:
        bl = (etati in etatsf)
    return bl

def reconnaissance_mot_automate_non_deterministe(mot, automate):
    automate = automate_generalise_vers_partiellement_generalise(automate)
    l = list()
    if word_recognition(mot, automate.getEtatInitial(), l, automate.getEtatsFinaux(), automate.getInstructions()):
        l.append(automate.getEtatInitial())
        l.reverse()
        print("Le mot : "+mot+" est reconnu par l'automate !")
        if len(l)==1:
            print("On est dans un état final et on a rien à lire")
        else:
            for i in range (len(l)-1):
                print(l[i]+","+mot[i]+","+l[i+1]+"\n")
            print("On a terminé de lire tout le mot et on est arrivé à un état final : "+l[i+1])
    else:
        print("Le mot : "+mot+" n'est pas reconnu par l'automate !")
###################################################  Affichage d'un automate : ###################################################
def afficher_automate(automate):
    print("Alphabet : ")
    print(automate.getAlphabet())
    print("Etats : ")
    print(automate.getEtats())
    print("Etat initial : ")
    print(automate.getEtatInitial())
    print("Etats finaux : ")
    print(automate.getEtatsFinaux())
    print("Instructions : ")
    print(automate.getInstructions())
###################################################  Construction d'un automate : ###################################################
def chaine_correcte(chaine, alphabet):
    correcte = True
    for lettre in list(chaine):
        if lettre not in alphabet:
            correcte = False 
            break
    return correcte

def construire_automate():
    #Debut de la partie d'introduction des données pour tester le programme        
    print("Construction de l'automate ")
    #Introduction de l'alphabet de notre automate
    alphabet = []
    etats = []
    etats_finaux = []
    stop = False
    while stop == False:
        nb=int(input("introduisez le nombre des lettres de l'alphabet "))
        if nb>0:
            stop = True
    while nb > 0:
        print("introduisez une lettre ")
        lettre=str(input())
        if (lettre not in alphabet and lettre!="" and len(lettre)==1):
            alphabet.append(lettre)
            nb=nb-1
    #Initialisation de l'état initial "etat_initial"
    etat_initial=input("introduisez l'état initial de l'automate ")
    #Initialisation des états finaux "etats_finaux"
    etats_finaux = []
    nb=int(input("introduisez le nombre des états finaux "))
    while nb > 0:
        print("introduisez un état final ")
        etat_final=str(input())
        if etat_final not in etats_finaux:
            etats_finaux.append(etat_final)
            nb=nb-1
    #Introduction des autres états de l'automate
    etats = etats + etats_finaux
    if etat_initial not in etats:
        etats.append(etat_initial)
    nb=int(input("introduisez le nombre d'états différents de l'état initial et les états finaux "))
    while nb > 0:
        print("introduisez un état ")
        etat=str(input())
        if etat not in etats:
            etats.append(etat)
            nb=nb-1
    #Construction de l'ensemble des instructions de l'automate "a"
    print("Construction de l'ensemble des instructions ")
    liste=[]
    a = {}
    stop=0
    j=1
    continu=1
    boucle = True
    while continu==1:
            while (boucle):
                etat=input("introduisez un état ")
                if etat not in etats:
                    print("Erreur, état inexistant dans la liste des états de l'automate ")
                else:
                    boucle = False
            boucle = True
            while (boucle):
                lettre=input("mot ou lettre à lire ")
                if chaine_correcte(lettre, alphabet):
                    boucle = False
                else:
                    print("Erreur, la chaine entrée est incorrecte ")
            boucle = True
            tup=(etat,lettre)
            print("introduction des états où on peut aller ")
            while stop==0:
                while (boucle):
                    etati=input("introduisez le "+str(j)+" (er/ème) état destination ")
                    if etati not in etats:
                        print("Erreur, état inexistant dans la liste des états de l'automate ")
                    else:
                        boucle = False
                boucle = True
                j=j+1
                if etati not in liste:
                    liste.append(etati)
                rep=input("ajouter un autre état ? o/n ")
                if rep=="n" or rep=="no":
                    stop=1
            if tup in a:
                for element in liste:
                    if element not in a[tup]:
                        a[tup] = a[tup] + [element]
            else:
                a[tup] = liste
            stop=0
            j=1
            liste=[]
            rep2=input("ajouter une autre instruction à l'automate ? o/n ")
            if rep2=="n":
                continu=0
    #Construire l'objet automate
    return Automate(alphabet, etats, etat_initial, etats_finaux, a)
#####################################  Sauvegarde et la lecture d'un automate à partir d'un fichier : ######################################
def lire_fichier(nomFichier):
    automate = None
    try:
        file = open(nomFichier)
        alphabet = file.readline().replace("\n","").split(" ")
        alphabet.pop()
        etats = file.readline().replace("\n","").split(" ")
        etats.pop()
        etati = file.readline().replace("\n","").split(" ")[0]
        etatsf = file.readline().replace("\n","").split(" ")
        etatsf.pop()
        ins = dict()
        instruction = file.readline().replace("\n","").split(" ")
        if len(instruction)==1:
            fin = True
        else:
            fin = False
        while (not fin):
            instruction.pop()
            tuplet = (instruction[0], instruction[1])
            del instruction[0]
            del instruction[0]
            l = []
            for etat in instruction:
                l.append(etat)
            ins[tuplet] = l
            instruction = file.readline().replace("\n","").split(" ")
            if len(instruction)==1:
                fin = True
            else:
                fin = False
        automate = Automate(alphabet, etats, etati, etatsf, ins)
        file.close()
        return automate
    except:
        return automate

def ecrire_fichier(nomFichier, automate):
    file = open(nomFichier, "w")
    for lettre in automate.getAlphabet():
        file.write(lettre+" ")
    file.write("\n")
    for etat in automate.getEtats():
        file.write(etat+" ")
    file.write("\n")
    file.write(automate.getEtatInitial()+"\n")
    for etatf in automate.getEtatsFinaux():
        file.write(etatf+" ")
    file.write("\n")
    for key, value in automate.getInstructions().items():
        chaine = key[0] + " " + key[1] + " "
        for etat in value:
            chaine = chaine + etat + " "
        chaine = chaine + "\n"
        file.write(chaine)
    file.close()
###################################################  Affichage au niveau de la console (execution) : ###################################################
from consolemenu import *
from consolemenu.items import *

def fonction0():
    nomFichier = input("Entrez le nom du fichier où l'automate est sauvegardé (précisez l'extension) ")
    automate = lire_fichier(nomFichier)
    if (automate!=None):
        afficher_automate(automate)
    else:
        print("Erreur au niveau du nom du fichier ")

def fonction1():
    nomFichier = input("Entrez le nom du fichier où l'automate est sauvegardé (précisez l'extension) ")
    automate = lire_fichier(nomFichier)
    if (automate!=None):
        afficher_automate(reduction_automate(automate))
    else:
        print("Erreur au niveau du nom du fichier ")
    
def fonction2():
    nomFichier = input("Entrez le nom du fichier où l'automate est sauvegardé (précisez l'extension) ")
    automate = lire_fichier(nomFichier)
    if (automate!=None):
        afficher_automate(non_deterministe_to_deterministe_complet(automate))
    else:
        print("Erreur au niveau du nom du fichier ")
    
def fonction3():
    nomFichier = input("Entrez le nom du fichier où l'automate est sauvegardé (précisez l'extension) ")
    automate = lire_fichier(nomFichier)
    if (automate!=None):
        afficher_automate(complement_automate(automate))
    else:
        print("Erreur au niveau du nom du fichier ")
    
def fonction4():
    nomFichier = input("Entrez le nom du fichier où l'automate est sauvegardé (précisez l'extension) ")
    automate = lire_fichier(nomFichier)
    if (automate!=None):
        afficher_automate(miroir_automate(automate))
    else:
        print("Erreur au niveau du nom du fichier ")
    
def fonction5():
    mot = input("Entrez un mot ")
    nomFichier = input("Entrez le nom du fichier où l'automate est sauvegardé (précisez l'extension) ")
    automate = lire_fichier(nomFichier)
    if (automate!=None):
        reconnaissance_mot_automate_non_deterministe(mot, automate)
    else:
        print("Erreur au niveau du nom du fichier ")

def fonction6():
    automate = construire_automate()
    print("****************************************************** ")
    nomFichier = input("Entrez le nom du fichier où vous sauvegarderez l'automate (précisez l'extension) ")
    ecrire_fichier(nomFichier, automate)

# MENU #
menu = ConsoleMenu("Automates d'états finis", "Un environnement contenant quelques opérations sur les automates.")

function_item0 = FunctionItem("Afficher un automate", fonction0)
function_item1 = FunctionItem("Réduire un automate", fonction1)
function_item2 = FunctionItem("Passage d’un automate non déterministe vers un déterministe", fonction2)
function_item3 = FunctionItem("Complément d’un automate", fonction3)
function_item4 = FunctionItem("Miroir d’un automate", fonction4)
function_item5 = FunctionItem("Reconnaissance d'un mot dans un automate non déterministe", fonction5)
function_item6 = FunctionItem("Construire un automate", fonction6)

menu.append_item(function_item0)
menu.append_item(function_item1)
menu.append_item(function_item2)
menu.append_item(function_item3)
menu.append_item(function_item4)
menu.append_item(function_item5)
menu.append_item(function_item6)

menu.show()
