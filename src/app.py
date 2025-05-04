from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Conversation, Message, AnalysisResult
from analysis import classifier
import json
import logging

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://localhost:5173"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:aaJJ10%40%40@localhost:5432/voiceup_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

db.init_app(app)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask API!"})

@app.route('/api/analyze', methods=['GET', 'POST'])
def analyze_text():
    if request.method == 'GET':
        return jsonify({"message": "Send a POST request with text to analyze."})

    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Invalid JSON or missing Content-Type header"}), 400

    text = data.get('text', '')
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        result = classifier(text)
        logger.debug(f"Analyze result: {result}")
        return jsonify(result)
    except Exception as e:
        logger.error(f"Classifier error: {str(e)}")
        return jsonify({"error": f"Failed to analyze text: {str(e)}"}), 500

@app.route('/api/predict', methods=['POST'])
def predict_top_emotion():
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Invalid JSON or missing Content-Type header"}), 400

    text = data.get('text', '')
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        result = classifier(text)
        logger.debug(f"Predict result: {result}")
        top_emotion = max(result[0], key=lambda x: x['score'])
        return jsonify({"emotion": top_emotion['label'], "score": round(top_emotion['score'], 4)})
    except Exception as e:
        logger.error(f"Classifier error: {str(e)}")
        return jsonify({"error": f"Failed to predict emotion: {str(e)}"}), 500

@app.route('/api/conversations', methods=['GET'])
def get_conversations():
    try:
        conversations = Conversation.query.all()
        logger.debug(f"Fetched {len(conversations)} conversations")
        return jsonify([{
            'id': conv.id,
            'created_at': conv.created_at.isoformat(),
            'message_count': len(conv.messages),
            'analysis': {
                'emotion_summary': conv.analysis_result.emotion_summary if conv.analysis_result else None,
                'compliance_score': conv.analysis_result.overall_compliance_score if conv.analysis_result else None
            }
        } for conv in conversations])
    except Exception as e:
        logger.error(f"Error fetching conversations: {str(e)}")
        return jsonify({"error": "Failed to fetch conversations"}), 500

