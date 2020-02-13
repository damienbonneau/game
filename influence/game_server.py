from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

player1 = Player("Arm",(0.3,0.3,1.0))
player2 = Player("Max",(1.0,0.3,0.3))

class GameServer(LineReceiver):
    def __init__(self, players,listplayers,board):
        self.players = players
        self.listplayers = listplayers
        self.player = None
        self.currentplayer= None
        self.board = board
        #self.state = "GETBOARD"
        self.state = "WAITPLAYER"

    def connectionMade(self):
        self.sendLine("GET PLAYER %d" % len(self.players.keys()) )

    def connectionLost(self, reason):
        if self.player ==None:
            return
        if self.players.has_key(self.player.id):
            print "Player %s has been deconnected\n" % self.player.name
            #del self.players[self.name]

    def setBoard(self,board):
        self.board = board

    def lineReceived(self, line):
        print "'%s' <%s>" % (line,self.state)
        if self.state == "WAITPLAYER":
            if line.startswith("PLAYER"):
                p = createPlayerFromPacket(line)
                self.players[p.id] = self
                self.listplayers.append(p)
                self.name= p.name
                self.player = p
                print "Hello %s" % self.name
                self.state = "WAITHOTHERS"

        for cid,client in  self.players.items():
            if client.state == "PLAY":
                self.handle_PLAY(client,line)

        if len(self.players.keys()) == 2 and self.state == "WAITHOTHERS":
            # For now, generate a fixed battle field:
            print self.listplayers
            self.board = BoardServer(30,30,self.listplayers)
            print "Generating landscape..."

            self.board.gene_board()
            self.board.add_unit(Tank(self.listplayers[1]),(8,5))
            self.board.add_unit(SpaceMarine(self.listplayers[1]),(8,6))
            self.board.add_unit(Tank(self.listplayers[1]),(5,5))
            self.board.add_unit(Tank(self.listplayers[0]),(5,6))
            self.board.add_unit(Tank(self.listplayers[0]),(5,12))
            for client in self.players.values():
                client.sendLine("INIT GAME")

            for client in self.players.values():
                for p in self.listplayers:
                    client.sendLine(p.packet)
                client.sendLine("CURRPLAYER 0")
                # Send the board to the players (TODO: make each client load the board from a file)
                # For now, the board is sent from the server to the clients
                client.sendLine("BOARD,%d,%d" % (self.board.width,self.board.height))
                for bloc in self.board.blocs.values():
                    if bloc.name != "space":
                        client.sendLine(bloc.packet)

                for u in self.board.units.values():
                    client.sendLine(u.packet)
                
                client.sendLine("LAUNCH GAME")
                client.state = "PLAY"

    def handle_PLAY(self,client,line):
        # Broadcast the actions done by every player
        client.sendLine(line)

            #if line.startswith("MOVE"):
            #    pass
            #if line.startswith("ATTACK"):
            #    pass

    def endTurn(self):
        nbplayers = len(self.players)
        self.currplayernumber = (self.currplayernumber+1) % nbplayers
        self.currentplayer = self.players[self.currplayernumber]
        self.board.newTurn(self.currentplayer)

class GameFactory(Factory):
    def __init__(self):
        self.players = {} # maps user names to Game instances
        self.listplayers = [] # list of players
        self.board = None

    def buildProtocol(self, addr):
        return GameServer(self.players,self.listplayers,self.board)


if __name__ == '__main__':
    reactor.listenTCP(8123, GameFactory())
    print "Game server is up"
    reactor.run()
