import random
from enum import Enum

class WumpusState(Enum):
  DEAD = 0
  AWAKE = 1
  ASLEEP = 2

gameState = {
  "alive": True,
  "wumpusState": WumpusState.ASLEEP,
  "startleChance": 0.5,
  "sleepChance": 0.4,
  "currentRoom": 1,
  "wumpusRoom": 1,
  "arrows": 4,
  "numberOfPits": 2,
  "pits": [],
  "numberOfBats": 2,
  "minCarry": 3,
  "maxCarry": 6,
  "bats": [],
  "caveMap": {
     1: [ 2,  5, 15],
     2: [ 1,  3,  7],
     3: [ 2,  4,  9],
     4: [ 3,  5, 11],
     5: [ 1,  4, 13],
     6: [ 7, 15, 16],
     7: [ 2,  6,  8],
     8: [ 3,  7,  9],
     9: [ 3,  8, 10],
    10: [ 3,  9, 11],
    11: [ 4, 10, 12],
    12: [11, 13, 19],
    13: [ 5, 12, 14],
    14: [13, 15, 20],
    15: [ 1, 6, 14],
    16: [ 6, 17, 20],
    17: [ 8, 16, 18],
    18: [10, 17, 19],
    19: [12, 18, 20],
    20: [14, 16, 19]
  }
}
# Test cave map
#  "caveMap": {
#    1: [2,3,4],
#    2: [1,3,4],
#    3: [1,2,5],
#    4: [1,2,3],
#    5: [1,6],
#    6: [7],
#    7: []

def numOfRooms(state):
  count = 0
  for room in state["caveMap"]:
    count += 1
  return count

def isBatInRoom(roomNum, state):
  for bat in state["bats"]:
    if bat["room"] == roomNum:
      return True
  return False

def randomRoom(state):
  while True:
    room = random.randint(1,numOfRooms(state))
    roomExits = state["caveMap"][room]
    if room in state["pits"] or isBatInRoom(room, state):
      continue
    if len(roomExits) > 0:
      break
  return room

def newGame(state):
  if numOfRooms(state) < 2:
    print("A game that only has one room in the cave is not supported")
    raise SystemExit
  for i in range(state["numberOfPits"]):
    state["pits"].append(randomRoom(state))
  for i in range(state["numberOfBats"]):
    state["bats"].append({"room":randomRoom(state), "roosting": True})
  while state["wumpusRoom"] == state["currentRoom"]:
    state["wumpusRoom"] = randomRoom(state)
    state["currentRoom"] = randomRoom(state)
    
def niceExitList(state):
  roomExits = state["caveMap"][state["currentRoom"]]
  numberOfExits = len(roomExits)
  if numberOfExits == 0 and state["alive"]:
    state["alive"] = False
    return "This room has no exits. You are trapped and starve to death!\n"
  if numberOfExits == 1:
    return f"This room's only exit goes to room {roomExits[0]}."
  if numberOfExits == 2:
    return f"This room has exits to rooms {roomExits[0]} and {roomExits[1]}."
  niceList = "This room has exits to rooms: "
  for exitNumber in range(numberOfExits-1):
    niceList += f"{roomExits[exitNumber]}, "
  return niceList + f"and {roomExits[-1]}."
  # NOTE: if you do not care about he ", and" here is a shortcut for the
  # last six lines:
  # return f"This room has exits to rooms: {str(roomExits)[1:-1]}."

def niceArrows(numArrows):
  if numArrows == 0:
    return "You are out of arrows!"
  if numArrows == 1:
    return "You are down to your last arrow!"
  return f"You have {numArrows} arrows left in your quiver."

def sense(state):
  roomNum = state["currentRoom"]
  roomExits = state["caveMap"][state["currentRoom"]]
  print(f"\nYou are in room {roomNum}.")
  print(niceArrows(state["arrows"]))
  if roomNum == state["wumpusRoom"] and state["wumpusState"] == WumpusState.ASLEEP:
    print("You see a sleeping wumpus!")
  elif roomNum == state["wumpusRoom"]:
    print("You see the wumpus looking back at you!")
  for exitNumber in roomExits:
    if state["wumpusRoom"] == exitNumber:
      print("You smell a wumpus!")
    if exitNumber in state["pits"]:
      print("You feel a breeze.")
    if isBatInRoom(exitNumber, state):
      print("You hear the squeaks of a very large bat.")

