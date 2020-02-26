import hashlib
from app import db, User, Quiz

print("Press 1 to input user")
print("Press 2 to input puzzle")
print("Press 3 to input admin")

choice = input("Enter choice: ")

if choice=="1":
       totalUser = input("Total team number: ")
       totalUser = int(totalUser)

       for i in range(totalUser):
              teamName = input("Enter team name: ")
              password = input("Enter password: ")
              token = input("Enter token: ")

              password_hash = hashlib.sha256(password.encode()).hexdigest()
              user = User(name=teamName, pwd=password_hash, token=token)
              db.session.add(user)

              print("This use has been added succesfully !")
              print("Team Name: ", teamName)
              print("Password: ", password)
              print("Token: ", token)
              print("Hashed password: ", password_hash)
              print("")

       db.session.commit()

elif choice=="2":
       totalPuzzle = input("Total puzzle number: ")
       totalPuzzle = int(totalPuzzle)

       file = open("puzzle.txt", "r")
       lines = file.read().splitlines()
       count = 0

       for i in range(totalPuzzle):
              puzzle_name = lines[count]
              count += 1
              answer = lines[count]
              count += 1

              print(puzzle_name)
              print(answer)

              quiz = Quiz(answer=answer, name=puzzle_name)
              db.session.add(quiz)
              print("Quiz has been added !")
       
       file.close()
       db.session.commit()

elif choice=="3":
       adminName = input("Enter name: ")
       adminPass = input("Enter password: ")
       token = input("Enter token: ")

       password_hash = hashlib.sha256(adminPass.encode()).hexdigest()
       user = User(name=adminName, pwd=password_hash, token=token, role="ADMIN")
       db.session.add(user)
       print("Admin added !")

       db.session.commit()

else:
       print("Your wish :/")
       exit(0)