@app.route('/api/conversations/<int:conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    try:
        conversation = Conversation.query.get_or_404(conversation_id)
        return jsonify({
            'id': conversation.id,
            'created_at': conversation.created_at.isoformat(),
            'messages': [{
                'id': msg.id,
                'sender': msg.sender,
                'text': msg.text,
                'timestamp': msg.timestamp.isoformat()
            } for msg in conversation.messages],
            'analysis': {
                'emotion_summary': conversation.analysis_result.emotion_summary if conversation.analysis_result else None,
                'compliance_summary': conversation.analysis_result.compliance_summary if conversation.analysis_result else None,
                'overall_compliance_score': conversation.analysis_result.overall_compliance_score if conversation.analysis_result else None
            }
        })
    except Exception as e:
        logger.error(f"Error fetching conversation {conversation_id}: {str(e)}")
        return jsonify({"error": f"Conversation {conversation_id} not found"}), 404

def check_compliance(messages):
    rules = {
        "greeting": any(any(word in msg.text.lower() 
            for word in ["hi", "hello", "welcome"]) 
            for msg in messages if msg.sender == "agent" and messages.index(msg) == 0),
        "personalization": any(any(name in msg.text 
            for name in ["Alex", "John", "Sarah", "Mike"]) 
            for msg in messages if msg.sender == "agent"),
        "apology": any("sorry" in msg.text.lower() 
            for msg in messages if msg.sender == "agent"),
        "resolution": any(any(word in msg.text.lower() 
            for word in ["fixed", "resolved", "working", "solved"]) 
            for msg in messages if msg.sender == "agent"),
        "no_unsupported_claims": not any(any(claim in msg.text.lower() 
            for claim in ["guarantee", "always", "never fails", "forever"]) 
            for msg in messages if msg.sender == "agent")
    }
    
    score = sum(1 for rule in rules.values() if rule) / len(rules) * 100
    return rules, round(score)

@app.route('/api/conversations/<int:conversation_id>/analyze', methods=['POST'])
def analyze_conversation(conversation_id):
    try:
        conversation = Conversation.query.get_or_404(conversation_id)
        
        all_text = " ".join([msg.text for msg in conversation.messages])
        if not all_text.strip():
            logger.warning(f"No text to analyze for conversation {conversation_id}")
            return jsonify({"error": "No text to analyze"}), 400
        
        emotion_results = classifier(all_text)
        logger.debug(f"Conversation {conversation_id} emotion results: {emotion_results}")
        
        if not isinstance(emotion_results, list) or not emotion_results or not isinstance(emotion_results[0], list):
            logger.error(f"Invalid classifier output for conversation {conversation_id}: {emotion_results}")
            return jsonify({"error": "Invalid classifier output"}), 500
        
        compliance_rules, compliance_score = check_compliance(conversation.messages)
        
        if conversation.analysis_result:
            analysis = conversation.analysis_result
            analysis.emotion_summary = {"emotions": emotion_results[0]}
            analysis.compliance_summary = compliance_rules
            analysis.overall_compliance_score = compliance_score
        else:
            analysis = AnalysisResult(
                conversation_id=conversation_id,
                emotion_summary={"emotions": emotion_results[0]},
                compliance_summary=compliance_rules,
                overall_compliance_score=compliance_score
            )
            db.session.add(analysis)
        
        db.session.commit()
        
        return jsonify({
            "emotion_summary": analysis.emotion_summary,
            "compliance_summary": analysis.compliance_summary,
            "overall_compliance_score": analysis.overall_compliance_score
        })
    except Exception as e:
        logger.error(f"Error analyzing conversation {conversation_id}: {str(e)}")
        return jsonify({"error": f"Failed to analyze conversation: {str(e)}"}), 500

@app.route('/api/messages/<int:message_id>', methods=['GET'])
def get_message(message_id):
    try:
        message = Message.query.get_or_404(message_id)
        return jsonify({
            'id': message.id,
            'conversation_id': message.conversation_id,
            'sender': message.sender,
            'text': message.text,
            'timestamp': message.timestamp.isoformat()
        })
    except Exception as e:
        logger.error(f"Error fetching message {message_id}: {str(e)}")
        return jsonify({"error": f"Message {message_id} not found"}), 404

@app.route('/api/messages/<int:message_id>/analyze', methods=['POST'])
def analyze_message(message_id):
    try:
        message = Message.query.get_or_404(message_id)
        logger.debug(f"Analyzing message {message_id}: {message.text}")
        if not message.text.strip():
            logger.warning(f"Empty text for message {message_id}")
            return jsonify({"emotions": []}), 200
        emotion_results = classifier(message.text)
        logger.debug(f"Emotion results for message {message_id}: {emotion_results}")
        if not isinstance(emotion_results, list) or not emotion_results or not isinstance(emotion_results[0], list):
            logger.error(f"Invalid classifier output for message {message_id}: {emotion_results}")
            return jsonify({"error": "Invalid classifier output"}), 500
        return jsonify({"emotions": emotion_results[0]})
    except Exception as e:
        logger.error(f"Error analyzing message {message_id}: {str(e)}")
        return jsonify({"error": f"Failed to analyze message: {str(e)}"}), 500

@app.route('/api/conversations/<int:conversation_id>/messages', methods=['GET'])
def get_conversation_messages(conversation_id):
    try:
        messages = Message.query.filter_by(conversation_id=conversation_id).order_by(Message.timestamp).all()
        return jsonify([{
            'id': msg.id,
            'sender': msg.sender,
            'text': msg.text,
            'timestamp': msg.timestamp.isoformat()
        } for msg in messages])
    except Exception as e:
        logger.error(f"Error fetching messages for conversation {conversation_id}: {str(e)}")
        return jsonify({"error": "Failed to fetch messages"}), 500

@app.route('/api/analysis/<int:analysis_id>', methods=['GET'])
def get_analysis(analysis_id):
    try:
        analysis = AnalysisResult.query.get_or_404(analysis_id)
        emotion_summary = analysis.emotion_summary
        if isinstance(emotion_summary, str):
            try:
                emotion_summary = json.loads(emotion_summary)
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON in emotion_summary for analysis {analysis_id}")
                emotion_summary = {}
        return jsonify({
            'id': analysis.id,
            'conversation_id': analysis.conversation_id,
            'emotion_summary': emotion_summary,
            'compliance_summary': analysis.compliance_summary,
            'overall_compliance_score': analysis.overall_compliance_score,
            'analyzed_at': analysis.analyzed_at.isoformat() if analysis.analyzed_at else None
        })
    except Exception as e:
        logger.error(f"Error fetching analysis {analysis_id}: {str(e)}")
        return jsonify({"error": f"Analysis {analysis_id} not found"}), 404

@app.route('/api/conversations/<int:conversation_id>/analysis', methods=['GET'])
def get_conversation_analysis(conversation_id):
    try:
        analysis = AnalysisResult.query.filter_by(conversation_id=conversation_id).first()
        if not analysis:
            logger.warning(f"No analysis found for conversation {conversation_id}")
            return jsonify({"error": f"Analysis for conversation {conversation_id} not found"}), 404
        emotion_summary = analysis.emotion_summary
        if isinstance(emotion_summary, str):
            try:
                emotion_summary = json.loads(emotion_summary)
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON in emotion_summary for conversation {conversation_id}")
                emotion_summary = {}
        return jsonify({
            'emotion_summary': emotion_summary,
            'compliance_summary': analysis.compliance_summary,
            'overall_compliance_score': analysis.overall_compliance_score,
            'analyzed_at': analysis.analyzed_at.isoformat() if analysis.analyzed_at else None
        })
    except Exception as e:
        logger.error(f"Error fetching analysis for conversation {conversation_id}: {str(e)}")
        return jsonify({"error": f"Failed to fetch analysis: {str(e)}"}), 500

@app.route('/api/analytics/emotions', methods=['GET'])
def get_emotion_analytics():
    try:
        analyses = AnalysisResult.query.all()
        if not analyses:
            return jsonify({
                'distribution': {},
                'trend': [],
                'total_conversations': 0
            })
        
        emotion_distribution = {}
        emotion_trend = []
        
        for analysis in analyses:
            emotion_summary = analysis.emotion_summary
            if isinstance(emotion_summary, str):
                try:
                    emotion_summary = json.loads(emotion_summary)
                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON in emotion_summary for analysis {analysis.id}")
                    continue
            
            emotions = emotion_summary.get('emotions', []) if isinstance(emotion_summary, dict) else []
            for emotion in emotions:
                if not isinstance(emotion, dict):
                    continue
                label = emotion.get('label')
                score = emotion.get('score')
                if label and score is not None:
                    emotion_distribution[label] = emotion_distribution.get(label, 0) + float(score)
            
            conversation = Conversation.query.get(analysis.conversation_id)
            if conversation:
                emotion_trend.append({
                    'date': conversation.created_at.strftime('%Y-%m-%d'),
                    'emotions': emotions
                })
        
        return jsonify({
            'distribution': emotion_distribution,
            'trend': emotion_trend,
            'total_conversations': len(analyses)
        })
    except Exception as e:
        logger.error(f"Error fetching emotion analytics: {str(e)}")
        return jsonify({"error": "Failed to fetch emotion analytics"}), 500

@app.route('/api/analytics/compliance', methods=['GET'])
def get_compliance_analytics():
    try:
        analyses = AnalysisResult.query.all()
        total = len(analyses)
        if total == 0:
            return jsonify({'error': 'No analysis data available'})
        
        compliant_count = sum(1 for a in analyses if a.overall_compliance_score >= 80)
        scores = [a.overall_compliance_score for a in analyses]
        
        rule_violations = {
            "greeting": 0,
            "personalization": 0,
            "apology": 0,
            "resolution": 0,
            "no_unsupported_claims": 0
        }
        
        for analysis in analyses:
            for rule, passed in analysis.compliance_summary.items():
                if not passed:
                    rule_violations[rule] += 1
        
        return jsonify({
            'compliance_rate': round(compliant_count / total * 100, 2) if total > 0 else 0,
            'average_score': round(sum(a.overall_compliance_score for a in analyses) / total, 2) if total > 0 else 0,
            'total_conversations': total,
            'compliant_conversations': compliant_count,
            'rule_violations': rule_violations,
            'scores': scores
        })
    except Exception as e:
        logger.error(f"Error fetching compliance analytics: {str(e)}")
        return jsonify({"error": "Failed to fetch compliance analytics"}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)