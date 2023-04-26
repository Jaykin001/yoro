from locust import HttpUser, task, between
import json

class TelegramUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def send_message(self):
        
        rasa_url = "https://2e63-180-211-99-146.ngrok-free.app/webhooks/telegram/webhook"
        rasa_payload = {
            "update_id": 123456,  # Random update_id
            "message": {
                "message_id": 123456,  # Random message_id
                "chat": {
                    "id": 5161210704,
                    "type": "private"
                },
                "text": "Which salesperson has the highest win rate?"
            }
        }
        rasa_headers = {
            "Content-Type": "application/json"
        }
        with self.client.post(rasa_url, data=json.dumps(rasa_payload), headers=rasa_headers, catch_response=True) as rasa_response:
            if rasa_response.status_code == 200:
                rasa_response.success()
            else:
                rasa_response.failure("Failed to get response from Rasa")
                
        response_time_ms = (rasa_response.elapsed.total_seconds()) * 1
        print("Response time for sending and receiving message: {} s".format(response_time_ms))

