from encryption.token_utils import generate_token, validate_token


def test_token_logic():
    # Token gets created
    token = generate_token(123)

    assert token

    # Token can be decoded
    decoded_token = validate_token(token)

    assert decoded_token["license_id"] == 123

    # Invalid token returns 0
    decoded_token = validate_token("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsaWNlbnNlX2lkIjoxMjN9"
                                 ".12W2ObIR9X8zGMghxmNu3iskV1nFWXqQ39qAXBq5sPp")

    assert not decoded_token
