from flask import Flask, request, jsonify
import json

class GitHubWebhookApp:
    def __init__(self, handler):
        self.app = Flask(__name__)
        self.handler = handler

        @self.app.route('/webhook', methods=['POST'])
        def webhook_received():
            try:
                event = request.get_data()
                event = json.loads(event)
                payload = json.loads(event.get('payload', '{}'))
                if payload.get('head_commit'):
                    self.handler.handle_push_code_event(payload)
                elif payload.get('team') and payload.get('action') == 'created':
                    self.handler.handle_create_team_event(payload)
                elif payload.get('repository') and payload.get('action') == 'deleted':
                    self.handler.handle_delete_repo_event(payload)
                return 'Success', 200
            except Exception as e:
                print("Error processing webhook:", str(e))
                return jsonify({'error': 'An error occurred'}), 500

    def run(self):
        self.app.run(port=3000)