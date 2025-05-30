"""
Beem SMS Python SDK

A professional Python package for sending SMS via Beem API.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .client import (
    BeemSMSClient,
    SMSResponse,
    SMSRecipient,
    SMSEncoding,
    send_sms,
)
from .exceptions import (
    SMSError,
    AuthenticationError,
    ValidationError,
    APIError,
    NetworkError,
)
from .validators import PhoneNumberValidator

__all__ = [
    "BeemSMSClient",
    "SMSResponse", 
    "SMSRecipient",
    "SMSEncoding",
    "send_sms",
    "SMSError",
    "AuthenticationError",
    "ValidationError", 
    "APIError",
    "NetworkError",
    "PhoneNumberValidator",
]