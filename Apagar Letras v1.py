from tkinter import messagebox
from tkinter import *
import random

game = Tk() # Criar a janela
game.title('Wordle')
frame = Frame(game)
frame.pack()

# Variables
green = '#27e512'
yellow = '#e8ef0e'
gray = '#4c4c4c'
font = 'Verdana, 38'
letras = []
letter_count = 0
advinhos = ''
palavras = []
winner = False
palavra = ''  # Initialize 'word' variable
pause = False
enter = False

# Get the words from a file
with open('palavras.txt', 'r') as file: #abrir ficheiro "five.text" no modo leitura "r"
    data = file.readlines() #ler o ficheiro linha por linha e guardar numa variavel
    for i in data: #para cada linha do ficheiro
        palavras.append(i[:-1]) #adicionar cada linha à lista "palavras" sem o ultimo caracter "\n"

# Key events
def key_pressed(event): #função que é chamada quando uma tecla é pressionada
    global letter_count, guess, winner, word, pause #variaveis globais
    if not winner: #se o jogo não estiver ganho
        if event.char.isalpha(): #se a tecla pressionada for uma letra
            if letter_count <= 29: #se o contador de letras for menor ou igual a 29
                update_guess(event.char.upper()) #adicionar a letra ao botão correspondente
                if letter_count % 5 == 0:#se o contador de letras for divisivel por 5
                    pause = True
                if letter_count == 30: #se o contador de letras for igual a 30
                    win_lose() #chamar a função "win_lose"
        elif event.keysym == 'Return':  #Se a tecla pressionada for "Enter"
            pause = False
            if guess.lower() in palavras:
                check_word()
                guess = ''
            else:
                letter_count -= 5
                go_again()
                guess = ''
            if letter_count == 30:
                win_lose()

def update_guess(char): #função que é chamada quando uma letra é pressionada
    global letter_count, guess #variaveis globais
    letras[letter_count]['text'] = char #adicionar a letra ao botão correspondente
    letter_count += 1 #incrementar o contador de letras
    guess += char #adicionar a letra à variavel "guess"

def check_word(): #função que é chamada quando o jogador acerta na palavra
    global winner, word, guess #variaveis globais
    btn_index = letter_count - 5 #indice do primeiro botão da palavra
    for i, letter in enumerate(guess): #percorrer a palavra
        if letter == word[i]: #se a letra estiver na posição correta
            letras[btn_index + i]['bg'] = green #mudar a cor do botão para verde
            letras[btn_index + i]['activebackground'] = green #mudar a cor do botão para verde
        elif letter in word: #se a letra estiver na palavra mas na posição errada
            if guess.count(letter) >= 1 and guess.count(letter) == word.count(letter): #se a letra estiver na palavra o mesmo numero de vezes que na palavra
                letras[btn_index + i]['bg'] = yellow #mudar a cor do botão para amarelo
                letras[btn_index + i]['activebackground'] = yellow    #mudar a cor do botão para amarelo
            else:
                letras[btn_index + i]['bg'] = gray #mudar a cor do botão para cinzento
                letras[btn_index + i]['activebackground'] = gray #mudar a cor do botão para cinzento
        else:
            letras[btn_index + i]['bg'] = gray #mudar a cor do botão para cinzento
            letras[btn_index + i]['activebackground'] = gray   #mudar a cor do botão para cinzento
    if guess == word: #se a palavra estiver correta
        winner = True #o jogo é ganho
        win_lose() #chamar a função "win_lose"

def go_again(): #função que é chamada quando a palavra não está na lista de palavras
    global letter_count #variavel global
    for i in range(5): #percorrer os 5 botões
        letras[letter_count + i]['text'] = ' ' #limpar o texto dos botões
    messagebox.showinfo(title='Aviso', message='A palavra não existe na lista') #mostrar mensagem

def win_lose(): #função que é chamada quando o jogo é ganho ou perdido
    global winner, word #variaveis globais
    if not winner: #se o jogo não estiver ganho
        title = 'You Lose'
        message = f'The word was {word}'
    else:
        title = 'You Win'
        message = 'Well done, you got it in {} guess(s)'.format(int(letter_count / 5)) #mensagem
    play_again = messagebox.askquestion(title=title, message=f'{message}.\nWould you like to play again?') #mostrar mensagem e guardar a resposta
    if play_again == 'yes': #se a resposta for sim
        layout() #chamar a função "layout"
    else:
        game.destroy() #fechar a janela
        quit() #sair do programa
'''       
def n_guess():
    global leter_count, n
    while letter_count % 5 == 0:
        n = n + 1
    return n
'''

def a(event):
     global enter, letter_count
     if event.keysym == 'Return':
         enter = True
         letter_count = 0
     #if letter_count == 0:
        # enter = False
     #elif letter_count % 6 == 0:
        #enter = False
    

def delete_letter(): # Adding handling for the "Backspace" key
    global letter_count, guess, winner, enter #variaveis globais
    if not winner and letter_count != 0 or not enter: #se o jogo não estiver ganho e o contador de letras for maior que 0 e o contador de letras não for divisivel por 5
    #if not winner and letter_count > 0 or (n != 1 or n != 2 or n != 3 or n == 4 or n == 5 or n == 6):
        letter_count -= 1 #decrementar o contador de letras
        #if letter_count == 0:
            #enter = True
        letras[letter_count]['text'] = ' ' #limpar o botão correspondente
        guess = guess[:-1] #remover a ultima letra da variavel "guess"
        

def layout(): #função que é chamada quando o jogo começa
    global frame, letter_count, winner, guess, word #variaveis globais
    frame.destroy() #destruir o frame
    frame = Frame(game) #criar um frame
    frame.pack() #mostrar o frame
    letras.clear() #limpar a lista de botões
    letter_count = 0 #repor o contador de letras
    winner = False #repor a variavel "winner"
    guess = '' #repor a variavel "guess"
    word = random.choice(palavras).upper() #escolher uma palavra aleatoria da lista de palavras e colocar em maiusculas
    for linha in range(6): #percorrer as 6 linhas
        for coluna in range(5): #percorrer as 5 colunas
            btn = Button(frame, text = ' ', width = 1, bg = 'white', activebackground = 'white', font = font) #criar um botão
            btn.grid(row = linha, column = coluna, padx = 3, pady = 5) #mostrar o botão
            letras.append(btn) #adicionar o botão à lista de botões
    menu = Menu(game) #criar um menu
    game.config(menu=menu) #mostrar o menu
    new_game = Menu(menu) #criar um sub-menu
    menu.add_command(label='Novo Jogo', command=layout) #adicionar uma opção ao menu
    game.bind('<Key>', key_pressed) #chamar a função "key_pressed" quando uma tecla é pressionada
    game.bind('<BackSpace>', lambda event: delete_letter()) #chamar a função "delete_letter" quando a tecla "Backspace" é pressionada
    game.bind('<Return>', key_pressed) #chamar a função "key_pressed" quando a tecla "Enter" é pressionada
    game.mainloop() #mostrar a janela

game.bind('<Key>', key_pressed) #chamar a função "key_pressed" quando uma tecla é pressionada
layout() #chamar a função "layout"
game.mainloop() #mostrar a janela
