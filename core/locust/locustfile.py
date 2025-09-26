from locust import HttpUser, task, between


class ExpenseUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        """
        Called when a simulated user starts.
        Login to get access token cookie.
        """
        self.username = "testuser"
        self.password = "testpassword"
        response = self.client.post(
            "/auth/login", data={"username": self.username, "password": self.password}
        )
        # Save cookies automatically handled by Locust
        if response.status_code != 200:
            print("Failed to login!")

    @task(3)
    def list_expenses(self):
        # GET /expenses
        self.client.get("/expenses")

    @task(2)
    def create_expense(self):
        # POST /expenses
        expense_data = {"title": "Coffee", "amount": 5000, "category": "Food"}
        self.client.post("/expenses", json=expense_data)

    @task(1)
    def get_non_existing_expense(self):
        # GET /expenses/<non_existing_id> to trigger 404
        self.client.get("/expenses/9999", catch_response=True)
