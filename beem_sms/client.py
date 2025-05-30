"""
Main client module for Beem SMS SDK
"""

import logging
import time
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass
from enum import Enum
import requests
from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .exceptions import (
    SMSError,
    AuthenticationError,
    ValidationError,
    APIError,
    NetworkError,
)
from .validators import PhoneNumberValidator


class SMSEncoding(Enum):
    """SMS encoding types"""
    PLAIN_TEXT = 0
    UNICODE = 8


@dataclass
class SMSRecipient:
    """SMS recipient data structure"""
    dest_addr: str
    recipient_id: Optional[int] = None

    def __post_init__(self):
        if not self.recipient_id:
            # Generate a simple ID based on phone number hash
            self.recipient_id = abs(hash(self.dest_addr)) % 10000


@dataclass
class SMSResponse:
    """SMS API response data structure"""
    success: bool
    status_code: int
    message: str
    response_data: Optional[Dict[str, Any]] = None
    request_id: Optional[str] = None


class BeemSMSClient:
    """
    Professional Beem SMS client with comprehensive features
    
    Features:
    - Input validation
    - Proper error handling
    - Logging
    - Retry logic
    - Rate limiting
    - Type hints
    - Structured responses
    """
    
    DEFAULT_BASE_URL = "https://apisms.beem.africa/v1/send"
    MAX_MESSAGE_LENGTH = 160  # SMS limit for plain text
    MAX_UNICODE_LENGTH = 70   # SMS limit for Unicode
    DEFAULT_TIMEOUT = 30
    MAX_RETRIES = 3
    
    def __init__(
        self,
        api_key: str,
        secret_key: str,
        base_url: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
        max_retries: int = MAX_RETRIES,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize Beem SMS client
        
        Args:
            api_key: Your Beem API key
            secret_key: Your Beem secret key
            base_url: API base URL (optional)
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            logger: Custom logger instance
        """
        if not api_key or not secret_key:
            raise AuthenticationError("API key and secret key are required")
        
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = base_url or self.DEFAULT_BASE_URL
        self.timeout = timeout
        
        # Setup logging
        self.logger = logger or self._setup_logger()
        
        # Setup requests session with retry strategy
        self.session = self._setup_session(max_retries)
        
        self.logger.info("Beem SMS client initialized")
    
    def _setup_logger(self) -> logging.Logger:
        """Setup default logger"""
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def _setup_session(self, max_retries: int) -> requests.Session:
        """Setup requests session with retry strategy"""
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["POST"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def _validate_message(self, message: str, encoding: SMSEncoding) -> None:
        """Validate message content and length"""
        if not message or not message.strip():
            raise ValidationError("Message cannot be empty")
        
        max_length = (
            self.MAX_UNICODE_LENGTH 
            if encoding == SMSEncoding.UNICODE 
            else self.MAX_MESSAGE_LENGTH
        )
        
        if len(message) > max_length:
            raise ValidationError(
                f"Message too long. Max length: {max_length} characters"
            )
    
    def _validate_recipients(self, recipients: List[SMSRecipient]) -> None:
        """Validate recipients list"""
        if not recipients:
            raise ValidationError("At least one recipient is required")
        
        for recipient in recipients:
            if not PhoneNumberValidator.validate(recipient.dest_addr):
                raise ValidationError(
                    f"Invalid phone number format: {recipient.dest_addr}"
                )
    
    def _prepare_payload(
        self,
        source_addr: str,
        message: str,
        recipients: List[SMSRecipient],
        encoding: SMSEncoding = SMSEncoding.PLAIN_TEXT
    ) -> Dict[str, Any]:
        """Prepare API request payload"""
        return {
            "source_addr": source_addr,
            "encoding": encoding.value,
            "message": message,
            "recipients": [
                {
                    "recipient_id": recipient.recipient_id,
                    "dest_addr": PhoneNumberValidator.clean(recipient.dest_addr)
                }
                for recipient in recipients
            ]
        }
    
    def _handle_response(self, response: requests.Response) -> SMSResponse:
        """Handle API response and create SMSResponse object"""
        try:
            response_data = response.json() if response.content else {}
        except ValueError:
            response_data = {}
        
        # Extract request ID if available
        request_id = response_data.get('request_id') or response.headers.get('X-Request-ID')
        
        if response.status_code == 200:
            self.logger.info(f"SMS sent successfully. Request ID: {request_id}")
            return SMSResponse(
                success=True,
                status_code=response.status_code,
                message="SMS sent successfully",
                response_data=response_data,
                request_id=request_id
            )
        elif response.status_code == 401:
            error_msg = "Authentication failed. Check your API credentials."
            self.logger.error(error_msg)
            raise AuthenticationError(error_msg)
        elif response.status_code == 429:
            error_msg = "Rate limit exceeded. Please try again later."
            self.logger.warning(error_msg)
            raise APIError(error_msg)
        else:
            error_msg = f"API request failed. Status: {response.status_code}"
            self.logger.error(f"{error_msg}. Response: {response.text}")
            return SMSResponse(
                success=False,
                status_code=response.status_code,
                message=error_msg,
                response_data=response_data,
                request_id=request_id
            )
    
    def send_sms(
        self,
        source_addr: str,
        dest_addr: Union[str, List[str]],
        message: str,
        encoding: SMSEncoding = SMSEncoding.PLAIN_TEXT
    ) -> SMSResponse:
        """
        Send SMS to one or more recipients
        
        Args:
            source_addr: Sender ID or phone number
            dest_addr: Recipient phone number(s)
            message: SMS message content
            encoding: Message encoding type
            
        Returns:
            SMSResponse object with operation results
            
        Raises:
            ValidationError: Invalid input parameters
            AuthenticationError: Authentication failed
            APIError: API request failed
            NetworkError: Network connection failed
        """
        start_time = time.time()
        
        # Normalize recipients to list
        if isinstance(dest_addr, str):
            recipients = [SMSRecipient(dest_addr)]
        else:
            recipients = [SMSRecipient(addr) for addr in dest_addr]
        
        # Validate inputs
        self._validate_message(message, encoding)
        self._validate_recipients(recipients)
        
        if not source_addr:
            raise ValidationError("Source address is required")
        
        # Prepare request
        payload = self._prepare_payload(source_addr, message, recipients, encoding)
        auth = HTTPBasicAuth(self.api_key, self.secret_key)
        
        self.logger.info(
            f"Sending SMS to {len(recipients)} recipient(s). "
            f"Message length: {len(message)} characters"
        )
        
        try:
            response = self.session.post(
                self.base_url,
                json=payload,
                auth=auth,
                timeout=self.timeout
            )
            
            result = self._handle_response(response)
            
            # Log performance metrics
            duration = time.time() - start_time
            self.logger.info(f"SMS operation completed in {duration:.2f}s")
            
            return result
            
        except requests.exceptions.Timeout:
            error_msg = f"Request timeout after {self.timeout} seconds"
            self.logger.error(error_msg)
            raise NetworkError(error_msg)
        except requests.exceptions.ConnectionError as e:
            error_msg = f"Connection failed: {str(e)}"
            self.logger.error(error_msg)
            raise NetworkError(error_msg)
        except requests.exceptions.RequestException as e:
            error_msg = f"Request failed: {str(e)}"
            self.logger.error(error_msg)
            raise APIError(error_msg)
    
    def send_bulk_sms(
        self,
        source_addr: str,
        recipients: List[str],
        message: str,
        encoding: SMSEncoding = SMSEncoding.PLAIN_TEXT,
        batch_size: int = 100
    ) -> List[SMSResponse]:
        """
        Send SMS to multiple recipients in batches
        
        Args:
            source_addr: Sender ID or phone number
            recipients: List of recipient phone numbers
            message: SMS message content
            encoding: Message encoding type
            batch_size: Number of recipients per batch
            
        Returns:
            List of SMSResponse objects for each batch
        """
        if batch_size <= 0:
            raise ValidationError("Batch size must be positive")
        
        results = []
        total_batches = (len(recipients) + batch_size - 1) // batch_size
        
        self.logger.info(
            f"Sending bulk SMS to {len(recipients)} recipients "
            f"in {total_batches} batch(es) of {batch_size}"
        )
        
        for i in range(0, len(recipients), batch_size):
            batch = recipients[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            
            self.logger.info(f"Processing batch {batch_num}/{total_batches}")
            
            try:
                result = self.send_sms(source_addr, batch, message, encoding)
                results.append(result)
                
                # Small delay between batches to respect rate limits
                if i + batch_size < len(recipients):
                    time.sleep(0.1)
                    
            except Exception as e:
                self.logger.error(f"Batch {batch_num} failed: {str(e)}")
                # Create error response for failed batch
                error_response = SMSResponse(
                    success=False,
                    status_code=0,
                    message=f"Batch {batch_num} failed: {str(e)}"
                )
                results.append(error_response)
        
        return results
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup resources"""
        if hasattr(self, 'session'):
            self.session.close()


# Convenience function for simple use cases
def send_sms(
    api_key: str,
    secret_key: str,
    source_addr: str,
    dest_addr: Union[str, List[str]],
    message: str,
    **kwargs
) -> SMSResponse:
    """
    Convenience function to send SMS without creating a client instance
    
    Args:
        api_key: Your Beem API key
        secret_key: Your Beem secret key
        source_addr: Sender ID or phone number
        dest_addr: Recipient phone number(s)
        message: SMS message content
        **kwargs: Additional arguments passed to BeemSMSClient
        
    Returns:
        SMSResponse object with operation results
    """
    with BeemSMSClient(api_key, secret_key, **kwargs) as client:
        return client.send_sms(source_addr, dest_addr, message)