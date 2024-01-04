import tkinter
from tkinter import *
from tkinter import messagebox
import random


janela = tkinter.Tk() #criar a janela
janela.title('Wordle') #mudar o nome da janela
janela.resizable(False, False) #não deixar alterar o tamanho da janela
frame = tkinter.Frame(janela) #criar um quadradinhos dentro da janela
frame.pack()

# variables
green = '#27e512'
yellow = '#e8ef0e'
gray = '#4c4c4c'
font = 'Verdana, 38'
letters = []
letter_count = 0
guess = ''
palavras = []
winner = False

# get the palavras from a file
with open('five.txt') as file: #abrir ficheiro "five.text" no modo leitura "r"
    data = file.readlines() #ler o ficheiro linha por linha e guardar numa variavel
    for i in data:
        palavras.append(i[:-1]) #adicionar cada linha à lista "palavras" sem o ultimo caracter "\n"


# key events
def key_pressed(event): #função que é chamada quando uma tecla é pressionada
    global letter_count, guess #variaveis globais: chamar variaveis fora da função para a função
    if not winner: #se o jogo não estiver ganho
        if event.char >= 'a' and event.char <= 'z' or event.char >= 'A' and event.char <= 'Z': #se a tecla pressionada for uma letra
            if letter_count <= 29: #se o contador de letras for menor ou igual a 29
                letters[letter_count]['text'] = event.char.upper() #adicionar a letra ao botão correspondente
                letters[letter_count].focus() #focar o botão
                guess = guess + event.char.upper() #adicionar a letra à variavel "guess"
                letter_count += 1 #incrementar o contador de letras
                if letter_count % 5 == 0: #se o contador de letras for divisivel por 5
                    if guess.lower() in palavras: #se a palavra estiver na lista de palavras
                        check_word(guess)   #chamar a função "check_word"
                        guess = '' #limpar a variavel "guess"
                    else: #se a palavra não estiver na lista de palavras
                        letter_count -= 5 #decrementar o contador de letras
                        go_again() #chamar a função "go_again"
                        guess = '' #limpar a variavel "guess"
            if letter_count == 30: #se o contador de letras for igual a 30
                win_lose(winner) #chamar a função "win_lose"
#apagar letras
def delete_letter():
    global letter_count, guess
    if letter_count > 0:
        letter_count -= 1
        letters[letter_count]['text'] = ' '
        guess = guess[:-1]

def win_lose(winner): #função que é chamada quando o jogo é ganho ou perdido
    if not winner: #se o jogo não estiver ganho
        titulo = 'You Lose' #titulo da mensagem
        mensagem = f'A palavra é {palavra}' #mensagem
    else:
        titulo = 'Ganhaste' #titulo da mensagem
        mensagem = 'Parabéns, tu acertaste em {} tentativa(s)'.format(int(letter_count / 5)) #mensagem
    play_again = messagebox.askquestion(title=titulo, message=f'{mensagem}.\nWould you like to play again?') #mostrar mensagem e guardar a resposta
    if play_again == 'Sim': #se a resposta for sim
        layout() #chamar a função "layout"
    else:
        janela.destroy() #fechar a janela
        quit() #sair do programa


def go_again(): #função que é chamada quando a palavra não está na lista de palavras
    for i in range(5): #percorrer os 5 botões
        letters[letter_count + i]['text'] = ' ' #limpar o texto dos botões


# check word
def check_word(guess): #função que é chamada quando o jogador acerta na palavra
    global winner #variavel global
    btn_index = letter_count - 5 #indice do primeiro botão da palavra
    for i, letter in enumerate(guess): #percorrer a palavra
        if letter == palavra[i]: #se a letra estiver na posição correta
            letters[btn_index + i]['bg'] = green #mudar a cor do botão para verde
            letters[btn_index + i]['activebackground'] = green #mudar a cor do botão para verde
        elif letter in palavra: #se a letra estiver na palavra mas na posição errada
            if guess.count(letter) >= 1 and guess.count(letter) == palavra.count(letter): #se a letra estiver na palavra o mesmo numero de vezes que na palavra
                letters[btn_index + i]['bg'] = yellow #mudar a cor do botão para amarelo
                letters[btn_index + i]['activebackground'] = yellow     #mudar a cor do botão para amarelo
            else:
                letters[btn_index + i]['bg'] = gray #mudar a cor do botão para cinzento
                letters[btn_index + i]['activebackground'] = gray   #mudar a cor do botão para cinzento
        else:
            letters[btn_index + i]['bg'] = gray #mudar a cor do botão para cinzento
            letters[btn_index + i]['activebackground'] = gray  #mudar a cor do botão para cinzento
    if guess == palavra: #se a palavra estiver correta
        winner = True #o jogo é ganho
        win_lose(winner) #chamar a função "win_lose"


# layout
def layout(): #função que é chamada quando o jogo começa ou quando o jogador quer jogar outra vez
    global frame, letter_count, winner, guess, palavra #variaveis globais
    frame.destroy() #destruir o quadradinho
    frame = tkinter.Frame(janela) #criar um novo quadradinho
    frame.pack() #mostrar o quadradinho
    letters.clear() #limpar a lista de botões
    letter_count = 0 #repor o contador de letras
    winner = False #repor a variavel "winner"
    guess = '' #repor a variavel "guess"
    palavra = random.choice(palavras).upper() #escolher uma palavra aleatoria da lista de palavras e colocar em maiusculas
    #print(palavra) #mostrar a palavra no terminal
    for row in range(6): #percorrer as linhas
        for col in range(5): #percorrer as colunas
            btn = tkinter.Button(frame, text=' ', width=1, bg='white', activebackground='white', font=font) #criar um botão
            btn.grid(row=row, column=col, padx=3, pady=5) #mostrar o botão
            letters.append(btn) #adicionar o botão à lista de botões
    menu = tkinter.Menu(janela) #criar um menu
    janela.config(menu=menu) #mostrar o menu
    new_game = tkinter.Menu(menu) #criar um sub-menu
    menu.add_command(label='New Game', command=layout) #adicionar uma opção ao menu
    janela.bind('<Key>', key_pressed)
    janela.bind('<BackSpace>', lambda event: delete_letter())  # Bind Backspace key to delete_letter
    janela.mainloop()


janela.bind('<Key>', key_pressed) #chamar a função "key_pressed" quando uma tecla é pressionada
layout()    #chamar a função "layout"
janela.mainloop() #mostrar a janela
