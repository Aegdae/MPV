from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)  # Tempo de espera entre requisições

    @task
    def login(self):
        data = {
            "email": "pennellopeh@yahoo.com.br",  # Substitua pelo e-mail que você vai usar para teste
            "password": "jonnathas1524"  # Substitua pela senha correta
        }
        
        # Enviando a requisição com o tipo JSON
        response = self.client.post("/login", json=data, headers={"Content-Type": "application/json"})
        
        # Exibindo o status e resposta para ajudar a depurar
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
