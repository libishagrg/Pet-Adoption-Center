
class Pet:
    def __init__(self, pet_id, name, age, breed, health_status):
        self.pet_id = pet_id
        self.name = name
        self.age = age
        self.breed = breed
        self.__health_status = health_status

    def get_health_status(self):
        return self.__health_status

    def set_health_status(self, status):
        self.__health_status = status

    def display(self):
        return f"{self.pet_id} - {self.name}, Age: {self.age}, Breed: {self.breed}, Health: {self.__health_status}"

    def to_line(self):
        return f"{self.__class__.__name__},{self.pet_id},{self.name},{self.age},{self.breed},{self.__health_status}\n"

    @classmethod
    def from_line(cls, line):
        parts = line.strip().split(',')
        if len(parts) != 6:
            return None
        pet_type, pet_id, name, age, breed, health = parts
        if pet_type == "Dog":
            return Dog(pet_id, name, int(age), breed, health)
        elif pet_type == "Cat":
            return Cat(pet_id, name, int(age), breed, health)
        elif pet_type == "Bird":
            return Bird(pet_id, name, int(age), breed, health)
        return None

class Dog(Pet):
    pass

class Cat(Pet):
    pass

class Bird(Pet):
    pass

class Adopter:
    def __init__(self, adopter_id, name, contact):
        self.adopter_id = adopter_id
        self.name = name
        self.contact = contact
        self.adopted_pets = []

    def adopt_pet(self, pet):
        self.adopted_pets.append(pet)

    def display(self):
        info = f"Adopter ID: {self.adopter_id}, Name: {self.name}, Contact: {self.contact}"
        if self.adopted_pets:
            info += "\n  Adopted Pets:"
            for pet in self.adopted_pets:
                info += f"\n    - {pet.display()}"
        return info

    def to_line(self):
        pet_ids = ",".join([pet.pet_id for pet in self.adopted_pets])
        return f"{self.adopter_id},{self.name},{self.contact},{pet_ids}\n"

    @classmethod
    def from_line(cls, line):
        parts = line.strip().split(',')
        if len(parts) < 3:
            return None
        adopter_id, name, contact, *adopted_pet_ids = parts
        adopter = Adopter(adopter_id, name, contact)
        adopter.adopted_pet_ids = adopted_pet_ids  
        return adopter

class PetAdoptionCenter:
    def __init__(self):
        self.pets = []
        self.adopters = []
        self.load_data()

    def add_pet(self, pet):
        self.pets.append(pet)
        print(f"{pet.name} has been added.")

    def remove_pet(self, pet_id):
        self.pets = [p for p in self.pets if p.pet_id != pet_id]
        print(f"Pet {pet_id} removed.")

    def register_adopter(self, adopter):
        self.adopters.append(adopter)
        print(f"{adopter.name} has been registered.")

    def remove_adopter(self, adopter_id):
        self.adopters = [a for a in self.adopters if a.adopter_id != adopter_id]
        print(f"Adopter {adopter_id} removed.")

    def list_pets(self):
        if not self.pets:
            print("No pets available.")
        for pet in self.pets:
            print(pet.display())

    def list_adopters(self):
        if not self.adopters:
            print("No adopters registered.")
        for adopter in self.adopters:
            print(adopter.display())

    def adopt_pet(self, adopter_id, pet_id):
        adopter = next((a for a in self.adopters if a.adopter_id == adopter_id), None)
        pet = next((p for p in self.pets if p.pet_id == pet_id), None)
        if adopter and pet:
            adopter.adopt_pet(pet)
            self.pets.remove(pet)
            print(f"{adopter.name} has adopted {pet.name}.")
        else:
            print("Adopter or Pet not found.")

    def save_data(self):
        with open("pets.txt", "w", encoding="utf-8") as pf:
            for pet in self.pets:
                pf.write(pet.to_line())
        with open("adopters.txt", "w", encoding="utf-8") as af:
            for adopter in self.adopters:
                af.write(adopter.to_line())

    def load_data(self):
        try:
            with open("pets.txt", "r", encoding="latin-1") as pf:
                for line in pf:
                    pet = Pet.from_line(line)
                    if pet:
                        self.pets.append(pet)
        except FileNotFoundError:
            print("No pet data found. Starting fresh.")

        try:
            with open("adopters.txt", "r", encoding="latin-1") as af:
                for line in af:
                    adopter = Adopter.from_line(line)
                    if adopter:
                        adopted_ids = adopter.adopted_pet_ids if hasattr(adopter, 'adopted_pet_ids') else []
                        adopter.adopted_pets = []
                        for pet_id in adopted_ids:
                            pet = next((p for p in self.pets if p.pet_id == pet_id), None)
                            if pet:
                                adopter.adopt_pet(pet)
                                self.pets.remove(pet)
                        self.adopters.append(adopter)
        except FileNotFoundError:
            print("No adopter data found. Starting fresh.")

def main():
    center = PetAdoptionCenter()

    while True:
        print("\n--- Pet Adoption Center ---")
        print("1. Add Pet")
        print("2. Remove Pet")
        print("3. Register Adopter")
        print("4. Remove Adopter")
        print("5. List Pets")
        print("6. List Adopters")
        print("7. Adopt Pet")
        print("8. Save & Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            t = input("Type (Dog/Cat/Bird): ")
            pid = input("Pet ID: ")
            name = input("Name: ")
            age = int(input("Age: "))
            breed = input("Breed: ")
            health = input("Health Status: ")
            if t.lower() == "dog":
                pet = Dog(pid, name, age, breed, health)
            elif t.lower() == "cat":
                pet = Cat(pid, name, age, breed, health)
            elif t.lower() == "bird":
                pet = Bird(pid, name, age, breed, health)
            else:
                print("Invalid type.")
                continue
            center.add_pet(pet)

        elif choice == '2':
            pid = input("Enter Pet ID to remove: ")
            center.remove_pet(pid)

        elif choice == '3':
            aid = input("Adopter ID: ")
            name = input("Name: ")
            contact = input("Contact: ")
            adopter = Adopter(aid, name, contact)
            center.register_adopter(adopter)

        elif choice == '4':
            aid = input("Enter Adopter ID to remove: ")
            center.remove_adopter(aid)

        elif choice == '5':
            center.list_pets()

        elif choice == '6':
            center.list_adopters()

        elif choice == '7':
            aid = input("Adopter ID: ")
            pid = input("Pet ID: ")
            center.adopt_pet(aid, pid)

        elif choice == '8':
            center.save_data()
            print("Data saved. Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
