import models
from database import engine, SessionLocal

# Create the tables in the database
models.Base.metadata.create_all(bind=engine)

def seed_db():
    db = SessionLocal()
    # Check if we already have data
    if not db.query(models.LegalKnowledge).first():
        sample_data = [
            models.LegalKnowledge(section="BNS 318", title="Cheating", description="Cheating and dishonestly inducing delivery of property."),
            models.LegalKnowledge(section="BNS 303", title="Theft", description="Whoever, intending to take dishonestly any movable property out of the possession of any person without that person's consent..."),
            models.LegalKnowledge(section="IT Act 66", title="Computer Related Offences", description="Computer or electronic resource fraud is punishable with imprisonment for a term which may extend to three years.")
        ]
        db.add_all(sample_data)
        db.commit()
    db.close()

seed_db()
