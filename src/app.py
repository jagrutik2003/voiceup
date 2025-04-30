from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Conversation, Message, AnalysisResult
from analysis import classifier

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:aaJJ10%40%40@localhost:5432/voiceup_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask API!"})

# 🔹 Route 1: GET and POST for full emotion scores
@app.route('/api/analyze', methods=['GET', 'POST'])
def analyze_text():
    if request.method == 'GET':
        return jsonify({"message": "Send a POST request with text to analyze."})

    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Invalid JSON or missing Content-Type header"}), 400

    text = data.get('text', 'Hello Jaggau I love you')
    if not text:
        return jsonify({"error": "No text provided"}), 400

    result = classifier(text)
    return jsonify(result)

# 🔹 Route 2: POST for only top emotion (e.g., "anger")
@app.route('/api/predict', methods=['POST'])
def predict_top_emotion():
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Invalid JSON or missing Content-Type header"}), 400

    text = data.get('text', '')
    if not text:
        return jsonify({"error": "No text provided"}), 400

    result = classifier(text)
    top_emotion = max(result[0], key=lambda x: x['score'])
    return jsonify({"emotion": top_emotion['label'], "score": round(top_emotion['score'], 4)})

# 🔹 Fetch all conversations
@app.route('/api/conversations', methods=['GET'])
def get_conversations():
    conversations = Conversation.query.all()
    return jsonify([{
        'id': conv.id,
        'created_at': conv.created_at,
        'message_count': len(conv.messages),
        'analysis': {
            'emotion_summary': conv.analysis_result.emotion_summary if conv.analysis_result else None,
            'compliance_score': conv.analysis_result.overall_compliance_score if conv.analysis_result else None
        }
    } for conv in conversations])

# 🔹 Fetch conversation by ID with messages and analysis
@app.route('/api/conversations/<int:conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    conversation = Conversation.query.get_or_404(conversation_id)
    
    return jsonify({
        'id': conversation.id,
        'created_at': conversation.created_at,
        'messages': [{
            'id': msg.id,
            'sender': msg.sender,
            'text': msg.text,
            'timestamp': msg.timestamp
        } for msg in conversation.messages],
        'analysis': {
            'emotion_summary': conversation.analysis_result.emotion_summary if conversation.analysis_result else None,
            'compliance_summary': conversation.analysis_result.compliance_summary if conversation.analysis_result else None,
            'overall_compliance_score': conversation.analysis_result.overall_compliance_score if conversation.analysis_result else None
        }
    })

# 🔹 Analyze existing conversation
@app.route('/api/conversations/<int:conversation_id>/analyze', methods=['POST'])
def analyze_conversation(conversation_id):
    conversation = Conversation.query.get_or_404(conversation_id)
    
    # Combine all messages for analysis
    all_text = " ".join([msg.text for msg in conversation.messages])
    emotion_results = classifier(all_text)
    
    # Check compliance rules
    compliance_summary = {
        "greeting": any("welcome" in msg.text.lower() for msg in conversation.messages if msg.sender == "agent"),
        "apology": any("sorry" in msg.text.lower() for msg in conversation.messages if msg.sender == "agent"),
        "resolution": any("fixed" in msg.text.lower() or "working" in msg.text.lower() for msg in conversation.messages)
    }
    
    # Calculate compliance score
    compliance_score = sum(compliance_summary.values()) * 100 // len(compliance_summary)
    
    # Update or create analysis result
    if conversation.analysis_result:
        analysis = conversation.analysis_result
        analysis.emotion_summary = {"emotions": emotion_results[0]}
        analysis.compliance_summary = compliance_summary
        analysis.overall_compliance_score = compliance_score
    else:
        analysis = AnalysisResult(
            conversation_id=conversation_id,
            emotion_summary={"emotions": emotion_results[0]},
            compliance_summary=compliance_summary,
            overall_compliance_score=compliance_score
        )
        db.session.add(analysis)
    
    db.session.commit()
    
    return jsonify({
        "emotion_summary": analysis.emotion_summary,
        "compliance_summary": analysis.compliance_summary,
        "overall_compliance_score": analysis.overall_compliance_score
    })

# 🔹 Message-related endpoints
@app.route('/api/messages/<int:message_id>', methods=['GET'])
def get_message(message_id):
    message = Message.query.get_or_404(message_id)
    return jsonify({
        'id': message.id,
        'conversation_id': message.conversation_id,
        'sender': message.sender,
        'text': message.text,
        'timestamp': message.timestamp
    })

@app.route('/api/conversations/<int:conversation_id>/messages', methods=['GET'])
def get_conversation_messages(conversation_id):
    messages = Message.query.filter_by(conversation_id=conversation_id).order_by(Message.timestamp).all()
    return jsonify([{
        'id': msg.id,
        'sender': msg.sender,
        'text': msg.text,
        'timestamp': msg.timestamp
    } for msg in messages])

# 🔹 Analysis Result endpoints
@app.route('/api/analysis/<int:analysis_id>', methods=['GET'])
def get_analysis(analysis_id):
    analysis = AnalysisResult.query.get_or_404(analysis_id)
    return jsonify({
        'id': analysis.id,
        'conversation_id': analysis.conversation_id,
        'emotion_summary': analysis.emotion_summary,
        'compliance_summary': analysis.compliance_summary,
        'overall_compliance_score': analysis.overall_compliance_score,
        'analyzed_at': analysis.analyzed_at
    })

@app.route('/api/conversations/<int:conversation_id>/analysis', methods=['GET'])
def get_conversation_analysis(conversation_id):
    analysis = AnalysisResult.query.filter_by(conversation_id=conversation_id).first_or_404()
    return jsonify({
        'emotion_summary': analysis.emotion_summary,
        'compliance_summary': analysis.compliance_summary,
        'overall_compliance_score': analysis.overall_compliance_score,
        'analyzed_at': analysis.analyzed_at
    })

# 🔹 Analytics endpoints
@app.route('/api/analytics/emotions', methods=['GET'])
def get_emotion_analytics():
    analyses = AnalysisResult.query.all()
    emotion_counts = {}
    
    for analysis in analyses:
        for emotion in analysis.emotion_summary.get('emotions', []):
            label = emotion['label']
            emotion_counts[label] = emotion_counts.get(label, 0) + 1
            
    return jsonify({
        'emotion_distribution': emotion_counts,
        'total_conversations': len(analyses)
    })

@app.route('/api/analytics/compliance', methods=['GET'])
def get_compliance_analytics():
    analyses = AnalysisResult.query.all()
    total = len(analyses)
    if total == 0:
        return jsonify({'error': 'No analysis data available'})
        
    compliant_count = sum(1 for a in analyses if a.overall_compliance_score >= 80)
    
    return jsonify({
        'compliance_rate': round(compliant_count / total * 100, 2),
        'average_score': round(sum(a.overall_compliance_score for a in analyses) / total, 2),
        'total_conversations': total,
        'compliant_conversations': compliant_count
    })

if __name__ == '__main__':
    app.run(debug=True)
