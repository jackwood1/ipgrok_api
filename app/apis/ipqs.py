import requests
import logging
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("IPQ_API_KEY")
IPQA_BASE_URL = "https://www.ipqualityscore.com/api/"

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

class IPQSValidator:
    """
    A class for interacting with the IPQualityScore (IPQS) API.
    Provides methods to validate emails, phone numbers, and IP addresses.
    """
    def __init__(self, response_format="json") -> None:
        self.api_key = API_KEY
        self.base_url = f"{IPQA_BASE_URL}"
        # TODO implement including User Agent in the request for IP
        self.ip_rep_url = f"https://www.ipqualityscore.com/api/json/ip/{self.api_key}"
        self.email_url = f"https://www.ipqualityscore.com/api/json/email/{self.api_key}"
        self.phone_url = f"https://www.ipqualityscore.com/api/json/phone/{self.api_key}"
        self.leaked_email_url  = f"https://www.ipqualityscore.com/api/json/leaked/email/{self.api_key}"
        self.leaked_email_url = f"https://www.ipqualityscore.com/api/json/leaked/email/{self.api_key}"

    def get_ip_data(self, ip_address, strictness=1, allow_public_access_points=True, fast=False, mobile=False):
        """
        Check if an IP address is a proxy or associated with malicious behavior.

        Args:
            ip_address (str): The IP address to be checked.
            strictness (int, optional): Adjusts detection accuracy. Defaults to 1 (low strictness).
            allow_public_access_points (bool, optional): Allows public access points in the detection. Defaults to True.
            fast (bool, optional): If True, prioritize speed over accuracy. Defaults to False.
            mobile (bool, optional): If True, treat the IP as mobile. Defaults to False.

        Returns:
            dict: JSON response from the API with proxy detection details.
        """

        # Parameters for API request
        params = {
            'strictness': strictness,
            'allow_public_access_points': str(allow_public_access_points).lower(),
            'fast': str(fast).lower(),
            'mobile': str(mobile).lower()
        }
        url = f"{self.ip_rep_url}/{ip_address}"

        logger.info(f"URL called => {url} with params {params}")
        try:
            response = requests.get(url, params=params)
            # If the response status is 200, return JSON data
            if check_response(response):
                logger.info(f"Ran IP reputation check successfully: {response.json()}")
                return response
            else:
                # If there's an error, return the status code and error
                logger.error(f"API call failed {response.status_code}: {response.raise_for_status()}")
                response.raise_for_status()

        except requests.exceptions.RequestException as e:
            logger.error(f"API call failed! Dont call Jack")
            return {"error": str(e)}

    def parse_ip_response(self, response):
        """
        Parses the JSON response if successful.

        :param response: The HTTP response object (requests.Response).
        :return: Parsed JSON data if successful, None otherwise.
        """
        try:
            json_data = response.json()
            if json_data.get('success', False):
                # Extracting the required values
                logger.info(f"Request successful. Parsed JSON:")
                ip = json_data.get('host')
                is_proxy = json_data.get('proxy')
                is_vpn = json_data.get('vpn')
                connection_type = json_data.get('connection_type')
                country_code = json_data.get('country_code')
                recent_abuse = json_data.get('recent_abuse')
                is_frequent_abuser = json_data.get('frequent_abuser')
                is_high_risk_attacks = json_data.get('high_risk_attacks')
                abuse_velocity = json_data.get('abuse_velocity')
                is_crawler = json_data.get('is_crawler')
                bot_status = json_data.get('bot_status')
                is_shared_connection = json_data.get('shared_connection')
                is_dynamic_connection = json_data.get('dynamic_connection')
                message = json_data.get('message')
                high_risk_attacks = json_data.get('high_risk_attacks')
                fraud_score = json_data.get('fraud_score')

                return {
                    'ip_address': ip,
                    'is_proxy': is_proxy,
                    'is_vpn': is_vpn,
                    'country_code': country_code,
                    'connection_type': connection_type,
                    'is_frequent_abuser': is_frequent_abuser,
                    'abuse_velocity': abuse_velocity,
                    'is_recent_abuse': recent_abuse,
                    'is_crawler': is_crawler,
                    "is_bot": bot_status,
                    "is_shared_connection": is_shared_connection,
                    "is_dynamic_connection": is_dynamic_connection,
                    'message': message,
                    'is_high_risk_attacks': high_risk_attacks,
                    'fraud_score': fraud_score
                }
            else:
                logger.error(f"Request failed. Message: {json_data.get('message', 'No message provided')}")
                return None
        except ValueError as e:
            logger.error(f"Error parsing JSON response: {e}")
            return None

    def get_email_data(self, email: str, timeout: int = 7, fast: str = 'false', abuse_strictness: int = 0) -> str:
        # Parameters for API request
        params = {
            'strictness': abuse_strictness,
            'timeout': timeout,
            'fast': str(fast).lower()
        }
        url = f"{self.email_url}/{email}"

        logger.info(f"URL called => {url} with params {params}")

        try:
            response = requests.get(url, params=params)
            # If the response status is 200, return JSON data
            if check_response(response):
                logger.info(f"Ran email reputation check successfully: {response.json()}")
                return response
            else:
                # If there's an error, return the status code and error
                logger.error(f"API call failed {response.status_code}: {response.raise_for_status()}")
                response.raise_for_status()

        except requests.exceptions.RequestException as e:
            logger.error(f"API call failed! Dont call Jack")
            return {"error": str(e)}

    def parse_email_response(self, response):
        """
        Parses the JSON response if successful.

        :param response: The HTTP response object (requests.Response).
        :return: Parsed JSON data if successful, None otherwise.
        """
        try:
            json_data = response.json()
            if json_data.get('success', False):
                # Extracting the required values
                logger.info(f"Request successful. Parsed JSON:")
                email = json_data.get('sanitized_email')
                overall_score = json_data.get('overall_score')
                spam_trap_score = json_data.get('spam_trap_score')
                is_honeypot = json_data.get('honeypot')
                is_valid = json_data.get('valid')
                is_disposable = json_data.get('disposable')
                first_seen_timestamp = json_data.get('first_seen', {}).get('timestamp')
                message = json_data.get('message')
                is_leaked = json_data.get('leaked')
                fraud_score = json_data.get('fraud_score')

                return {
                    'email': email,
                    'overall_score': overall_score,
                    'spam_trap_score': spam_trap_score,
                    'is_valid': is_valid,
                    'is_disposable': is_disposable,
                    'first_seen_timestamp': first_seen_timestamp,
                    'is_honeypot': is_honeypot,
                    'message': message,
                    'is_leaked': is_leaked,
                    'fraud_score': fraud_score
                }
            else:
                logger.error(f"Request failed. Message: {json_data.get('message', 'No message provided')}")
                return None
        except ValueError as e:
            logger.error(f"Error parsing JSON response: {e}")
            return None

    def get_phone_data(self, phone_number, strictness=1, country="US"):
        # Parameters for API request
        params = {
            'strictness': strictness,
            'country': country
        }
        url = f"{self.phone_url}/{phone_number}"

        logger.info(f"URL called => {url} with params {params}")
        try:
            response = requests.get(url, params=params)
            # If the response status is 200, return JSON data
            if check_response(response):
                logger.info(f"Ran email reputation check successfully: {response.json()}")
                return response
            else:
                # If there's an error, return the status code and error
                logger.error(f"API call failed {response.status_code}: {response.raise_for_status()}")
                response.raise_for_status()

        except requests.exceptions.RequestException as e:
            logger.error(f"API call failed! Dont call Jack")
            return {"error": str(e)}

    def parse_phone_response(self, response):
        """
        Parses the JSON response if successful.

        :param response: The HTTP response object (requests.Response).
        :return: Parsed JSON data if successful, None otherwise.
        """
        try:
            json_data = response.json()
            if json_data.get('success', False):
                # Extracting the required values
                logger.info(f"Request successful. Parsed JSON:")
                phone_number = json_data.get('formatted')
                is_valid = json_data.get('valid')
                fraud_score = json_data.get('fraud_score')
                is_prepaid = json_data.get('prepaid')
                is_recent_abuse = json_data.get('recent_abuse')
                is_voip = json_data.get('VOIP')
                is_risky = json_data.get('risky')
                is_active = json_data.get('active')
                line_type = json_data.get('line_type')
                is_leaked = json_data.get('leaked')
                user_activity = json_data.get('user_activity')
                associated_email_addresses = json_data.get('associated_email_addresses', {}).get('emails')

                return {
                    'phone_number': phone_number,
                    'is_valid': is_valid,
                    'fraud_score': fraud_score,
                    'is_prepaid': is_prepaid,
                    'is_recent_abuse': is_recent_abuse,
                    'is_voip': is_voip,
                    'is_risky': is_risky,
                    'is_active': is_active,
                    'line_type': line_type,
                    'is_leaked': is_leaked,
                    'user_activity': user_activity,
                    'associated_email_addresses': associated_email_addresses
                }
            else:
                logger.error(f"Request failed. Message: {json_data.get('message', 'No message provided')}")
                return None
        except ValueError as e:
            logger.error(f"Error parsing JSON response: {e}")
            return None

    def get_darkweb_data(self, email):

        params = {} # none supported yet
        url = f"{self.leaked_email_url}/{email}"

        logger.info(f"URL called => {url} with params {params}")
        try:
            response = requests.get(url, params=params)
            # If the response status is 200, return JSON data
            if check_response(response):
                logger.info(f"Ran email reputation check successfully: {response.json()}")
                return response
            else:
                # If there's an error, return the status code and error
                logger.error(f"API call failed {response.status_code}: {response.raise_for_status()}")
                response.raise_for_status()

        except requests.exceptions.RequestException as e:
            logger.error(f"API call failed! Dont call Jack")
            return {"error": str(e)}

    def parse_darkweb_response(self, response):
        """
        Parses the JSON response if successful.

        :param response: The HTTP response object (requests.Response).
        :return: Parsed JSON data if successful, None otherwise.
        """
        try:
            json_data = response.json()
            if json_data.get('success', False):
                # Extracting the required values
                logger.info(f"Request successful. Parsed JSON:")
                phone_number = json_data.get('formatted')
                is_valid = json_data.get('valid')
                fraud_score = json_data.get('fraud_score')
                is_prepaid = json_data.get('prepaid')
                is_recent_abuse = json_data.get('recent_abuse')
                is_voip = json_data.get('VOIP')
                is_risky = json_data.get('risky')
                is_active = json_data.get('active')
                line_type = json_data.get('line_type')
                is_leaked = json_data.get('leaked')
                user_activity = json_data.get('user_activity')
                associated_email_addresses = json_data.get('associated_email_addresses', {}).get('emails')

                return {
                    'phone_number': phone_number,
                    'is_valid': is_valid,
                    'fraud_score': fraud_score,
                    'is_prepaid': is_prepaid,
                    'is_recent_abuse': is_recent_abuse,
                    'is_voip': is_voip,
                    'is_risky': is_risky,
                    'is_active': is_active,
                    'line_type': line_type,
                    'is_leaked': is_leaked,
                    'user_activity': user_activity,
                    'associated_email_addresses': associated_email_addresses
                }
            else:
                logger.error(f"Request failed. Message: {json_data.get('message', 'No message provided')}")
                return None
        except ValueError as e:
            logger.error(f"Error parsing JSON response: {e}")
            return None