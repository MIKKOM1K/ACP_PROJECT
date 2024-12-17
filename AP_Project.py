from collections import deque

class User:
    def __init__(self, name):
        self.name = name
        self.friends = set()
        self.friend_count = 0

class SocialNetwork:
    MAX_USERS = 20
    MAX_FRIEND_REQUESTS = 20

    def __init__(self):
        self.users = {}
        self.friend_requests = deque()

    def normalize_name(self, name):
        return name.strip().lower()

    def add_user(self, name):
        name = self.normalize_name(name)
        if len(self.users) >= self.MAX_USERS:
            print("Cannot add more users. Maximum limit reached.")
            return
        if name in self.users:
            print(f"User {name} already exists.")
            return
        self.users[name] = User(name)
        print(f"User {name} added successfully.")

    def add_connection(self, user1, user2):
        if user1.friend_count >= self.MAX_USERS or user2.friend_count >= self.MAX_USERS:
            print("Cannot add more connections for these users. Maximum limit reached.")
            return
        if user2 in user1.friends:
            print(f"{user1.name} and {user2.name} are already friends.")
            return
        user1.friends.add(user2)
        user2.friends.add(user1)
        user1.friend_count += 1
        user2.friend_count += 1
        print(f"{user1.name} and {user2.name} are now friends!")

    def unfriend_user(self, user1, user2):
        if user2 in user1.friends:
            user1.friends.remove(user2)
            user1.friend_count -= 1
            print(f"{user1.name} unfriended {user2.name}.")
        else:
            print(f"{user1.name} and {user2.name} are not friends.")

        if user1 in user2.friends:
            user2.friends.remove(user1)
            user2.friend_count -= 1

    def search_user(self, name):
        return self.users.get(self.normalize_name(name), None)

    def display_friends(self, user):
        if not user:
            print("User not found.")
            return
        print(f"Friends of {user.name}:")
        if not user.friends:
            print("No friends yet.")
        else:
            for idx, friend in enumerate(user.friends, 1):
                print(f"{idx}. {friend.name}")

    def display_all_users(self):
        if not self.users:
            print("No users in the network.")
            return
        print("List of Users:")
        for name in self.users:
            print(name)

    def send_friend_request(self, sender, receiver):
        if len(self.friend_requests) >= self.MAX_FRIEND_REQUESTS:
            print("Friend request queue full. Oldest request discarded.")
            self.friend_requests.popleft()
        self.friend_requests.append((sender, receiver))
        print(f"Friend request sent from {sender.name} to {receiver.name}.")

    def process_friend_requests(self, decision_callback):
        if not self.friend_requests:
            print("No pending friend requests.")
            return

        while self.friend_requests:
            sender, receiver = self.friend_requests.popleft()
            print(f"\n{receiver.name}, you have a friend request from {sender.name}.")
            decision = decision_callback(sender, receiver)
            if decision == "yes":
                self.add_connection(sender, receiver)
            elif decision == "no":
                print(f"{receiver.name} rejected the friend request from {sender.name}.")
            else:
                print("Invalid input. Friend request rejected by default.")

    def delete_user(self, name):
        name = self.normalize_name(name)
        user = self.users.pop(name, None)
        if not user:
            print("User not found.")
            return

        for friend in user.friends:
            friend.friends.remove(user)
            friend.friend_count -= 1

        print(f"User {name} deleted from the social network.")

def friend_request_decision(sender, receiver):
    decision = input(f"Do you accept {sender.name}'s friend request? (yes/no): ").strip().lower()
    return decision

def main():
    print("===================================")
    print("Welcome to the Social Network System")
    print("===================================")
    network = SocialNetwork()

    while True:
        print("\t[1] Add Multiple Users")
        print("\t[2] Send Friend Request")
        print("\t[3] Process Friend Requests")
        print("\t[4] Search User and Display Friends")
        print("\t[5] Display All Users")
        print("\t[6] Delete User")
        print("\t[7] Unfriend a User")
        print("\t[8] Exit")
        user_input = input("Enter an option: ")

        if user_input == "1":
            try:
                num_users = int(input("How many users do you want to add? "))
                if num_users > SocialNetwork.MAX_USERS:
                    print(f"Cannot add more than {SocialNetwork.MAX_USERS} users.")
                    continue
                for i in range(num_users):
                    name = input(f"Enter the name of user {i + 1}: ")
                    network.add_user(name)
            except ValueError:
                print("Please enter a valid number.")

        elif user_input == "2":
            sender_name = input("Enter sender name: ")
            receiver_name = input("Enter receiver name: ")
            sender = network.search_user(sender_name)
            receiver = network.search_user(receiver_name)
            if sender and receiver:
                network.send_friend_request(sender, receiver)
            else:
                print("Invalid sender or receiver.")

        elif user_input == "3":
            network.process_friend_requests(friend_request_decision)

        elif user_input == "4":
            search_name = input("Enter the name to search: ")
            user = network.search_user(search_name)
            if user:
                network.display_friends(user)
            else:
                print("User not found.")

        elif user_input == "5":
            network.display_all_users()

        elif user_input == "6":
            name = input("Enter the name of the user to delete: ")
            network.delete_user(name)

        elif user_input == "7":
            user1_name = input("Enter your name: ")
            user2_name = input("Enter the name of the user you want to unfriend: ")
            user1 = network.search_user(user1_name)
            user2 = network.search_user(user2_name)
            if user1 and user2:
                network.unfriend_user(user1, user2)
            else:
                print("One or both users not found.")

        elif user_input == "8":
            print("Exiting program...")
            break

        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()

