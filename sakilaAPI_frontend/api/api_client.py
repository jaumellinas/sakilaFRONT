import requests
from django.conf import settings
from typing import Optional, Dict, Any


class APIClient:
    def __init__(self, token: Optional[str] = None):
        self.base_url = settings.API_BASE_URL
        self.token = token
        self.headers = self._get_headers()

    def _get_headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        try:
            if method == "GET":
                response = requests.get(
                    url, headers=self.headers, params=params
                )
            elif method == "POST":
                response = requests.post(
                    url, headers=self.headers, json=data
                )
            elif method == "PUT":
                response = requests.put(
                    url, headers=self.headers, json=data
                )
            elif method == "DELETE":
                response = requests.delete(
                    url, headers=self.headers
                )
            response.raise_for_status()
            return response.json() if response.text else {}
        except requests.exceptions.RequestException as e:
            raise Exception(f"API Error: {str(e)}")

    def register(
        self, username: str, email: str, password: str
    ) -> Dict[str, Any]:
        return self._request(
            "POST",
            "/api/v1/auth/register",
            data={
                "username": username,
                "email": email,
                "password": password
            }
        )

    def login(
        self, username: str, password: str
    ) -> Dict[str, Any]:
        data = {
            "username": username,
            "password": password
        }
        url = f"{self.base_url}/api/v1/auth/token"
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.json()

    def get_customers(self) -> list:
        return self._request(
            "GET",
            "/api/v1/customers"
        )

    def get_customer(self, customer_id: int) -> Dict[str, Any]:
        return self._request(
            "GET",
            f"/api/v1/customers/{customer_id}"
        )

    def create_customer(
        self, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        return self._request(
            "POST",
            "/api/v1/customers",
            data=data
        )

    def update_customer(
        self, customer_id: int, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        return self._request(
            "PUT",
            f"/api/v1/customers/{customer_id}",
            data=data
        )

    def delete_customer(self, customer_id: int) -> None:
        self._request(
            "DELETE",
            f"/api/v1/customers/{customer_id}"
        )

    def get_rentals(self) -> list:
        return self._request(
            "GET",
            "/api/v1/rentals"
        )

    def get_rental(self, rental_id: int) -> Dict[str, Any]:
        return self._request(
            "GET",
            f"/api/v1/rentals/{rental_id}"
        )

    def create_rental(
        self, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        return self._request(
            "POST",
            "/api/v1/rentals",
            data=data
        )

    def return_rental(self, rental_id: int) -> Dict[str, Any]:
        return self._request(
            "PUT",
            f"/api/v1/rentals/{rental_id}/return"
        )

    def get_customer_rentals(
        self, customer_id: int
    ) -> list:
        return self._request(
            "GET",
            f"/api/v1/rentals/customer/{customer_id}"
        )