import random

SUITS = ["Clubs", "Diamonds", "Hearts", "Spades"]


class Game:
    def __init__(self):
        self.cards = []
        for num in range(1, 14):
            for suit in SUITS:
                card = Card(num, suit)
                self.cards.append(card)

    def start(self):
        random.shuffle(self.cards)
        self.index = 0

    def give_card(self, humans):
        for human in humans:
            card = self.cards[self.index]
            human.get_card(card)

            self.index += 1


    def play_once(self, player, dealer):
        # set bet money
        while True:
            bet_money = input("How much would you like to bet? You currently have $%s: " % player.money)
            if bet_money.isdigit():
                bet_money = int(bet_money)
                if 0 < bet_money <= player.money:
                    break
                print("Invalid num.")
            else:
                print("Invalid input.")

        # first deal
        self.start()
        print("\ndealing...")
        self.give_card([dealer, player])
        self.give_card([dealer, player])

        player.show()
        dealer.hidden_show()

        # check black jack
        if player.get_nums() == 21:
            print("You are black jack.")
            print("You win. You gain double $%s" % bet_money)
            player.change_money(bet_money * 2)

            player.show()
            dealer.show()

            player.show_money()
            return

        # hit or stand
        while True:
            # check bust
            if player.get_nums() > 21:
                print("You bust.")
                print("Dealer wins. You lose $%s" % bet_money)
                player.change_money(-bet_money)

                player.show()
                dealer.show()

                player.show_money()
                break

            if dealer.get_nums() > 21:
                print("Dealer bust.")
                print("You win. You gain $%s" % bet_money)
                player.change_money(bet_money)

                player.show()
                dealer.show()

                player.show_money()
                break

            choice = input("Would you like to hit/stand?")
            choice = choice.lower()
            if choice == "s" or choice == "stand":
                player_nums = player.get_nums()
                dealer_nums = dealer.get_nums()

                if player_nums > dealer_nums:
                    print("You win. You gain $%s" % bet_money)
                    player.change_money(bet_money)
                elif player_nums == dealer_nums:
                    print("Draw.No lose no gain")  # 平局，钱不变
                else:
                    print("Dealer wins. You lose $%s" % bet_money)
                    player.change_money(-bet_money)

                player.show()
                dealer.show()

                player.show_money()
                break

            elif choice == "h" or choice == "hit":
                print("hitting...")
                self.give_card([dealer, player])

                player.show()
                dealer.hidden_show()
                # 游戏未结束，继续循环
            else:
                print("Invalid input.")


class Card:
    def __init__(self, num, suit):
        self.num = num
        self.suit = suit

    def __str__(self):
        return "%s of %s" % (self.num, self.suit)


class Human:
    def __init__(self):
        self.cards = []

    def get_card(self, card):
        self.cards.append(card)

    def get_nums(self):  # 计算所有牌的总点数
        nums = 0
        for card in self.cards:
            nums += card.num
        return nums


class Dealer(Human):
    def hidden_show(self):
        s = "Dealer's cards: "
        s += str(self.cards[0])
        s += ", "

        s += "HIDDEN"

        print(s)

    def show(self): # stand 
        s = "Dealer's cards: "
        for card in self.cards:
            s += str(card)
            s += ", "

        s += " - %s" % self.get_nums()
        print(s)


class Player(Human):
    def __init__(self, money):
        super().__init__()
        self.money = money

    def change_money(self, change):
        self.money += change

    def show_money(self):
        print("Player currently has $%s" % self.money)

    def show(self):
        s = "Player's cards: "
        for card in self.cards:
            s += str(card)
            s += ", "

        s += " - %s" % self.get_nums()
        print(s)


def main():
    print("Welcome to play Black Jack!")

    # set player money
    while True:
        money = input("How much money do you have?")
        if money.isdigit():
            money = int(money)
            break
        else:
            print("Invalid input.")

    game = Game()
    dealer = Dealer()
    player = Player(money)

    game.play_once(player, dealer)

    # ask play again
    while True:
        if player.money == 0:
            while True:
                add_money = input("Would you like to add more money?(y/n)")
                if add_money == "y":
                    break 
                elif add_money == "n":
                    print("GoodBye.")
                    return 
                else:
                    print("Invalid input.")

            while True:
                money = input("How much money do you want to add?")
                if money.isdigit():
                    money = int(money)
                    player.change_money(money)
                    break
                else:
                    print("Invalid input.")

        again = input("\nWould you like to play again? y/n: ")
        if again == "y":
            # reset data
            game.start()
            player.cards = []
            dealer.cards = []

            game.play_once(player, dealer)
        elif again == "n":
            print("Bye")
            break
        else:
            print("Invalid input.")


main()