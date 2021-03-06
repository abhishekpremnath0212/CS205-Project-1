
import itertools
import collections
goals=[[1,2,3],[4,5,6],[7,8,0]]
class Node:#Node represent any tile that is to be solved
    def __init__(self, puzzle, dmetric, parent=None, action=None, ):
        self.puzzle = puzzle
        self.parent = parent
        self.action = action
        self.distanceMetric = dmetric
        if (self.parent != None):
            self.g = parent.g + 1
        else:
            self.g = 0

    @property
    def score(self):#calculating f(n)
        return (self.g + self.h)

    @property
    def state(self):#returing a string representation of itself
        return str(self)

    @property 
    def path(self):#root to parent path
        node, p = self, []
        while node:
            p.append(node)
            node = node.parent
        yield from reversed(p)#using list iterator instead of a single return statement

    @property
    def solved(self): #checking to see if goal state is achieved
        """ Wrapper to check if 'puzzle' is solved """
        return self.puzzle.solved

    @property
    def actions(self): #checking for possible actions
      return self.puzzle.actions

    @property
    def h(self):
        """"h"""
        if self.distanceMetric == "manhattan":
          return self.puzzle.manhattan
        elif self.distanceMetric == "misplaced":
          return self.puzzle.misplaced
        elif self.distanceMetric == "uninformed":
          return self.puzzle.uninformed

    @property
    def f(self):
        """"f"""
        return self.h + self.g

    def __str__(self):
        return str(self.puzzle)

class Solver:
    def __init__(self, start, dmetric="manhattan"):
        self.start = start
        self.dmetric = dmetric

    def solve(self):#solve helper function
        queue = collections.deque([Node(self.start, self.dmetric)])
        seen = set()
        seen.add(queue[0].state)
        while queue:
            queue = collections.deque(sorted(list(queue), key=lambda node: node.f))
            node = queue.popleft()
            if node.solved:
                return node.path

            for move, action in node.actions:
                child = Node(move(), self.dmetric, node, action)

                if child.state not in seen:
                    queue.appendleft(child)
                    seen.add(child.state)

class Puzzle:
    def __init__(self, board):#declaring dimensions of the board. Can be easily chaned for the 15 tile piuzzle
        self.width = len(board[0])
        self.board = board

    @property
    def solved(self):
        N = self.width * self.width
        return str(self) == ''.join(map(str, range(1,N))) + '0'

    @property 
    def actions(self):
        def create_move(at, to):
            return lambda: self._move(at, to)

        moves = []
        for i, j in itertools.product(range(self.width),
                                      range(self.width)):
            #All possible movement directions
            direcs = {'Moving Right':(i, j-1),
                      'Moving Left':(i, j+1),
                      'Moving Down':(i-1, j),
                      'Moving Up':(i+1, j)}

            for action, (r, c) in direcs.items():#checking all valid moves for a particular instance of a board
                if r >= 0 and c >= 0 and r < self.width and c < self.width and \
                   self.board[r][c] == 0:
                    move = create_move((i,j), (r,c)), action
                    moves.append(move)
        return moves

    @property
    def manhattan(self):#calculating manhattan distance heuristic
      distance = 0
      for i in range(3):
          for j in range(3):
              if self.board[i][j] != 0:
                  x, y = divmod(self.board[i][j]-1, 3)
                  distance += abs(x - i) + abs(y - j)
      return distance

    @property
    def uninformed(self):#uninformed heuristic hardcoded to zero
      return 0


    @property
    def misplaced(self):#calcuating misplaced tile heuristic
      c=0
      for i in range(len(self.board)):
        for j in range(len(self.board[0])):
          if self.board[i][j]!=goals[i][j]:
            c+=1
      return c

    def copy(self):#creating a temp copy of the board
        board = []
        for row in self.board:
            board.append([x for x in row])
        return Puzzle(board)

    def _move(self, at, to):#moving on the temo copy of the board
        copy = self.copy()
        i, j = at
        r, c = to
        copy.board[i][j], copy.board[r][c] = copy.board[r][c], copy.board[i][j]
        return copy

    def pprint(self):#printing board
        for row in self.board:
            print(row)
        print()

    def __str__(self):
        return ''.join(map(str, self))

    def __iter__(self):#list return from the rows
        for row in self.board:
            yield from row

from pprint import pprint
import time

def getBoard():#helper function to get a custom board from the user
  board = []
  for i in range(3):
    board.append([])
    for j in range(3):
      n = int(input(f"board[{i}][{j}]: "))
      board[i].append(n)
  
  
  return board

board = [[1,2,3],[5,0,6],[4,7,8]]#hardcoded board value for testing purpoes

choice1 = int(input("Enter choice: (1) Custom Board [3x3], (2) Default board:  "))
if choice1 == 1:
  board = getBoard()

print("board: ")

for i in range(3):
  for j in range(3):
    print(board[i][j], end=" ")
  print()

metrics_allowed = ["manhattan", "misplaced", "uninformed"]
dmetric = input(f"\nEnter the distance metric to be used {metrics_allowed}:  ")#User input for heuristic
if dmetric not in metrics_allowed:
  print(f"\n\n\nERROR: metric entered ('{dmetric}') cannot be used. Choose only one from - {metrics_allowed}")
  raise KeyboardInterrupt

print(f"Distance Metric chosen: '{dmetric}'")
#-----------------------------------------------------------------------------------------------
puzzle = Puzzle(board)
s = Solver(puzzle, dmetric)
tic = time.time()
p = s.solve()
toc = time.time()

steps = 0
for node in p:
    print(node.action)
    node.puzzle.pprint()
    steps += 1
#statistics for the solved board
print("Total number of steps: " + str(steps))
print("Total amount of time in search: " + str(toc - tic) + " second(s)")

