import csv
import time

class Game:

    def __init__(self):

        #turn counter
        self.MAX_TURNS = 35

        #needed for running
        self.curNodeID = '0'
        self.nextNodeID = '1'

        #libraries
        self.storyNodes = {}
        self.nextNodes = {}

        #globals
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

    # gets the next story element
    def getNext(self, input=""):
        
        if (self.storyNodes[self.curNodeID]["user_input_needed"] == 'TRUE') :
            # set and check global variables
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

        else:
            # if we are at the chest
            if (self.curNodeID == '5'):
                # set global variables
                self.grabbedDagger = True
                self.grabbedRope = True
                
                print("Items grabbed")
                print("")
            
            self.nextNodeID = self.storyNodes[self.curNodeID]["next_node_ID"]



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

        # catch all so program thows no errors
        if(game.curNodeID not in game.storyNodes):
            print("You died via alligator attack!")
            num_turns = game.MAX_TURNS + 1

        else: # for when the code works as intented

            print(game.storyNodes[game.curNodeID]["output"])
            print("")

            # give player enough time to read
            time.sleep(2.5)

            #grab user input
            if(game.storyNodes[game.curNodeID]["user_input_needed"] == 'TRUE' and game.curNodeID != '242') :
                inputValid = False
                userInput = ""
                while(not inputValid):

                    userInput = input("> ")
                    print("")

                    # try user input
                    try:
                        game.getNext(userInput)
                    except: 
                        print("I really didn't get that. Try again!")
                        print("")
                    else:
                        inputValid = True


            else:
                game.getNext()

            game.curNodeID = game.nextNodeID

            num_turns += 1


    #######################################
    # CASE 1: MADE TOO MANY BAD DECISIONS #
    #######################################
    if(num_turns == game.MAX_TURNS) :
        print("You took too long trying to escape and the fire has gotten to you!")

    ###################################
    # CASE 2: WENT DOWN A DEATH ROUTE #
    ###################################
    if(game.nextNodeID == 'X'):
        print("You've died!")

    #############################
    # CASE 3: MADE IT TO SAFETY #
    #############################
    if(game.nextNodeID == ":)"):
        print("You have successfully escaped from the burning castle!")
        print("")
        print("You win!")


    return 0


if __name__ == '__main__':
    main()