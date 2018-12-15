from app.models import User, DbSetup, OpenIdAccount

class UserService():
    def __init__(self, dbsetup: DbSetup):
        self.dbsetup = dbsetup
    
    def get_user(self, id: int) -> User:
        session = self.dbsetup.create_session()
        user = session.query(User) \
                      .filter(User.id == id) \
                      .one_or_none()
        session.close()
        return user

    def get_or_add_openid_account(self, issuer_identifier: str, subject_identifier: str) -> User:
        session = self.dbsetup.create_session()

        # Look to see if there is an existing OpenId based account
        existing = session.query(OpenIdAccount) \
                          .filter(OpenIdAccount.issuer_identifier == issuer_identifier) \
                          .filter(OpenIdAccount.subject_identifier == subject_identifier) \
                          .one_or_none()

        if existing is None:
            # Build a new OpenId account and a new user object
            user = User()
            openid_account = OpenIdAccount(
                issuer_identifier = issuer_identifier, 
                subject_identifier = subject_identifier,
                user = user)
            session.add(user)
            session.commit()
            # Access the user.id property to force SQLAlchemy to get the newly generated id.
            id = user.id
        else:
            # Return the user associated with the existing account
            user = session.query(User).filter(User.id == existing.user_id).one()
        
        session.close()
        return user