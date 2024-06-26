from datetime import datetime

class GitHubWebhookHandler:
        
    def handle_push_code_event(self, payload):
        try:
            head_commit = payload.get('head_commit')
            if head_commit:
                timestamp_str = head_commit.get('timestamp')
                if timestamp_str:
                    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S%z')
                    if 14 <= timestamp.hour < 16: # test if the push event occurred between 14:00-16:00
                        self.notify_about_suspicious_behavior(suspicious_behavior_message="Push event occurred between 14:00-16:00")
        except Exception as e:
            print("Error processing push event:", str(e))
            raise e

    def handle_create_team_event(self, payload):
        try:
            team_name = payload.get('team').get('name')
            if team_name.startswith('hacker'):
                self.notify_about_suspicious_behavior(suspicious_behavior_message="Prefix hacker team creation, the team name is: " + team_name)
        except Exception as e:
            print("Error processing team event:", str(e))
            raise e

    def handle_delete_repo_event(self, payload):
        try:
            repository_name = payload.get('repository').get('name')
            deleted_at = datetime.strptime(datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'), '%Y-%m-%dT%H:%M:%SZ')
            created_at = datetime.strptime(payload.get('repository').get('created_at'), '%Y-%m-%dT%H:%M:%SZ')
            if (deleted_at - created_at).total_seconds() < 600: # test if the repository was created and deleted within 10 minutes
                self.notify_about_suspicious_behavior(suspicious_behavior_message="Creating and deleting a repository within 10 minutes, the repository name is: " + repository_name)
        except Exception as e:
            print("Error processing repository event:", str(e))
            raise e

    def notify_about_suspicious_behavior(self, suspicious_behavior_message):
        print("Suspicious behavior detected:", suspicious_behavior_message)