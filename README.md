### OTP Auth Migration
This Python script provides a simple and effective way to parse and extract individual otpauth URIs from a single otpauth-migration URI.

When you export your two-factor authentication (2FA) accounts from an authenticator app, they are often bundled into a single, long URI. This tool allows you to take that URI, decode its contents, and generate a separate, standard otpauth URI for each individual account. This is particularly helpful for migrating your 2FA secrets to a new authenticator app that may not support bulk imports.

### Features
* Parses a given otpauth-migration URI.
* Extracts all the individual account secrets and parameters.
* Generates a list of standard otpauth URIs, one for each account.
* Handles different OTP types (TOTP and HOTP).