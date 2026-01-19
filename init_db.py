from database import Base, engine
from models import Chat, Message

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Done!")
