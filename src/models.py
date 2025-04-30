from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

db = SQLAlchemy()

class Conversation(db.Model):
    __tablename__ = 'conversations'
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    messages = db.relationship('Message', backref='conversation', cascade='all, delete-orphan')
    analysis_result = db.relationship('AnalysisResult', backref='conversation', uselist=False, cascade='all, delete-orphan')

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=False)
    sender = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class AnalysisResult(db.Model):
    __tablename__ = 'analysis_results'
    
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=False)
    emotion_summary = db.Column(JSONB, nullable=False)
    compliance_summary = db.Column(JSONB, nullable=False)
    overall_compliance_score = db.Column(db.Integer, nullable=False)
    analyzed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)