# OTP Auth Migration
This Python script provides a simple and effective way to parse and extract individual otpauth URIs from a single otpauth-migration URI.

When you export your two-factor authentication (2FA) accounts from an authenticator app, they are often bundled into a single, long URI. This tool allows you to take that URI, decode its contents, and generate a separate, standard otpauth URI for each individual account. This is particularly helpful for migrating your 2FA secrets to a new authenticator app that may not support bulk imports.

## Features
* Parses a given otpauth-migration URI.
* Extracts all the individual account secrets and parameters.
* Generates a list of standard otpauth URIs, one for each account.
* Handles different OTP types (TOTP and HOTP).

## How To Use
This Python function, getOTPAuthPerLineFromOPTAuthMigration, is designed to extract individual otpauth:// URIs from a Google Authenticator migration URI.  You can use it by simply passing a migration URI string as an argument, and it will return a list of standard otpauth URIs, one for each account contained in the migration data.

For example, if you have a Google Authenticator QR code that exports multiple accounts, the URI encoded in that QR code can be processed by this function.

To use the getOTPAuthPerLineFromOPTAuthMigration function, you'll need to follow these steps:

Obtain the Migration URI: Get the otpauth-migration:// URI. This is typically obtained by exporting your accounts from the Google Authenticator app on a device. The app generates a QR code that contains this URI.

Pass the URI to the Function: Call the function with the migration URI string as the sole argument.

Process the Output: The function will return a list of strings, where each string is a standard otpauth:// URI representing an individual TOTP (Time-based One-Time Password) or HOTP (HMAC-based One-Time Password) account.

Here's a simple example of how to use it in your Python code:

```python

from urllib.parse import urlparse, parse_qs, quote_plus
from base64 import b64decode, b32encode
import migration_pb2 as otp

# Real URIs will have a long, complex 'data' parameter.
migration_uri = "otpauth-migration://offline?data=A..." 

# Call the function to get the individual OTP URIs
individualOtpUris = getOTPAuthPerLineFromOPTAuthMigration(migration_uri)

# Print the results
if individualOtpUris:
    for uri in individualOtpUris:
        print(uri)
else:
    print("Failed to get any OTP URIs from the migration URI.")

```
## What the Function Does
The function works by:

1. Parsing the URI: It first checks if the URI is a valid otpauth-migration scheme.

2. Decoding the Data: It extracts the data parameter from the query string, which is a Base64-encoded string. It then decodes this string.

3. Deserializing the Protobuf Payload: The decoded data is then parsed using the migration_pb2.MigrationPayload object. This is a crucial step as it understands the structure of the data exported by Google Authenticator.

4. Constructing Individual URIs: It iterates through each otp_parameters entry within the payload. For each entry, it takes the secret key, issuer, account name, algorithm, and digits, and constructs a new, standard otpauth:// URI.

5. Handling HOTP: If the account type is HOTP, it also adds the counter parameter to the URI.

6. Returning the List: Finally, it returns a list containing all the newly created otpauth:// URIs. Each URI in the list can be used to add a single account to an authenticator app.