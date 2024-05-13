from app import GitHubWebhookApp
from webhooksHandler import GitHubWebhookHandler

if __name__ == '__main__':
    webhook_handler = GitHubWebhookHandler()
    app = GitHubWebhookApp(webhook_handler)
    app.run()