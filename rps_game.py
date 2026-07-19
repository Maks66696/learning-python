import random

CHOICES = ['камень', 'ножницы', 'бумага']

def get_computer_choice():
    computer_choice=random.choice(CHOICES)
    return computer_choice

def get_player_choice():
    player_choice = input("Введите ваш выбор: ")
    return player_choice.lower()

def get_round_winner (computer, player):
        if (player == computer ):
            return "ничья"
        elif (player=="ножницы" and computer=="бумага" 
            or player=="камень" and computer=="ножницы" 
            or player=="бумага" and computer=="камень"):
            return "игрок"
        else:
             return "компьютер"
        
player_score=0
computer_score=0

while player_score < 3 and computer_score < 3:
    print(f"\nТекущий счет — Вы: {player_score} | Компьютер: {computer_score}")
    p_move=get_player_choice()
    c_move=get_computer_choice()
    print(f"Компьютер выбрал: {c_move}")
    result=get_round_winner(c_move,p_move)

    if result == "компьютер":
        print("Компьютер выиграл")
        computer_score += 1

    elif result == "игрок":
        print("Игрок выиграл")
        player_score +=1
    else:
        print("Ничья")
           
    if player_score == 3:
        print("Игрок выиграл раунд")
        break
    elif computer_score==3:
         print("Компьютер выиграл раунд")
         break
        

    
    

    


            
            
            

   



