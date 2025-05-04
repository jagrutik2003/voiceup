from models import db, Conversation, Message, AnalysisResult
from datetime import datetime, timedelta
from app import app
from analysis import classifier

def check_compliance(messages):
    """Check compliance rules and return score"""
    rules = {
        "greeting": any(any(word in msg["text"].lower() 
            for word in ["hi", "hello", "welcome"]) 
            for msg in messages if msg["sender"] == "agent" and messages.index(msg) == 0),
        
        "personalization": any(any(name in msg["text"] 
            for name in ["Alex", "John", "Sarah", "Mike"]) 
            for msg in messages if msg["sender"] == "agent"),
        
        "apology": any("sorry" in msg["text"].lower() 
            for msg in messages if msg["sender"] == "agent"),
        
        "resolution": any(word in msg["text"].lower() 
            for word in ["fixed", "resolved", "working", "solved"] 
            for msg in messages if msg["sender"] == "agent"),
        
        "no_unsupported_claims": not any(claim in msg["text"].lower() 
            for claim in ["guarantee", "always", "never fails", "forever"] 
            for msg in messages if msg["sender"] == "agent")
    }
    
    score = sum(rules.values()) / len(rules) * 100
    return rules, round(score)

def seed_database():
    print("Seeding database...")
    
    mock_conversations = [
        # Existing conversation 1
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
        # Existing conversation 2
        {
            "messages": [
                {"sender": "agent", "text": "Hello, how can I assist you today?"},
                {"sender": "customer", "text": "My router is showing a red light and no internet."},
                {"sender": "agent", "text": "No worries, our routers usually fix themselves in a few minutes."},
                {"sender": "customer", "text": "Are you sure? This has been happening for an hour."},
                {"sender": "agent", "text": "Guaranteed it will be fine soon!"}
            ]
        },
        # New conversation 3 - Good compliance
        {
            "messages": [
                {"sender": "agent", "text": "Hello Sarah! Welcome to VoiceUp support. How may I assist you today?"},
                {"sender": "customer", "text": "Hi, my internet speed is very slow lately."},
                {"sender": "agent", "text": "I understand this must be frustrating, Sarah. Let me run a speed test."},
                {"sender": "customer", "text": "Thank you, please check."},
                {"sender": "agent", "text": "I've optimized your connection settings. Can you try now?"},
                {"sender": "customer", "text": "Much better now, thank you!"},
                {"sender": "agent", "text": "Wonderful! Is there anything else I can help you with, Sarah?"}
            ]
        },
        # New conversation 4 - Poor compliance
        {
            "messages": [
                {"sender": "agent", "text": "What do you want?"},
                {"sender": "customer", "text": "Is this how you greet customers? I'm having network issues."},
                {"sender": "agent", "text": "Our network never has issues, must be your device."},
                {"sender": "customer", "text": "This is terrible service!"},
                {"sender": "agent", "text": "Try restarting your router."}
            ]
        },
        # New conversation 5 - Mixed compliance
        {
            "messages": [
                {"sender": "agent", "text": "Hello! How can I help you today?"},
                {"sender": "customer", "text": "Hi, I'm John. My Wi-Fi keeps dropping."},
                {"sender": "agent", "text": "Let me check that for you."},
                {"sender": "customer", "text": "It's really annoying!"},
                {"sender": "agent", "text": "I understand your frustration. I've reset your connection."},
                {"sender": "customer", "text": "Is it fixed now?"},
                {"sender": "agent", "text": "Yes, it should work better now."}
            ]
        }
    ]
    
    for conv_data in mock_conversations:
        # Create conversation
        conversation = Conversation()
        db.session.add(conversation)
        db.session.flush()
        
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
        
        # Check compliance
        compliance_rules, compliance_score = check_compliance(conv_data["messages"])
        
        # Create analysis result
        analysis = AnalysisResult(
            conversation_id=conversation.id,
            emotion_summary={"emotions": emotion_results[0]},
            compliance_summary=compliance_rules,
            overall_compliance_score=compliance_score
        )
        db.session.add(analysis)
    
    db.session.commit()
    print("Database seeded successfully!")

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
        seed_database()