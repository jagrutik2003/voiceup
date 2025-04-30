from models import db, Conversation, Message, AnalysisResult
from datetime import datetime, timedelta
from app import app
from analysis import classifier

def seed_database():
    print("Seeding database...")
    
    mock_conversations = [
        {
            "messages": [
                {"sender": "agent", "text": "Hi Alex! Welcome to VoiceUp Support. How can I help you?"},
                {"sender": "customer", "text": "My internet keeps disconnecting and it's really frustrating!"},
                {"sender": "agent", "text": "I'm so sorry for the inconvenience, Alex. Let me check this for you."},
                {"sender": "customer", "text": "Thanks, I hope it gets fixed soon."},
                {"sender": "agent", "text": "I have reset your connection. Could you please check now?"},
                {"sender": "customer", "text": "Yes, it's working now. Thank you!"}
            ]
        },
        {
            "messages": [
                {"sender": "agent", "text": "Hello, how can I assist you today?"},
                {"sender": "customer", "text": "My router is showing a red light and no internet."},
                {"sender": "agent", "text": "No worries, our routers usually fix themselves in a few minutes."},
                {"sender": "customer", "text": "Are you sure? This has been happening for an hour."},
                {"sender": "agent", "text": "Guaranteed it will be fine soon!"}
            ]
        }
    ]
    
    for conv_data in mock_conversations:
        # Create conversation
        conversation = Conversation()
        db.session.add(conversation)
        db.session.flush()  # Get the ID
        
        # Create messages
        for i, msg_data in enumerate(conv_data["messages"]):
            message = Message(
                conversation_id=conversation.id,
                sender=msg_data["sender"],
                text=msg_data["text"],
                timestamp=datetime.utcnow() + timedelta(minutes=i*2)
            )
            db.session.add(message)
            
        # Analyze conversation
        all_text = " ".join([msg["text"] for msg in conv_data["messages"]])
        emotion_results = classifier(all_text)
        
        # Create analysis result
        analysis = AnalysisResult(
            conversation_id=conversation.id,
            emotion_summary={"emotions": emotion_results[0]},
            compliance_summary={
                "greeting": any("welcome" in msg["text"].lower() for msg in conv_data["messages"] if msg["sender"] == "agent"),
                "apology": any("sorry" in msg["text"].lower() for msg in conv_data["messages"] if msg["sender"] == "agent"),
                "resolution": any("fixed" in msg["text"].lower() or "working" in msg["text"].lower() for msg in conv_data["messages"])
            },
            overall_compliance_score=85
        )
        db.session.add(analysis)
    
    db.session.commit()
    print("Database seeded successfully!")

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
        seed_database()