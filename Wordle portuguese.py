from tkinter import messagebox
from tkinter import *
import random # Escolha aleatória de uma palavra da lista

main_window = Tk()
main_window.title("Wordle em Português")

#set the window size
sw = main_window.winfo_screenwidth()
sh = main_window.winfo_screenheight()
x = ((sw - 425)/2)
y = ((sh - 425)/2)
main_window.geometry("%dx%d+%d+%d" % (425, 425, x, y))

main_window.resizable(FALSE,FALSE) #not resizable
icone = PhotoImage (file = "wordle icon.png") #set the picture
iconeLbl = Label(main_window, image = icone).place(x=160, y=50) #set the picture position
main_window.iconphoto(True, icone) #set the picture as icon

Label(main_window, text= "Wordle em Português", font= ('Verdana 17 bold')).place(x=75, y=160)
Label(main_window, text= "Tens 6 chances para adivinhar", font= ('Verdana 15')).place(x=55, y=200)
Label(main_window, text= "uma palavra com 5 letras", font= ('Verdana 15')).place(x=77, y=230)

#varibles
letras = []
palavras = []
nova_linha = 0
num_letras = 0 # "Contador de letras (nº de letras)"
termo = '' # Palavra a adivinhar
tentativa = '' # Palavra/tentativa do jogador
tentativa_certa = False


def janela1():
    global verde, amarelo, cinzento
    janela1= Toplevel(main_window)
    janela1.title("Instruções")
    sw = janela1.winfo_screenwidth()
    sh = janela1.winfo_screenheight()
    x = ((sw - 750)/2)
    y = ((sh - 500)/2)
    janela1.geometry("%dx%d+%d+%d" % (750, 500, x, y))
    janela1.resizable(FALSE,FALSE)

    titulo = Label(janela1, text= "Como Jogar?", font= ('Verdana 17 bold')).place(x=280, y=10)
    texto = Label(janela1, text= "Advinhe a palavra em 6 tentativas. Depois de cada tentativa, a cor da", font= ('Verdana 10')).place(x=120, y=60)
    texto = Label(janela1, text= "letra irá mudar para mostrar o quão perto estará o seu palpite da palavra vencedora.", font= ('Verdana 10')).place(x=70, y=80)

    verde = PhotoImage (file = "verde.png")
    verdeLbl = Label(janela1, image = verde).place(x=240, y=130)
    #verdeLbl.image = verde
    texto = Label(janela1, text= "A letra T está presente na palavra e na posição certa.", font= ('Verdana 10')).place(x=180, y=200)

    amarelo = PhotoImage (file = "amarelo.png")
    amareloLbl = Label(janela1, image = amarelo).place(x=240, y=250)
    #amareloLbl.image = amarelo
    texto = Label(janela1, text= "A letra S está presente na palavra mas na posição errada.", font= ('Verdana 10')).place(x=165, y=320)

    cinzento = PhotoImage (file = "cinzento.png")
    cinzentoLbl = Label(janela1, image = cinzento).place(x=240, y=380)
    #cinzentoLbl.image = cinzento
    texto = Label(janela1, text= "A letra E não está presente na palavra.", font= ('Verdana 10')).place(x=225, y=440)


# game window
def game_window():
    global game, frame
    main_window.withdraw()
    game = Toplevel(main_window) # Janela do jogo
    game.title('Wordle Português')
    sw = game.winfo_screenwidth()
    sh = game.winfo_screenheight()
    x = ((sw - 400)/2)
    y = ((sh - 850)/2)
    game.geometry("%dx%d+%d+%d" % (400, 850, x, y))
    game.geometry("450x900")
    game.resizable(FALSE,FALSE)
    icone = PhotoImage (file = "wordle icon.png")
    iconeLbl = Label(game, image = icone).pack(pady=30)
    Label(game, text= "Wordle em Português", font= ('Verdana 17 bold')).pack()
    frame = Frame(game)
    frame.pack(pady=40)
    wordle()
    #game.protocol("WM_DELETE_WINDOW", janela.destroy) # quando o utilizador clica no botão de fechar, chama a função "fechar_jogo"

def close_main_window():
    if messagebox.askokcancel("Sair", "Queres sair?") == True:
        main_window.destroy()


def close_game():
    if messagebox.askokcancel("Sair", "Queres sair do jogo?") == True:
        quit()

# Recolher as palavras do ficheiro
with open('palavras.txt', 'r') as file:
    data = file.readlines()
    for i in data:
        palavras.append(i[:-1])

# Verificar se a tecla pressionada é uma letra ou 'enter'
def key_pressed(event):
    global num_letras, tentativa, tentativa_certa, palavras, nova_linha
    if event.char.isalpha(): # Se a tecla pressionada for uma letra
        if num_letras <= 30 and len(tentativa) < 5: # Se o número de letras for menor ou igual a 30 e o comprimento da tentativa for menor que 5
            update_tentativa(event.char.upper()) # Chamar a função "update_tentativa"
    elif event.keysym == 'Return': # Se a tecla pressionada for 'enter'
        if len(tentativa) < 5: # Se o comprimento da tentativa for menor que 5
            less_than_5()
            tentativa = '' # Repor a variável
        elif tentativa.lower() in palavras: # Se a tentativa estiver na lista
            check_word()
            tentativa = ''
            nova_linha = num_letras
        else:
            go_again()
            tentativa = '' # Repor a variável
        if num_letras == 30:
            win_lose()

