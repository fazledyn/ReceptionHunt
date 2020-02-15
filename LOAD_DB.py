import hashlib
from app import db, User, Quiz

print("Press 1 to input user")
print("Press 2 to input puzzle")

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

       for i in range(totalPuzzle):
              print("Quiz no: ", i+1)
              answer = input("Enter the answer: ")

              quiz = Quiz(answer=answer)
              db.session.add(quiz)
              print("Quiz has been added !")
       
       db.session.commit()

else:
       print("Your wish :/")
       exit(0)
