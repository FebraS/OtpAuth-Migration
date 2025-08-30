from urllib.parse import urlparse, parse_qs, quote_plus
from base64 import b64decode, b32encode
import migration_pb2 as otp

def getOTPAuthPerLineFromOPTAuthMigration(uri):
    try:
        url = urlparse(uri)
        if url.scheme != 'otpauth-migration':
            return []

        qs = parse_qs(url.query)
        if 'data' not in qs:
            return []

        data = b64decode(qs['data'][0])
        payload = otp.MigrationPayload.FromString(data)

        otpUris = []
        for params in payload.otp_parameters:
            # Construct the base otpauth URI
            # URL-encode name and issuer to ensure they are valid URI components
            label = f"{quote_plus(params.issuer)}:{quote_plus(params.name)}" if params.issuer else quote_plus(params.name)
            base_uri = f"otpauth://totp/{label}"

            # Add query parameters
            queryParams = {
                'secret': b32encode(params.secret).decode('utf-8').replace('=', ''),
                'issuer': params.issuer,
                'algorithm': otp.Algorithm.Name(params.algorithm).lower(), # Chaned to lower case
                'digits': str(params.digits), # Changed to str
            }
            if params.type == otp.OtpType.HOTP:
                queryParams['counter'] = params.counter
            
            # Build the full URI string
            queryString = "&".join([f"{key}={value}" for key, value in queryParams.items() if value])
            fullUri = f"{base_uri}?{queryString}"
            otpUris.append(fullUri)

        return otpUris

    except Exception as e:
        print(f"An error occurred: {e}")
        return []
