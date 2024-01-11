from tkinter import messagebox
from tkinter import *
import random

game = Tk() # Criar a janela
game.title('wordle')
frame = Frame(game)
frame.pack()

#variaveis
letras = []
letter_count = 0
guess = ''
palavras = []
winner = False
palavra = ''  # Initialize 'word' variable
nova_linha = 0

# Get the words from a file
with open('palavras.txt', 'r') as file: #abrir ficheiro "five.text" no modo leitura "r"
    data = file.readlines() #ler o ficheiro linha por linha e guardar numa variavel
    for i in data: #para cada linha do ficheiro
        palavras.append(i[:-1]) #adicionar cada linha à lista "palavras" sem o ultimo caracter "\n"

# Key events
def key_pressed(event): #função que é chamada quando uma tecla é pressionada
    global letter_count, guess, winner, palavras, nova_linha #variaveis globais
    #if not winner: #se o jogo não estiver ganho
    if event.char.isalpha(): #se a tecla pressionada for uma letra
        if letter_count <= 30 and len(guess) < 5: #se o contador de letras for menor ou igual a 29 e o comprimento da palavra for menor que 5
            update_guess(event.char.upper()) #adicionar a letra ao botão correspondente
    elif event.keysym == 'Return':  #Se a tecla pressionada for "Enter
        if len(guess) < 5: #se o comprimento da palavra for menor que 5
            menor5() #chamar a função "menor5"
            guess = '' #repor a variavel "guess"
        elif guess.lower() in palavras: #se a palavra estiver na lista de palavras
            check_word()
            guess = '' #repor a variavel "guess"
            nova_linha = letter_count
        else: #se a palavra não estiver na lista de palavras
            go_again()
            guess = '' #repor a variavel "guess"
        if letter_count == 30:
            win_lose()

def update_guess(char): #função que é chamada quando uma letra é pressionada
    global letter_count, guess #variaveis globais
    letras[letter_count]['text'] = char #adicionar a letra ao botão correspondente
    letter_count += 1 #incrementar o contador de letras
    guess += char #adicionar a letra à variavel "guess"

def check_word(): #verificar se a palavra está correta
    global winner, palavra, guess #variaveis globais
    btn_index = letter_count - 5 #indice do primeiro botão da palavra
    for i, letra in enumerate(guess): #percorrer a palavra
        if letra == palavra[i]: #se a letra estiver na posição correta
            letras[btn_index + i]['bg'] = '#27e512' #mudar a cor do botão para verde
            letras[btn_index + i]['activebackground'] = '#27e512' #mudar a cor do botão para verde
        elif letra in palavra: #se a letra estiver na palavra mas na posição errada
            if guess.count(letra) == palavra.count(letra): #se a letra estiver na palavra o mesmo numero de vezes que na palavra
                letras[btn_index + i]['bg'] = '#e8ef0e' #mudar a cor do botão para amarelo
                letras[btn_index + i]['activebackground'] = '#e8ef0e'    #mudar a cor do botão para amarelo
            else:
                letras[btn_index + i]['bg'] = '#4c4c4c' #mudar a cor do botão para cinzento
                letras[btn_index + i]['activebackground'] = '#4c4c4c' #mudar a cor do botão para cinzento
        else:
            letras[btn_index + i]['bg'] = '#4c4c4c' #mudar a cor do botão para cinzento
            letras[btn_index + i]['activebackground'] = '#4c4c4c'   #mudar a cor do botão para cinzento
    if guess == palavra: #se a palavra estiver correta
        winner = True #o jogo é ganho
        win_lose() #chamar a função "win_lose"

def go_again(): #função que é chamada quando a palavra não está na lista de palavras
    global letter_count #variavel global
    letter_count -= 5
    for i in range(5): #percorrer os 5 botões
        letras[letter_count + i]['text'] = ' ' #limpar o texto dos botões
    messagebox.showinfo(title='Aviso', message='A palavra não existe na lista') #mostrar mensagem

def menor5(): #função que é chamada quando a palavra tem menos de 5 letras
    global letter_count #variavel global
    messagebox.showinfo(title='Aviso', message='A palavra tem ter 5 letras')
    letter_count -= len(guess) #decrementar o contador de letras
    for i in range(5): #percorrer os 5 botões
        letras[letter_count + i]['text'] = ' ' #limpar o texto dos botões


def win_lose(): #função que é chamada quando o jogo é ganho ou perdido
    global winner, palavra #variaveis globais
    if not winner: #se o jogo não estiver ganho
        title = 'You Lose'
        message = f'The palavra was {palavra}'
    else:
        title = 'You Win'
        message = 'Well done, you got it in {} guess(s)'.format(int(letter_count / 5)) #mensagem
    play_again = messagebox.askquestion(title=title, message=f'{message}.\nWould you like to play again?') #mostrar mensagem e guardar a resposta
    if play_again == 'yes': #se a resposta for sim
        Inicio() #chamar a função "layout"
    else:
        game.destroy() #fechar a janela
        quit() #sair do programa


def delete_letter(): # Adding handling for the "Backspace" key
    global letter_count, guess, winner, nova_linha #variaveis globais
    if letter_count > nova_linha: #se o jogo não estiver ganho e o contador de letras for maior que 0 e o contador de letras não for divisivel por 5
        letter_count -= 1 #decrementar o contador de letras
        letras[letter_count]['text'] = ' ' #limpar o botão correspondente
        guess = guess[:-1] #remover a ultima letra da variavel "guess"


def Inicio(): #função que é chamada quando o jogo começa
    global frame, letter_count, winner, guess, palavra #variaveis globais
    frame.destroy() #destruir o frame
    frame = Frame(game) #criar um frame
    frame.pack() #mostrar o frame
    letras.clear() #limpar a lista de botões
    letter_count = 0 #repor o contador de letras
    winner = False #repor a variavel "winner"
    guess = '' #repor a variavel "guess"
    palavra = random.choice(palavras).upper() #escolher uma palavra aleatoria da lista de palavras e colocar em maiusculas
    print(palavra)
    for linha in range(6): #percorrer as 6 linhas
        for coluna in range(5): #percorrer as 5 colunas
            btn = Button(frame, text = ' ', width = 1, bg = 'white', activebackground = 'white', font = 'Verdana, 38') #criar um botão
            btn.grid(row = linha, column = coluna, padx = 3, pady = 5) #mostrar o botão
            letras.append(btn) #adicionar o botão à lista de botões
    menu = Menu(game) #criar um menu
    game.config(menu=menu) #mostrar o menu
    menu.add_command(label='Novo Jogo', command=Inicio) #adicionar uma opção ao menu
    game.mainloop() #mostrar a janela

game.bind('<Key>', key_pressed) #chamar a função "key_pressed" quando uma tecla é pressionada
game.bind('<BackSpace>', lambda event: delete_letter()) #chamar a função "delete_letter" quando a tecla "Backspace" é pressionada
game.bind('<Return>', key_pressed) #chamar a função "key_pressed" quando a tecla "Enter" é pressionada
Inicio() #chamar a função "layout"



