# -*- coding: utf8 -*-
#
# INFO-F106 - Projet d'année - Partie 4
#
# GÉRARD Pierre  000379259


from tkinter import *
from tkinter import messagebox, filedialog
from draughtsFunctions import *
from draughts import *


class BoardGUI():
    """Gère l'interface graphique du damier"""
    def __init__(self, masterFrame):
        """Intilialise les variables de l'interface graphique """
        # ---init game et gui var ---
        self.masterFrame = masterFrame
        self.draughtsMain = Draughts(PLAYER_VS_PLAYER)
        self.boardDimension = self.draughtsMain.getDimension()
        self.pawnPerPlayer = self.boardDimension * 2
        self.mainCanDim = 500
        self.currentPlayerCanvasHeight = 25
        self.boardOutlineDim = 15
        self.boardCaptWidth = 125
        self.squareDimension = self.mainCanDim / self.boardDimension
        self.pawnPading = 5 * self.squareDimension / 50
        self.pawnWidth = 2
        self.textSize = "16"
        self.padXBoard = 8
        self.padYBoard = 5
        self.PadXButton = 2
        self.PadYButton = 5
        # choose mode
        self.choiceMode = IntVar()
        self.choiceMode.set(0)
        # --- make Frame ----
        self.makeButtonFrame()
        self.makeBoardFrame()
        #  ---- Selection/binding ------
        self.selectedPawn = False
        self.selectedKing = False
        self.boardCanvas.bind("<Button-1>", self.clickMouse)
        # ----- Welcome message ---------
        messagebox.showinfo("Welcome","Welcome to Draughts \nBy default you're playing against an other player, click on new game to start a new game in an other mode \nHave fun!")

    def makeBoardFrame(self):
        """ Intilialise la frame contenant le damier et son contour,le joueur 
        actuel et le nombre de capture effectué et arrange ses élements avec 
        grid """
        self.boardFrame = Frame(self.masterFrame)  # 4 row - 5 column
        # ---- Current player label : ----
        self.currentPlayerLabel = Label(self.boardFrame, text="", font=self.textSize)
        self.currentPlayerLabel.grid(row=0, column=2, padx=self.padXBoard, pady=self.padYBoard)
        # ---- Outine canvas -----
        # Les canvas sont plus facile a utilisé dans ce cas la que Label car
        # il permette facilement d'aligné le texte au centre d'une case de
        # même largeur que un carré
        self.boardOutlineHorizontalTop = Canvas(self.boardFrame, height=self.boardOutlineDim, width=self.mainCanDim)
        self.boardOutlineHorizontalTop.grid(row=1, column=2)
        self.boardOutlineHorizontalDown = Canvas(self.boardFrame, height=self.boardOutlineDim, width=self.mainCanDim)
        self.boardOutlineHorizontalDown.grid(row=3, column=2)
        self.boardOutlineHVeritcalLeft = Canvas(self.boardFrame, height=self.mainCanDim, width=self.boardOutlineDim)
        self.boardOutlineHVeritcalLeft.grid(row=2, column=1)
        self.boardOutlineHVerticalRight = Canvas(self.boardFrame, height=self.mainCanDim, width=self.boardOutlineDim)
        self.boardOutlineHVerticalRight.grid(row=2, column=3)
        # ---- Capture label -----
        self.whiteCaptLabel = Label(self.boardFrame, text="", font=self.textSize, bg="grey")
        self.whiteCaptLabel.grid(row=2, column=0, sticky="N", padx=self.padXBoard, pady=self.padYBoard)
        self.blackCaptLabel = Label(self.boardFrame, text="", font=self.textSize, bg="grey")
        self.blackCaptLabel.grid(row=2, column=4, sticky="N", padx=self.padXBoard, pady=self.padYBoard)
        # --- Création Canvas---
        self.boardCanvas = Canvas(self.boardFrame, height=self.mainCanDim, width=self.mainCanDim, bg="white")
        self.boardCanvas.grid(row=2, column=2)

         # Creation black square(ne change jamais) :
        for row in range(self.boardDimension):
            for col in range(self.boardDimension):
                if (row + col) % 2 == 1:
                    topleftX = col * self.squareDimension
                    topleftY = row * self.squareDimension
                    self.boardCanvas.create_rectangle(topleftX, topleftY, topleftX + self.squareDimension, topleftY +
                                                      self.squareDimension, fill="black", tags="staticSquare")

        self.updateBoardFrame()
        # --- grid ---
        self.boardFrame.grid(row=0)

    def makeButtonFrame(self):
        """ Intilialise la frame contenant les bouttons et arrange ses élements
        avec grid """
        # ---- init frame ---
        self.buttonFrame = Frame(self.masterFrame)
        # --- init button ---
        self.newGame = Button(self.buttonFrame, text="New game", command=self.newGame)
        self.newGame.grid(row=0, column=0, padx=self.PadXButton, pady=self.PadYButton)
        self.loadGame = Button(self.buttonFrame, text="Load game", command=self.loadFile)
        self.loadGame.grid(row=0, column=1, padx=self.PadXButton, pady=self.PadYButton)
        self.saveGame = Button(self.buttonFrame, text="Save game", command=self.saveFile)
        self.saveGame.grid(row=0, column=2, padx=self.PadXButton, pady=self.PadYButton)
        self.help = Button(self.buttonFrame, text="Help", command=self.displayHelp)
        self.help.grid(row=0, column=3, padx=self.PadXButton, pady=self.PadYButton)
        # --- grid ----
        self.buttonFrame.grid(row=1)

    def updateBoardOutline(self):
        """ Permet de mettre à jour les chiffre/lettres correspondant au case 
        autour du damier"""
        self.boardOutlineHorizontalTop.delete(ALL)
        self.boardOutlineHorizontalDown.delete(ALL)
        self.boardOutlineHVeritcalLeft.delete(ALL)
        self.boardOutlineHVerticalRight.delete(ALL)
        if self.draughtsMain.getPlayer() == WHITE_PLAYER:
            order = range(self.boardDimension)
        else:
            order = range(self.boardDimension - 1, -1, -1)
        j = 0
        for i in order:
            self.boardOutlineHorizontalTop.create_text(
                j * self.squareDimension + self.squareDimension // 2, self.boardOutlineDim // 2, text=chr(i + ord("a")))
            self.boardOutlineHorizontalDown.create_text(
                j * self.squareDimension + self.squareDimension // 2, self.boardOutlineDim // 2, text=chr(i + ord("a")))

            self.boardOutlineHVeritcalLeft.create_text(
                self.boardOutlineDim // 2, j * self.squareDimension + self.squareDimension // 2, text=str(i + 1))

            self.boardOutlineHVerticalRight.create_text(
                self.boardOutlineDim // 2, j * self.squareDimension + self.squareDimension // 2, text=str(i + 1))
            j += 1

    def resetSelection(self):
        """ Déselectionne le pion """
        self.selectedPawn = False
        self.selectedKing = False

    def updateCapture(self):
        """ Permet d'écrire les captures effectués par les joueurs"""
        self.numberOfWhiteCapt = self.pawnPerPlayer
        self.numberOfBlackCapt = self.pawnPerPlayer
        for row in self.draughtsMain.getBoard():
            for col in row:
                if col <= BLACK_PLAYER:
                    self.numberOfWhiteCapt -= 1
                if col >= WHITE_PLAYER:
                    self.numberOfBlackCapt -= 1
        if self.numberOfWhiteCapt > 0:
            self.whiteCaptLabel.config(text="White captures : \n\n {0}".format(self.numberOfWhiteCapt))
        else:
            self.whiteCaptLabel.config(text="White captures :")
        if self.numberOfBlackCapt > 0:
            self.blackCaptLabel.config(text="Black captures : \n\n {0}".format(self.numberOfBlackCapt))
        else:
            self.blackCaptLabel.config(text="Black captures :")

    def updateCurrentPlayer(self):
        """Permet de mettre a jour le joueur actuel"""
        if self.draughtsMain.getMode() == PLAYER_VS_PLAYER:
            self.currentPlayerLabel.config(text="Current player : {0} (pvp)".format(nameOf(self.draughtsMain.getPlayer())))
        else:
            self.currentPlayerLabel.config(text="{0} vs Computer".format(nameOf(self.draughtsMain.getPlayer()).capitalize()))

    def updateBoardFrame(self):
        """Met à jour l'affichage du damier et des widgets liés"""
        self.updateCurrentPlayer()
        self.updateBoardOutline()
        self.updateCapture()
        board = self.draughtsMain.getBoard()
        for pawn in self.boardCanvas.find_withtag("white"):
            self.boardCanvas.delete(pawn)
        for pawn in self.boardCanvas.find_withtag("black"):
            self.boardCanvas.delete(pawn)
        if self.draughtsMain.getPlayer() == WHITE_PLAYER:
            order = range(self.boardDimension)
        else:
            order = range(self.boardDimension - 1, -1, -1)
        rowCounter = 0
        for row in order:
            colCounter = 0
            for col in order:
                topleftX = colCounter * self.squareDimension
                topleftY = rowCounter * self.squareDimension
                if board[row][col] != 0:
                    if board[row][col] / abs(board[row][col]) == WHITE_PLAYER:
                        if isKing(board, row, col):
                            crown = (topleftX + 10 * self.squareDimension / 50, topleftY + 15 * self.squareDimension / 50, topleftX + 18 * self.squareDimension / 50, topleftY + 22 * self.squareDimension / 50, topleftX + 25 * self.squareDimension / 50, topleftY + 12 * self.squareDimension / 50, topleftX + 32 * self.squareDimension / 50, topleftY + 22 * self.squareDimension / 50, topleftX + 40 * self.squareDimension / 50, topleftY +
                                     15 * self.squareDimension / 50, topleftX + 35 * self.squareDimension / 50, topleftY + 35 * self.squareDimension / 50, topleftX + 15 * self.squareDimension / 50, topleftY + 35 * self.squareDimension / 50)
                            pawnId = self.boardCanvas.create_oval(topleftX + self.pawnPading, topleftY + self.pawnPading, topleftX + self.squareDimension - self.pawnPading, topleftY +
                                                                  self.squareDimension - self.pawnPading, outline="grey", fill="white", width=self.pawnWidth)
                            crownId = self.boardCanvas.create_polygon(crown, fill='yellow', tags="white")
                            self.boardCanvas.itemconfig(crownId, tags=("white", "king", "crown", pawnId))
                            self.boardCanvas.itemconfig(pawnId, tags=("white", "king", "pawn", crownId))
                        else:
                            self.boardCanvas.create_oval(topleftX + self.pawnPading, topleftY + self.pawnPading, topleftX + self.squareDimension - self.pawnPading, topleftY + self.squareDimension -
                                                         self.pawnPading, outline="grey", fill="white", width=self.pawnWidth, tags="white")
                    else:
                        if isKing(board, row, col):
                            crown = (topleftX + 10 * self.squareDimension / 50, topleftY + 15 * self.squareDimension / 50, topleftX + 18 * self.squareDimension / 50, topleftY + 22 * self.squareDimension / 50, topleftX + 25 * self.squareDimension / 50, topleftY + 12 * self.squareDimension / 50, topleftX + 32 * self.squareDimension / 50, topleftY + 22 * self.squareDimension / 50, topleftX + 40 * self.squareDimension / 50, topleftY +
                                     15 * self.squareDimension / 50, topleftX + 35 * self.squareDimension / 50, topleftY + 35 * self.squareDimension / 50, topleftX + 15 * self.squareDimension / 50, topleftY + 35 * self.squareDimension / 50)
                            pawnId = self.boardCanvas.create_oval(topleftX + self.pawnPading, topleftY + self.pawnPading, topleftX + self.squareDimension - self.pawnPading, topleftY +
                                                                  self.squareDimension - self.pawnPading, outline="grey", fill="black", width=self.pawnWidth)
                            crownId = self.boardCanvas.create_polygon(crown, fill='yellow', tags="black")
                            self.boardCanvas.itemconfig(crownId, tags=("black", "king", "crown", pawnId))
                            self.boardCanvas.itemconfig(pawnId, tags=("black", "king", "pawn", crownId))
                        else:
                            self.boardCanvas.create_oval(topleftX + self.pawnPading, topleftY + self.pawnPading, topleftX + self.squareDimension - self.pawnPading, topleftY + self.squareDimension -
                                                         self.pawnPading, outline="grey", fill="black", width=self.pawnWidth, tags="black")
                colCounter += 1
            rowCounter += 1
        # Remise du fond vert sur le pion selectionné :
        played = self.draughtsMain.getPlayed()
        if played:
            x, y = self.revertConvertToBoard(played[1], played[0])
            y = y + self.pawnPading * 3
            x = x + self.pawnPading * 3
            self.selectedPawn = self.boardCanvas.find_closest(x, y)
            self.boardCanvas.itemconfig(self.selectedPawn, fill="green")

        if not (isinstance(self.draughtsMain.getFinished(), bool)):
            self.messageWinner()

    def convertDirectionLenght(self):
        """ Permet d'obtenir la direction et la longueur du déplacement """
        if self.draughtsMain.getPlayer() == WHITE_PLAYER:
            if self.x1 > self.x3 and self.y1 < self.y3:
                self.direction = "LB"
            elif self.x1 < self.x3 and self.y1 < self.y3:
                self.direction = "RB"
            elif self.x1 > self.x3 and self.y1 > self.y3:
                self.direction = "L"
            elif self.x1 < self.x3 and self.y1 > self.y3:
                self.direction = "R"
            self.lenght = abs(self.x1 - self.x3)
        else:
            if self.x1 > self.x3 and self.y1 < self.y3:
                self.direction = "R"
            elif self.x1 < self.x3 and self.y1 < self.y3:
                self.direction = "L"
            elif self.x1 > self.x3 and self.y1 > self.y3:
                self.direction = "RB"
            elif self.x1 < self.x3 and self.y1 > self.y3:
                self.direction = "LB"
            self.lenght = abs(self.x1 - self.x3)

    def convertToBoard(self, x, y):
        """ convertit les position sur le canvas en position sur le damier """
        x, y = int(x // self.squareDimension), int(y // self.squareDimension)
        if self.draughtsMain.getPlayer() == BLACK_PLAYER:
            y = abs(y - self.boardDimension + 1)  # Symétrie
            x = abs(x - self.boardDimension + 1)
        return x, y

    def revertConvertToBoard(self, x, y):
        """ convertit les positions sur le damier en positions sur le canvas """
        if self.draughtsMain.getPlayer() == BLACK_PLAYER:
            y = abs(y - self.boardDimension + 1)
            x = abs(x - self.boardDimension + 1)
        return x * self.squareDimension, y * self.squareDimension

    def clickMouse(self, event):
        """Gère les clicks:
        - Premier click : Selectionne un pion si il y en a un là ou l'utilisateur
             click et le modifie pour changer son fond en vert
        - Deuxième click : C'est celui qui effectue le mouvement après avoir 
            convertie les coordonnées et ou si l'utilisateur click sur le même 
           pion finit son tour"""
        if not self.selectedPawn:
            self.x1, self.y1 = event.x, event.y
            self.selectedPawn = self.boardCanvas.find_closest(self.x1, self.y1)
            if nameOf(self.draughtsMain.getPlayer()) in self.boardCanvas.gettags(self.selectedPawn):
                if "king" in self.boardCanvas.gettags(self.selectedPawn):
                    self.selectedKing = self.boardCanvas.gettags(self.selectedPawn)[3]  #edit
                    if "crown" in self.boardCanvas.gettags(self.selectedPawn):
                        self.selectedKing, self.selectedPawn = self.selectedPawn, self.selectedKing
                else:
                    self.selectedKing = False
                self.boardCanvas.itemconfig(self.selectedPawn, fill="green")
                self.boardCanvas.lift(self.selectedPawn)
                if self.selectedKing:
                    self.boardCanvas.lift(self.selectedKing)
                self.x1, self.y1 = self.convertToBoard(self.x1, self.y1)

            else:
                self.resetSelection()
        else:
            self.x3, self.y3 = event.x, event.y
            self.x3, self.y3 = self.convertToBoard(self.x3, self.y3)
            moveStr = "({0},{1}) -> ({2},{3})".format(chr(self.x1 + ord("a")), self.y1 + 1, chr(self.x3 + ord("a")), self.y3 + 1)
            if (self.x1, self.y1) == (self.x3, self.y3):
                result = self.draughtsMain.askEndOfTurn()
                self.resetSelection()
                self.updateBoardFrame()
            elif abs(self.x1 - self.x3) != abs(self.y1 - self.y3):
                messagebox.showerror("Move error", "The move {0} is not correct : Only diagonal move are allowed\n(Click on help for more information)".format(moveStr))
            else:
                self.convertDirectionLenght()
                error = self.draughtsMain.makeMove(self.y1, self.x1, self.direction, self.lenght)
                if error != NO_ERROR:
                    messagebox.showerror("Move error", "The movement {0} is not allowed :  \n {1}\n(Click on help for more information)".format(moveStr, strerr(error).capitalize()))
                    self.resetSelection()
                else:
                    played = self.draughtsMain.getPlayed()
                    self.y1, self.x1 = played
                self.updateBoardFrame()

    def messageWinner(self):
        """ Affiche le gagnant à la fin du jeu dans une fenètre d'info """
        self.resetSelection()
        for pawn in self.boardCanvas.find_withtag("white"):
            self.boardCanvas.delete(pawn)
        for pawn in self.boardCanvas.find_withtag("black"):
            self.boardCanvas.delete(pawn)
        self.boardCanvas.create_text(self.mainCanDim // 2, self.mainCanDim // 2 - 20, text="End of game : {0}".format(
            self.draughtsMain.sayWinner()), fill="red", font=self.textSize, tags=("white", "black"))

    def makeNewGame(self):
        self.draughtsMain.__init__(int(self.choiceMode.get()))
        self.resetSelection()
        self.updateBoardFrame()
        self.newGameTop.destroy()

    def newGame(self):
        """Permet à l'utilisateur de créer un nouveau jeu (demande une confirmation"""
        self.newGameTop = Toplevel(self.masterFrame)
        self.newGameTop.title("New Game ...")
        label0 = Label(self.newGameTop, text="Please choose your game mode")
        label0.grid(row=0,columnspan=2)
        option1 = Radiobutton(self.newGameTop, text="Player vs Player",variable=self.choiceMode, value=0)
        option1.grid(row=1,columnspan=2)
        option2 = Radiobutton(self.newGameTop, text="Player vs Computer (black)",variable=self.choiceMode, value=-1)
        option2.grid(row=2,columnspan=2)
        option3 = Radiobutton(self.newGameTop, text="Player vs Computer (white)", variable=self.choiceMode, value=1)
        option3.grid(row=3,columnspan=2)
        buttonOk = Button(self.newGameTop, text="Play", command=self.makeNewGame)
        buttonOk.grid(row=4,column=0)
        buttonCancel = Button(self.newGameTop, text="Cancel", command=self.newGameTop.destroy)
        buttonCancel.grid(row=4,column=1)

    def loadFile(self):
        """Crée un popup permettant à l'utilisateur de charger un damier"""
        fileLoaded = filedialog.askopenfilename(title='Load', filetypes=[('Data File', '.dat')])
        if fileLoaded != "":
            try:
                player,mode, board = load(fileLoaded)
                self.draughtsMain.setBoard(board)
                self.draughtsMain.setPlayer(player)
                self.draughtsMain.setMode(mode)
                self.resetSelection()
                self.updateBoardFrame()
                messagebox.showinfo("Load File", "File loaded with success")
            except IOError:
                messagebox.showerror("File Error", "Cannot open the file : IOError")
            except ValueError:
                messagebox.showerror("File Error", "Cannot open the file : Invalid File")
            except:
                messagebox.showerror("File Error", "Cannot open the file : Unexpected error")

    def saveFile(self):
        """Crée un popup permettant à l'utilisateur de sauver le jeu"""
        if self.selectedPawn:
        # Si le joueur a fait un déplacement sans indiquer qu'il a terminer son
        # tour, sauvegarder lui permetterait de re-effectuer un déplacement
        # au chargement
            messagebox.showerror("Save Error", "You can't save the game in the middle of your turn, please finish your turn first.")
        else:
            fileLoaded = filedialog.asksaveasfilename(title='Save', filetypes=[('Data File', '.dat')])
            if fileLoaded != "":
                try:
                    save(fileLoaded, self.draughtsMain.getBoard(), self.draughtsMain.getPlayer(), self.draughtsMain.getMode())
                    messagebox.showinfo("Save File", "File saved with success")
                except IOError:
                    messagebox.showerror("File Error", "Cannot open the file : IOError")

    def displayHelp(self):
        """Créer un popup affichant l'aide"""
        helpMessage = ("Rules : \nThe rules can be find on the following " +
        "website : http://www.ffjd.fr/Web/ \n However there is severale " +
        "modification of the rules : Capture or maximum capture are not " +
        "forced \n How to play: \nFirst, click on the pawn you want to play " +
        "with then click on the destination of the pawn or the pawn you want" +
        " to capture.Finally click on the pawn you played with to " +
        "terminate your turn")
        messagebox.showinfo("Help", helpMessage)


def main():
    """Création du jeu et de la boucle d'attente """
    root = Tk()
    root.title("Draughts")
    gui = BoardGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
