class user:
    user_count = 0
    def _init_(self,name,email):
        self.name = name
        self.email = email
        user.user_count += 1


    def greet(self):
        return f"Hello, {self.name}!"
    
        
