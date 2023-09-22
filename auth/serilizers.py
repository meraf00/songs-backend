class UserSerializer:    
    @staticmethod
    def serialize(user) -> dict:
        return {
            'id': user.id,
            'email': user.email,            
        }
        