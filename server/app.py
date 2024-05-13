import os
from flask import Flask, request
from datetime import datetime
from flask import jsonify
import json

app = Flask(__name__)

class GitHubWebhookHandler:
    def __init__(self):
        self.suspicious_behaviors = []

    def handle_push_event(self, payload):
        # Check if push event happened between 14:00-16:00
        # Assuming 'head_commit' and 'timestamp' fields exist in the event
        try:
            head_commit = payload.get('head_commit')
            if head_commit:
                timestamp_str = head_commit.get('timestamp')
                print("Timestamp:", timestamp_str)
                if timestamp_str:
                    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%SZ')
                    if 14 <= timestamp.hour < 17:
                        self.suspicious_behaviors.append("Pushing code between 14:00-16:00")
        except Exception as e:
            print("Error processing push event:", str(e))

    def handle_create_team_event(self, payload):
        # Check if a team name starts with 'hacker'
        try:
            team_name = payload.get('team').get('name')
            print("Team name:", team_name)
            if team_name.startswith('hacker'):
                print("Notifying security team about prefix hacker team creation")
                # Notify security team
        except Exception as e:
            print("Error processing team event:", str(e))


    def handle_create_delete_repo_event(self, payload):
        # Check if a repository is created and deleted within 10 minutes
        try:
            #the deleted time should be in UTC 0 timezone
            deleted_at_in_datetime = datetime.strptime(datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'), '%Y-%m-%dT%H:%M:%SZ')
            created_at_in_datetime = datetime.strptime(payload.get('repository').get('created_at'), '%Y-%m-%dT%H:%M:%SZ')
            if (deleted_at_in_datetime - created_at_in_datetime).total_seconds() < 600:  # 600 seconds = 10 minutes
                print("Notifying security team about creating and deleting a repository within 10 minutes")
                # Notify security team
        except Exception as e:
            print("Error processing repository event:", str(e))

    def notify_suspicious_behavior(self):
        if self.suspicious_behaviors:
            print("Suspicious behavior detected:")
            for behavior in self.suspicious_behaviors:
                print("-", behavior)




@app.route('/webhook', methods=['POST'])
def webhook_recived():
    try:
        print("Received webhook request")
        event = request.get_data()
        event = json.loads(event)
        payload = json.loads(event.get('payload', '{}'))  # Parse payload as JSON, defaulting to empty dictionary
        print("Received payload: ", payload)
        if payload.get('head_commit'):
            print("Received push event")
            webhook_handler.handle_push_event(payload)
        elif payload.get('team'):
            print("Received team event")
            webhook_handler.handle_create_team_event(payload)
        elif payload.get('repository') and payload.get('action') == 'deleted':
            print("Received repository deleted event")
            webhook_handler.handle_create_delete_repo_event(payload)
        webhook_handler.notify_suspicious_behavior()
        return '', 200
    except Exception as e:
        print("Error processing webhook:", str(e))
        return jsonify({'error': 'An error occurred'}), 500


if __name__ == '__main__':
    webhook_handler = GitHubWebhookHandler()
    app.run(port=3000)