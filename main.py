import csv
import time

class Game:

    def __init__(self):

        #game variables
        self.MAX_TURNS = 30
        self.player_name = ""

        #needed for running
        self.curNodeID = '0'
        self.nextNodeID = '1'

        self.storyNodes = {}
        self.nextNodes = {}

        self.grabbedDagger = False
        self.grabbedRope = False
        self.wearingArmor = False


        # load and process storyNodes
        with open('storyData/storyNodes.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                self.storyNodes[row["node_ID"]] = {
                    "output": row["output"],
                    "user_input_needed": row["user_input_needed"],
                    "next_node_ID": row["next_node_ID"]
                }
                line_count += 1

        # load and process nextNodes
        with open('storyData/nextNodes.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                
                if (row["node_ID"] not in self.nextNodes):
                    self.nextNodes[row["node_ID"]] = {
                        row["resp_option"]: row["next_node_ID"]
                    }
                else:
                    self.nextNodes[row["node_ID"]].update({
                        row["resp_option"]: row["next_node_ID"]
                    })    
                
                line_count += 1

    def getNext(self, input=""):
        
        if (self.storyNodes[self.curNodeID]["user_input_needed"] == 'TRUE') :

            if (self.curNodeID == '203' and input == 'yes'):
                self.wearingArmor = True
                self.nextNodeID = self.nextNodes[self.curNodeID][input]
            elif(self.curNodeID == '242' and self.wearingArmor and self.grabbedDagger):
                self.nextNodeID = '250'
            elif(self.curNodeID == '242' and self.wearingArmor and not self.grabbedDagger):
                self.nextNodeID = '260'
            elif(self.curNodeID == '242' and not self.wearingArmor):
                self.nextNodeID = '270'
            else:
                self.nextNodeID = self.nextNodes[self.curNodeID][input]

            #self.nextNodeID = self.nextNodes[self.curNodeID][input]
        else:
            if (self.curNodeID == '5'):
                self.grabbedDagger = True
                self.grabbedRope = True
                #print("")
                print("Items grabbed")
                print("")
            
            self.nextNodeID = self.storyNodes[self.curNodeID]["next_node_ID"]

        #return 'X'


def main():

    game = Game()

    num_turns = 0

    print("")
    print("******************************************************")
    print("*                                                    *")
    print("*    Welcome to our very own text-based adventure    *")
    print("*              game inspired by Advent!              *")
    print("*                                                    *")
    print("*           The authors of this game are:            *")
    print("*     Oscar Dong, Kelsey Recinas, and Aileen Wu      *")
    print("*                                                    *")
    print("*      Your mission, should you choose to accept,    *")
    print("*    is to escape from your burning castle before    *")
    print("*      the flames have a chance to consume you!      *")
    print("*                                                    *")
    print("******************************************************")
    print("")


    while (num_turns < game.MAX_TURNS and game.nextNodeID != 'X' and game.nextNodeID != ':)') :

        # do stuff with curNode

        if(game.curNodeID not in game.storyNodes):
            print("You died via alligator attack!")
            num_turns = game.MAX_TURNS + 1
        else:

            print(game.storyNodes[game.curNodeID]["output"])
            print("")
            time.sleep(0.5)

            #grab user input
            if(game.storyNodes[game.curNodeID]["user_input_needed"] == 'TRUE' and game.curNodeID != '242') :
                inputValid = False
                userInput = ""
                while(not inputValid):

                    userInput = input("> ")
                    print("")
                    #print(userInput)
                    #print(game.curNodeID)

                    try:
                        #game.nextNodeID = game.nextNodes[game.curNodeID][userInput]
                        game.getNext(userInput)
                    except: 
                        print("I really didn't get that. Try again!")
                        print("")
                    else:
                        inputValid = True

                #game.nextNodeID = game.nextNodes[game.curNodeID][userInput]

            else:
                #game.nextNodeID = game.storyNodes[game.curNodeID]["next_node_ID"]
                game.getNext()

            game.curNodeID = game.nextNodeID

            num_turns += 1

    if(num_turns == game.MAX_TURNS) :
        print("You took too long trying to escape and the fire has gotten to you!")

    
    if(game.nextNodeID == 'X'):
        print("You've died!")

    if(game.nextNodeID == ":)"):
        print("You have successfully escaped from the burning castle!")
        print("")
        print("You win!")


    return 0


if __name__ == '__main__':
    main()