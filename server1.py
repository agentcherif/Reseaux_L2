#!/usr/bin/python3
#coding:UTF_8

"""
Importation  des modules 
"""
import socket
import select
import string
import sys
 
"""
HOST : varriable pour le localhost
PORT : varriable pour le numéro de port
"""  	
host , port = ('',1459)
"""
Pour créer une socket aussi bien pour le serveur que pour le client
"""
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
"""
pour faire un bind sur un port donné (ici 1459), pour le serveur
"""
s.bind((host , port))
"""
pour écouter sur le port, pour le serveur; Si ce n'est pas possible, une exception socket.error est générée
"""
s.listen(1)

"""
is_nicked : est une fonction qui prend une socket et teste si cette socket est nické.
Genre si la socket  est attribué à un nick 
"""
def is_nicked(soc):
    return type(CAdrr[soc]) is str 

"""
affiche nick : est une fonction qui prend une socket et return sont nick associé
"""
def affiche_nick(soc):
    name = CAdrr[soc]
    name = name[0:len(name)-1]
    return (s2.sendall( ("\n{} >".format(name)).encode()))


def envoit_message(soc,msg):
    return (soc.sendall(msg))



def get_socket(name):
    for sock in CAdrr :
        if CAdrr[sock] == name : 
            return sock

"""
l : est une liste qui contient les socket
""" 
l = []
"""
CAdrr : est un dictionnaire  qui associe chaque socket à un nick
""" 
CAdrr = {} 
"""
Liste_Canal : est une liste qui contient les canaux
""" 
Liste_Canal = []
"""
Membre_Canal : est un dictionnaire qui associe chaque canal, à  la liste des membres  du canal
""" 
Membre_Canal = {}
"""
Client_Canal : est un dictionnaire qui associe chaque client, à  sont canal
""" 
Client_Canal = {}

Membre_Canal_2 = {}

Client_Canal_2 = {}

print("\nWelcome to Chat Room\n")
print("\nWaiting for incoming connections...\n")



