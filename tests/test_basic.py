import bot


def test_bot_module_imports():

    assert hasattr(bot, "main")
    assert callable(bot.main)


def test_payload_structure():
   
    payload = {
        "type": "text",
        "user_id": 123456,
        "username": "test_user",
        "message": "hello",
        "reply": "hi there",
    }

    # Zorunlu alanlar
    required_keys = {"type", "user_id", "username", "message", "reply"}

    assert required_keys.issubset(payload.keys())
