from app.repositories.user_repository import UserRepository

class UserService:
    @staticmethod
    def authenticate_user(email, password):
        return UserRepository.authenticate(email, password)

    @staticmethod
    def add_user(first_name, last_name, email, password):
        UserRepository.add(first_name, last_name, email, password)

    @staticmethod
    def get_user_by_email(email):
        return UserRepository.get_by_email(email)

    @staticmethod
    def update_user_theme(user_id, theme):
        UserRepository.update_theme(user_id, theme)