while(True):
    r, _, _ = select.select(l + [s], [], [])

    for s2 in r: # la boucle qui parcour les sockets
        if s2 == s: #si c'est un nouveau client
            s2, a = s.accept() 
            print("Nouveau client : ", a) #Affichage au serveur qu'un client vient de connecté
            l = l + [s2]   #Ajout de la socket du client dans l
            CAdrr[s2] = a  # on associe la socket du client  à sont adresse
            
            strings = "Enter your Nick : ".encode() # message envoyer au client pour saisir sont nick
            s2.sendall(strings) 
               
        else: # si c'est n'est pas un nouveaux client
            strings = s2.recv(2048) # on reçoit ce que le client a saisie
            strings_decode = strings.decode() #on decode
            if len(strings) == 0: #si la longueur de ce qu'on a reçut est zéro, alors ça signifie le client n'a rien taper au clavier, donc c'est une fermeture de session 
                print("Client deconnecte : ",CAdrr[s2]) # on affiche dans le serveur que le client s'est déconnecté
                s2.close()# on ferme la socket du client
                l.remove(s2) # on supprime la socke dans le liste l
                sys.exit()
                strings = "PART {}\n".format(CAdrr[s2]).encode() # on encode un message qu'on vas partagé au users
                del CAdrr[s2] #on suprime sont nom dans notre dictionnaire
                for s3 in l:
                    if s3 != s2:
                        s3.sendall(strings) #on informe a tout les users que ce client est partie
                break
            elif not is_nicked(s2): # on teste si la socket est nické
                trouver = False
                for name in CAdrr: #si c'est n'est pas le cas on cherche dans notre dico (CAdrr)
                    if CAdrr[name] == strings_decode: # ici on voit que le nom que l'user a saisie figure dans notre dico
                        trouver = True
                        strings = "Nick already existe\n".encode() # on informe que ce nom existe déjà
                        s2.sendall(strings)
                if trouver == True : 
                    strings = "Enter your Nick : ".encode() # on lui redemande d'entré sont nick
                    s2.sendall(strings)
                else : # sinon ça veut dire que le nick est bon
                    CAdrr[s2] = strings_decode # on attribut le nick a la socket; dans le dico (CAdrr)
                    strings = "Nom ajouté avec success\n".encode() # message de success
                    s2.sendall(strings)
                    affiche_nick(s2) #appel à la fonction (affiche_nick)            
                """
                LIST : une commande qui permet de listé la liste des canaux.
                Si l'utilisateur entre la commande LIST on parcoure la liste des canaux et on les affiches à chaque tour de boucle
                """
            elif strings_decode[0:5] == "/LIST" :
                s2.sendall("La liste des canaux : \n".encode())
                for canal in Liste_Canal:
                    strings = "-> {}\n".format(canal).encode()
                    s2.sendall(strings)
                affiche_nick(s2) #appel à la fonction (affiche_nick)
                
                """
                JOIN <non_canal> : une commande qui permet de réjoindre un canal existant, sinon il le crée.
                Si l'utilisateur entre la commande JOIN on parcoure la liste des canaux,
                si le canal existe le client rejoint, sinon il le crée et le rejoint.
                """  
                
            elif strings_decode[0:5] == "/JOIN" :
                strings_decode = strings_decode.split(" ")
                try:
                    strings_decode[1] is str
                except IndexError :
                    strings = "Syntaxe -> /JOIN <canal_name>\n".encode()
                    s2.sendall(strings)
                    affiche_nick(s2) #appel à la fonction (affiche_nick)
                    break
                if strings_decode[1][0:1] == "":
                    strings = "Syntaxe -> /JOIN <canal_name>\n".encode()
                    s2.sendall(strings)
                    affiche_nick(s2) #appel à la fonction (affiche_nick)
                    break
                trouver = False 
                for client in Client_Canal:
                    if client == CAdrr[s2]:
                        trouver = True
                if trouver :
                    strings = "Vous êtes déja membre d'un canal !\n".encode()
                    s2.sendall(strings)
                    affiche_nick(s2) #appel à la fonction (affiche_nick)
                else : 
                    trouver = False
                    for canal in Liste_Canal:
                        if canal == strings_decode[1]:
                            Membre_Canal[canal].append(CAdrr[s2])
                            Membre_Canal_2[canal].append(s2)
                            trouver = True 
                    if trouver == False :
                        Liste_Canal.append(strings_decode[1])
                        Membre_Canal[strings_decode[1]] = [CAdrr[s2]]
                        Membre_Canal_2[strings_decode[1]] = [s2]
                    Client_Canal[CAdrr[s2]] = strings_decode[1] 
                    Client_Canal_2[s2] = strings_decode[1] 
                affiche_nick(s2) #appel à la fonction (affiche_nick)
                
                """
                WHO : une commande qui permet d'affiche la liste des menbre d'un meme canal.
                Si l'utilisateur entre la commande WHO on parcoure la liste des Client_canal,
                et on affiche la liste de tout ceux qui sont sur le meme canal.
                """
                  
            elif strings_decode[0:4] == "/WHO" :
                trouver = False 
                for client in Client_Canal:
                    if client == CAdrr[s2] :
                        trouver = True
                if trouver :
                    strings = "La liste des client du canal {}\n".format(Client_Canal[CAdrr[s2]]).encode()
                    s2.sendall(strings)
                    admin = 0
                    for client in Membre_Canal[Client_Canal[CAdrr[s2]]]:
                        if not admin :
                            client = client[0:len(client)-1]
                            strings = "-> @{}@  \n".format(client).encode()
                            s2.sendall(strings)
                            admin+=1
                        else :
                            strings = "-> {}\n".format(client).encode()
                            s2.sendall(strings)
                else :
                    strings = "Vous n'êtes membre d'aucun canal !\n".encode()
                    s2.sendall(strings)
                affiche_nick(s2) #appel à la fonction (affiche_nick)
                
            elif strings_decode[0:4] == "/MSG" :
                strings_decode = strings_decode.split(" ",2)
                nom_dest = strings_decode[1]+"\n"
                msg_dest =(strings_decode[2]).encode()
                #print(msg_dest)
                #print(nom_dest)
                
                #sock_dest = get_socket (nom_dest)
                #s2.sendall(msg_dest)
                #print(sock_dest)
                
                find1 = False 
                for client in Client_Canal:
                    if client == CAdrr[s2]:
                        find1 = True 
                        canal_du_client = Client_Canal[client]
                #print(canal_du_client)
                if find1 :
                    find2 = False
                    for name in Membre_Canal[canal_du_client]:
                        print(name)
                        if name == nom_dest:
                            find2 = True     
                    if find2 :
                        sock_dest = get_socket (nom_dest)
                        envoit_message(sock_dest,msg_dest)
                        affiche_nick(s2) #appel à la fonction (affiche_nick)
                    else :
                        string = "Pas de client a ce nom dans votre canal !\n".encode()
                        s2.sendall(string)
                        affiche_nick(s2) #appel à la fonction (affiche_nick)
                else : 
                    string = "Vous n'êtes membre d'aucun canal !\n".encode()
                    s2.sendall(string)
                    affiche_nick(s2) #appel à la fonction (affiche_nick)

                    
                    
            elif strings_decode[0:6] == "/LEAVE":
                Membre_Canal[Client_Canal[CAdrr[s2]]].remove(CAdrr[s2])
                Membre_Canal_2[Client_Canal_2[s2]].remove(s2)
                del Client_Canal[CAdrr[s2]]
                del Client_Canal_2[s2]
                affiche_nick(s2) #appel à la fonction (affiche_nick)
                
                
            elif strings_decode [0:4] == "/BYE":
                trouver = False
                for membre in Client_Canal:
                    if membre == CAdrr[s2]:
                        trouver = True 
                if not trouver : 
                    print("Client deconnecte : ",CAdrr[s2])
                    s2.close()
                    l.remove(s2)
                    sys.exit()
                    strings = "PART {}\n".format(CAdrr[s2]).encode()
                    del CAdrr[s2]
                    for s3 in l:
                        if s3 != s2:
                            s3.sendall(strings)
                    break
                else : 
                    strings  = "Vous ne pouvez pas utilisez cette commande avant de quitter le canal !\n".encode()
                    s2.sendall(strings)
                affiche_nick(s2) #appel à la fonction (affiche_nick)
                
                
            elif strings_decode[0:5] == "/KICK":
                trouver = False 
                for client in Client_Canal:
                    if client == CAdrr[s2]:
                        trouver = True 
                        canal_du_client = Client_Canal[client]
                if trouver :
                    admin = Membre_Canal[Client_Canal[CAdrr[s2]]][0] == CAdrr[s2] 
                    strings_decode = strings_decode.split(" ")
                    try :
                        strings_decode[1] is str 
                    except IndexError :
                        strings = "Syntaxe -> /KICK <nick_name>\n".encode()
                        s2.sendall(strings)
                        affiche_nick(s2) #appel à la fonction (affiche_nick)
                        break
                    if strings_decode[1][0:1] == "":
                        strings = "Syntaxe -> /KICK <nick_name>\n".encode()
                        s2.sendall(strings)
                        affiche_nick(s2) #appel à la fonction (affiche_nick)
                        break

                    if admin :
                        trouver = False 
                        for membre in Membre_Canal[Client_Canal[CAdrr[s2]]] :
                            if membre == strings_decode[1]:
                                trouver = True
                        if trouver :
                            Membre_Canal[Client_Canal[CAdrr[s2]]].remove(strings_decode[1])
                            del Client_Canal[strings_decode[1]]
                        else :
                            s2.sendall("Nick introuvable !".encode())
                            affiche_nick(s2) #appel à la fonction (affiche_nick)
                    else :
                        s2.sendall("Vous n'avez pas le droit d'utiliser cette commande".encode())
                        affiche_nick(s2) #appel à la fonction (affiche_nick)
                else : 
                    strings = "Vous n'êtes membre d'aucun canal !\n".encode()
                    s2.sendall(strings)
                affiche_nick(s2) #appel à la fonction (affiche_nick)
                
                
            elif strings_decode[0:4] == "/REN" :
                trouver = False 
                for client in Client_Canal:
                    if client == CAdrr[s2]:
                        trouver = True 
                        canal_du_client = Client_Canal[client]
                if trouver :
                    admin = Membre_Canal[Client_Canal[CAdrr[s2]]][0] == CAdrr[s2]
                    strings_decode = strings_decode.split(" ")
                    if admin : 
                        nom_act = Client_Canal[CAdrr[s2]]
                        Liste_Canal = [strings_decode[1] if x == nom_act else x for x in Liste_Canal]
                        Membre_Canal[strings_decode[1]] = Membre_Canal[nom_act]
                        del Membre_Canal[nom_act]
                        for memnbre in Membre_Canal[strings_decode[1]] :
                            Client_Canal[memnbre] = strings_decode[1]
                    else :
                        s2.sendall("Vous n'avez pas le droit d'utiliser cette commande".encode())
                else : 
                    strings = "Vous n'êtes membre d'aucun canal !\n".encode()
                    s2.sendall(strings)
                affiche_nick(s2) #appel à la fonction (affiche_nick)
                        
                    
            elif strings_decode[0:5] == "/HELP" :
                s2.send("/LIST: list all available channels on server\n".encode())
                s2.send("/JOIN <channel>: join (or create) a channel\n".encode())
                s2.send("/LEAVE: leave current channel\n".encode())
                s2.send("/WHO: list users in current channel\n".encode())
                s2.send("<message>: send a message in current channel\n".encode())
                s2.send("/MSG <nick> <message>: send a private message in current channel\n".encode())
                s2.send("/BYE: disconnect from server\n".encode())
                s2.send("/KICK <nick>: kick user from current channel [admin]\n".encode())
                s2.send("/REN <channel>: change the current channel name [admin]\n".encode())
                affiche_nick(s2) #appel à la fonction (affiche_nick)
            else:	
                trouver = False 
                for client in Client_Canal:
                    if client == CAdrr[s2] :
                        trouver = True
                if trouver :
                    for membre in Membre_Canal_2[Client_Canal_2[s2] ]:
                        if membre != s2:
                            membre.sendall(strings )
                else :
                    strings = "Vous n'etes membre d'aucun canal !\n".encode()
                    s2.sendall(strings)
                affiche_nick(s2) #appel Ã  la fonction (affiche_nick)
            