def move(state):
  nextRoom = int(input("\nWhat room would you like to move to? "))
  if nextRoom not in state["caveMap"][state["currentRoom"]]:
    print(f"\nI'm sorry, you cannot get to room {nextRoom} from here.")
    return
  if nextRoom not in state["caveMap"]:
    print(f"\nOh no! Room {nextRoom} doesn't exist!")
    return
  state["currentRoom"] = nextRoom

def shoot(state):
  roomExits = state["caveMap"][state["currentRoom"]]
  if state["arrows"] == 0:
    print("Unfortunately, you find your quiver is empty. You have no arrows.")
    return
  nextRoom = int(input("Which room are you going to shoot into? "))
  if nextRoom not in roomExits:
    print(f"The room you are in does not have an exit to room {nextRoom}.")
    return
  numRooms = int(input("Through how many rooms do you want your arrow to travel? "))
  print(f"The arrow leaves your bow and flies through the exit into room {nextRoom}!")
  state["arrows"] -= 1
  while numRooms > 0:
    print(".", end="");
    if nextRoom == state["currentRoom"]:
      print("\nYou blink in amazement as your arrow flies back into your room!")
      print("Unfortunately, you have been struck down by your own arrow!")
      state["alive"] = False
      break
    if nextRoom == state["wumpusRoom"]:
      print("\nYou hear a loud groan travel through the cave")
      print("Congratulations!")
      print("You have vanquished the wumpus and are released from the cave")
      state["wumpusState"] = WumpusState.DEAD
      break
    numRooms -= 1
    if numRooms == 0:
      print("\nYou hear a faint sound as your arrow hits the ground and breaks!")
      break
    roomExits = state["caveMap"][nextRoom]
    if len(roomExits) == 0:
      print("\nYou hear your arrow break against a cave wall")
      break
    nextRoom = random.choice(roomExits)

def encounter(state):
  if state["currentRoom"] == state["wumpusRoom"] and state["wumpusState"] == WumpusState.ASLEEP:
    print("You have awoken the wumpus!")
    state["wumpusState"] = WumpusState.AWAKE
    if random.random() < state["startleChance"]:
      roomExits = state["caveMap"][state["currentRoom"]]
      if len(roomExits) == 0:
        print("You startled it, but this room has no exits!")
      else:
        print("Luckily, you startled the wumpus and it ran through one of the exits!")
        state["wumpusRoom"] = random.choice(roomExits)
  if state["currentRoom"] == state["wumpusRoom"]:
    print("You have, unfortunately, been eaten by a very hungry wumpus.")
    state["alive"] = False
  if state["currentRoom"] in state["pits"]:
    print("You have fallen into a bottomless pit never to be seen again!")
    state["alive"] = False
  if isBatInRoom(state["currentRoom"], state):
    print("A superbat suddenly snatches you up and carries you away!")
    numOfRooms = random.randint(state["minCarry"], state["maxCarry"])
    newRoom = state["currentRoom"]
    while numOfRooms > 0:
      newRoom = random.choice(state["caveMap"][newRoom])
      print(".", end="")
      numOfRooms -= 1
    print(f"The bat has dropped you into room {newRoom}")
    state["currentRoom"] = newRoom
    sense(state)
    encounter(state)

def updateHazards(state):
  if state["wumpusState"] == WumpusState.AWAKE:
    roomExits = state["caveMap"][state["currentRoom"]]
    if random.random() < state["sleepChance"] and state["currentRoom"] not in state["pits"]:
      state["wumpusState"] = WumpusState.ASLEEP
    elif len(roomExits) > 0:
      state["wumpusRoom"] = random.choice(roomExits)

newGame(gameState)
print("Hunt the Wumpus")
while gameState["alive"] and gameState["wumpusState"] != WumpusState.DEAD:
  updateHazards(gameState)
  sense(gameState)
  encounter(gameState)
  if not gameState["alive"]:
    break
  print(niceExitList(gameState))
  nextAction = input("\nWhat next? ").lower()[:1]
  if nextAction == "q":
    break
  if nextAction == "m":
    move(gameState)
    continue
  if nextAction == "s":
    shoot(gameState)
    continue
  print(f"\nI'm sorry, I don't know how to do '{nextAction}'.")
  print("I know how to move, shoot my bow, or quit.\n")
