import requests
import logging

API_KEY = "xBDl2N/J4V2fUEtzuBw32Q==9zBsF1pfoJzius9m"  # personal account
BASE_URL = "https://api.api-ninjas.com/v1/"
# https://api.api-ninjas.com/v1/routingnumber?routing_number=111000012

logger = logging.getLogger("validatelogger")

def check_response(response):
    """
    Checks the HTTP response for errors based on status codes.

    :param response: The HTTP response object (requests.Response).
    :return: True if the response is successful, False otherwise.
    """
    status_messages = {
        400: "Bad Request: The server could not understand the request due to invalid syntax.",
        401: "Unauthorized: Access is denied due to invalid credentials.",
        403: "Forbidden: The server understood the request, but refuses to authorize it.",
        404: "Not Found: The requested resource could not be found.",
        500: "Internal Server Error: The server encountered an error and could not complete your request.",
        503: "Service Unavailable: The server is not ready to handle the request."
    }

    if response.status_code == 200:
        return True
    logger.error(status_messages.get(response.status_code, f"Unexpected Error: HTTP Status Code {response.status_code}"))
    return False

class Dnstool:
    """
    A class for interacting with the IPQualityScore (IPQS) API.
    Provides methods to validate emails, phone numbers, and IP addresses.
    """
    def __init__(self, response_format="json") -> None:
        self.api_key = API_KEY
        self.base_url = f"{BASE_URL}"

    def get_dns_data(self, domain):
        headers = {
            'X-Api-Key': self.api_key
        }
        # TODO need to catch 50x timeouts for bad domains
        url = f"{self.base_url}whois?domain={domain}"

        logger.info(f"URL called => {url} with headers {headers}")
        try:
            response = requests.get(url, headers=headers)
            # If the response status is 200, return JSON data
            if check_response(response):
                logger.info(f"Ran DNS check successfully: {response.json()}")
                return response.json()
            else:
                # If there's an error, return the status code and error
                logger.error(f"API call failed {response.status_code}: {response.raise_for_status()}")
                response.raise_for_status()

        except requests.exceptions.RequestException as e:
            logger.error(f"API call failed! Dont call Jack")
            return {"error": str(e)}

    def get_routing_data(self, routing_number):
        headers = {
            'X-Api-Key': self.api_key
        }
        # TODO need to catch 50x timeouts for bad domains
        url = f"{self.base_url}routingnumber?routing_number={routing_number}"

        logger.info(f"URL called => {url} with headers {headers}")
        try:
            response = requests.get(url, headers=headers)
            # If the response status is 200, return JSON data
            if check_response(response):
                logger.info(f"Ran DNS check successfully: {response.json()}")
                return response.json()
            else:
                # If there's an error, return the status code and error
                logger.error(f"API call failed {response.status_code}: {response.raise_for_status()}")
                response.raise_for_status()

        except requests.exceptions.RequestException as e:
            logger.error(f"API call failed! Dont call Jack")
            return {"error": str(e)}