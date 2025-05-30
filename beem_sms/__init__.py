"""
Beem SMS Python SDK

A professional Python package for sending SMS via Beem API.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .client import (BeemSMSClient, SMSEncoding, SMSRecipient, SMSResponse,
                     send_sms)
from .exceptions import (APIError, AuthenticationError, NetworkError, SMSError,
                         ValidationError)
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
