import re
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
import logging
import requests
from app.apis.ipqs import IPQSValidator
from app.apis.dnstool import Dnstool

router = APIRouter()
logger = logging.getLogger("ip_tools")

async def fetch_ip_from_api(ip: str = None):
    """
    Fetch the IP address from the external API.

    Args:
        ip (str, optional): The IP address to append to the API URL.

    Returns:
        dict: The JSON response from the external API.
    """
    url = "https://freeipapi.com/api/json"
    if ip:
        url += f"/{ip}"

    response = requests.get(url)
    response.raise_for_status()  # Check the HTTP status
    data = response.json()

    # Validate response
    if 'ipAddress' not in data:
        raise ValueError("Invalid response: 'ip' key not found")

    response = {"ip": data['ipAddress'],
            "countryName": data.get('countryName', "Unknown"),
            "regionName": data.get('regionName', "Unknown"),
            "cityName": data.get('cityName', "Unknown"),
            "zipCode": data.get('zipCode', "Unknown"),
            "isProxy": data.get('isProxy', "Unknown")
    }

    return response

@router.get("/api/iptools/info")
async def get_info():
    """
    Endpoint to get information about the ip_tools API.

    Returns:
        JSON: A JSON object with a message.
    """
    return JSONResponse(content={"message": "ip_tools endpoint v1"})

@router.get("/api/iptools/search")
async def search(request: Request):
    """
    Endpoint to process a search request.

    Args:
        request (Request): The request object containing the search data.

    Returns:
        JSON: A JSON object with the search results.
    """
    try:
        search_value = request.query_params.get("search")

        #if not search_value:
        #    raise HTTPException(status_code=400, detail="Missing 'search' query parameter")

        # Regular expressions for IP address, email, and domain
        ip_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
        email_pattern = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")
        domain_pattern = re.compile(r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$")
        phone_pattern = re.compile(r"^\+?[1-9]\d{1,14}$|^1?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$")
        dns_pattern = re.compile(r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$")
        routing_pattern = re.compile(r"^RN-\d{9}$", re.IGNORECASE)

        if ip_pattern.match(search_value):
            search_results = {
                "status": "success",
                "message": f"IP address: {search_value}",
                "type": "ip",
                "value": search_value
            }
        elif email_pattern.match(search_value):
            search_results = {
                "status": "success",
                "message": f"Email address: {search_value}",
                "type": "email",
                "value": search_value
            }
        elif domain_pattern.match(search_value):
            search_results = {
                "status": "success",
                "message": f"DNS: {search_value}",
                "type": "dns",
                "value": search_value
            }
        elif phone_pattern.match(search_value):
            if not search_value.startswith("1"):
                search_value = "1" + search_value
            search_results = {
                "status": "success",
                "message": f"Phone number: {search_value}",
                "type": "phone",
                "value": search_value
            }
        elif dns_pattern.match(search_value):
            search_results = {
                "status": "success",
                "message": f"DNS name: {search_value}",
                "type": "dns",
                "value": search_value
            }
        elif routing_pattern.match(search_value):
            search_value = search_value[3:]
            search_results = {
                "status": "success",
                "message": f"Routing number name: {search_value}",
                "type": "routing_number",
                "value": search_value
            }
        else:
            search_results = {"status": "error", "message": "Search supports IPs, emails, domains, phone numbers, and routing numbers (rn-xxxxxxxxx)."}
            return JSONResponse(content=search_results, status_code=200)

        return JSONResponse(content=search_results)
    except Exception as e:
        logger.error(f"Error processing search request: {e}")
        return JSONResponse(content={"error": "Internal Server Error"}, status_code=500)

@router.get("/api/iptools/get_my_ip")
async def get_my_ip():
    """
    Endpoint to get the client's public IP address.

    Returns:
        JSON: A JSON object with the client's public IP address.
    """
    try:
        # API call to ipify to get the public IP address
        ipify_response = requests.get("https://api.ipify.org?format=json")
        ipify_response.raise_for_status()
        ip = ipify_response.json().get("ip")
        return JSONResponse(content={"ip": ip})
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching IP address: {e}")
        return JSONResponse(content={"status": "error", "message": "Internal Server Error"}, status_code=500)

@router.get("/api/iptools/ip")
async def get_ip(request: Request):
    """
    Endpoint to get the email address from the query parameter.

    Args:
        request (Request): The request object containing the email data.

    Returns:
        JSON: A JSON object with the email address.
    """

    validator = IPQSValidator()


    response = {"status": "success"}
    ip_value = request.query_params.get("ip")
    if ip_value:
        data = validator.get_ip_data(ip_value)
        response['details'] = data.json()

    return JSONResponse(content=response)

@router.get("/api/iptools/email")
async def get_email(request: Request):
    """
    Endpoint to get the email address from the query parameter.

    Args:
        request (Request): The request object containing the email data.

    Returns:
        JSON: A JSON object with the email address.
    """

    validator = IPQSValidator()


    response = {"status": "success"}
    email_value = request.query_params.get("email")
    if email_value:
        data = validator.get_email_data(email_value)
        response['details'] = data.json()
        dark_data = validator.get_darkweb_data(email_value)
        response['darkweb'] = dark_data.json()

    return JSONResponse(content=response)

@router.get("/api/iptools/phone")
async def get_phone(request: Request):
    """
    Endpoint to get the phone number from the query parameter.

    Args:
        request (Request): The request object containing the phone data.

    Returns:
        JSON: A JSON object with the phone number.
    """

    validator = IPQSValidator()


    response = {"status": "success"}
    phone_value = request.query_params.get("phone")
    if phone_value:
        data = validator.get_phone_data(phone_value)
        response['details'] = data.json()

    return JSONResponse(content=response)

@router.get("/api/iptools/dns")
async def get_dns(request: Request):
    """
    Endpoint to get the dns from the query parameter.

    Args:
        request (Request): The request object containing the dns data.

    Returns:
        JSON: A JSON object with the dns.
    """

    validator = Dnstool()


    response = {"status": "success"}
    domain_value = request.query_params.get("domain")
    if domain_value:
        data = validator.get_dns_data(domain_value)
        print(f"Data: {data}")
        response['details'] = data

    return JSONResponse(content=response)

@router.get("/api/iptools/bank_routing")
async def get_bank_routing(request: Request):
    """
    Endpoint to get the bank_routing from the query parameter.

    Args:
        request (Request): The request object containing the bank_routing data.

    Returns:
        JSON: A JSON object with the bank_routing.
    """

    validator = Dnstool()


    response = {"status": "success"}
    routing_number = request.query_params.get("routing_number")
    if routing_number:
        data = validator.get_routing_data(routing_number)
        print(f"Data: {data}")
        response['details'] = data

    return JSONResponse(content=response)