# Adiciona a letra ao espaço correspondente
def update_tentativa(char):
    global num_letras, tentativa
    letras[num_letras]['text'] = char
    num_letras += 1
    tentativa += char

# Se a palavra estiver na lista, verificar se é a palavra correta
def check_word():
    global tentativa_certa, termo, tentativa
    btn_index = num_letras - 5
    for i, letra in enumerate(tentativa):
        if letra == termo[i]: # Letra no local correto
            letras[btn_index + i]['bg'] = '#27e512'
            letras[btn_index + i]['activebackground'] = '#27e512' # Mudar a cor do fundo para Verde
        elif letra in termo:
            if tentativa.count(letra) == termo.count(letra): # Letra existente na palavra, mas no local incorreto
                letras[btn_index + i]['bg'] = '#e8ef0e'
                letras[btn_index + i]['activebackground'] = '#e8ef0e' # Mudar a cor do fundo para Amarelo
            else:
                letras[btn_index + i]['bg'] = '#4c4c4c'
                letras[btn_index + i]['activebackground'] = '#4c4c4c' # Mudar a cor do fundo para Cinzento
        else: # Letra inexistente na palavra
            letras[btn_index + i]['bg'] = '#4c4c4c'
            letras[btn_index + i]['activebackground'] = '#4c4c4c' # Mudar a cor do fundo para Cinzento
    if tentativa == termo:
        tentativa_certa = True # A variável 'tentativa_certa' muda de False para True, caso a tentativa esteja certa
        win_lose()

# Se a palavra não constar na lista
def go_again():
    global num_letras
    num_letras -= 5
    for i in range(5):
        letras[num_letras + i]['text'] = ' '
    messagebox.showinfo(title='Atenção', message='Palavra não encontrada')
    game.focus_force()

# Aviso, no caso de a palavra escrita ter menos de 5 letras
def less_than_5():
    global num_letras
    messagebox.showinfo(title='Atenção', message='A palavra tem de ter 5 letras!')
    num_letras -= len(tentativa)
    for i in range(5):
        letras[num_letras + i]['text'] = ' '
    game.focus_force()

# Fim das tentativas, indicação ao jogador se venceu/perdeu o jogo
def win_lose():
    global tentativa_certa, termo, main_window
    if not tentativa_certa:
        title = 'Continua a tentar!'
        message = f'A palavra certa era {termo}'
    else:
        title = 'Bom trabalho!'
        message = 'Parabéns, conseguiste em {} tentativa(s)'.format(int(num_letras / 5))
    play_again = messagebox.askquestion(title = title, message = f'{message}.\nQueres jogar outra vez?')
    if play_again == 'yes':
        wordle() # Voltar a jogar
    else:
        quit()

# Possibilidade de apagar letras
def delete_letter(event):
    global num_letras, tentativa, tentativa_certa, nova_linha
    if num_letras > nova_linha:
        num_letras -= 1
        letras[num_letras]['text'] = ' '
        tentativa = tentativa[:-1]

# Layout da interface
def wordle():
    global frame, num_letras, tentativa_certa, tentativa, termo, game, letras
    frame.destroy()
    frame = Frame(game)
    frame.pack(pady=40)
    letras.clear()
    num_letras = 0
    tentativa_certa = False
    tentativa = ''
    termo = random.choice(palavras).upper()
    print(termo) #para que, de modo a facilitar o jogo, apareça a palavra escolhida na "Shell"
    for linha in range(6): # 6 linhas
        for coluna in range(5): # 5 colunas
            btn = Button(frame, text = ' ', width = 1, bg = 'white', activebackground = 'white', font = 'Verdana, 38')
            btn.grid(row = linha, column = coluna, padx = 3, pady = 5)
            letras.append(btn)
    menu = Menu(game) # Criar um menu
    game.config(menu=menu)
    menu.add_command(label='Novo Jogo', command=wordle) # Opção de jogar outro jogo, com uma nova palavra
    menu.add_command(label='Instruções', command=janela1) # Opção de voltar a ver as instruçõesdf

    game.bind('<Key>', key_pressed) # Chamar a função "key_pressed"
    game.bind('<BackSpace>', delete_letter) # Chamar a função "delete_letter"
    game.bind('<Return>', key_pressed) # #Chamar a função "key_pressed", quando a tecla 'enter' é pressionada

    game.protocol("WM_DELETE_WINDOW", close_game) # quando o utilizador clica no botão de fechar, chama a função "fechar_jogo"
    game.focus_force()
    game.mainloop()

Button(main_window, text="Instruções", font= ('Verdana 10'), command=janela1).place(x=120, y=280)
Button(main_window, text="Começar", font= ('Verdana 10'), command=game_window).place(x=215, y=280)
main_window.protocol("WM_DELETE_WINDOW", close_main_window) # quando o utilizador clica no botão de fechar, chama a função "fechar_janela"
main_window.mainloop()

