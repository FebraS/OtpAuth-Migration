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
migrationUri = "otpauth-migration://offline?data=A..." 

# Call the function to get the individual OTP URIs
individualOtpUris = getOTPAuthPerLineFromOPTAuthMigration(migrationUri)

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


## Explanation of the migration.proto File
The migration.proto file is a Protocol Buffers (Protobuf) schema. Protobuf is a method used by Google to serialize structured data. This schema defines the structure of the data that's encoded within the data parameter of the otpauth-migration URI.

### message MigrationPayload
This is the main message that holds all the exported data.

* **repeated OtpParameters otp_parameters = 1;**: This is the most important field. repeated means it's a list of OtpParameters objects. Each OtpParameters object represents a single account (e.g., your Google account, your GitHub account) within the Authenticator app.

* **optional int32 version = 2;**: Indicates the version of the migration format.

* **optional int32 batch_size = 3;**: The total number of batches if the data is split into multiple parts.

* **optional int32 batch_index = 4;**: The index of the current batch.

* **optional int32 batch_id = 5;**: A unique identifier for the entire migration process.

### message OtpParameters
This message defines the parameters for a single OTP account.

* **optional bytes secret = 1;**: The secret key used to generate the OTP codes. This is typically a Base32-encoded string when presented in a standard otpauth URI.

* **optional string name = 2;**: The name of the account, such as an email address or username.

* **optional string issuer = 3;**: The service provider (e.g., "Google" or "GitHub").

* **optional Algorithm algorithm = 4;**: The hash algorithm used (e.g., SHA1, SHA256).

* **optional DigitCount digits = 5;**: The number of digits in the generated code (e.g., 6 or 8).

* **optional OtpType type = 6;**: The type of OTP, either TOTP (Time-based One-Time Password) or HOTP (HMAC-based One-Time Password).

* **optional int64 counter = 7;**: This field is only used for HOTP accounts. It is a counter that increments each time a new code is generated.

### enum Algorithm
This enumeration defines the supported hashing algorithms. The values 1, 2, 3, and 4 correspond to the standard algorithms SHA1, SHA256, SHA512, and MD5, respectively.

### enum DigitCount
This enumeration specifies the number of digits in the generated OTP code, with SIX and EIGHT being the most common values.

### enum OtpType
This enumeration distinguishes between the two types of OTPs:

* HOTP: Uses an incrementing counter.

* TOTP: Uses the current time as a factor.

## What is migration_pb2.py?
The migration_pb2.py file is a Python module automatically generated by the Protocol Buffers (Protobuf) compiler.