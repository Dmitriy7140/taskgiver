
from dotenv import load_dotenv
def test_phone_numbers_format():

    PHONE_NUMBERS = "+aaa,+bbb,+ccc"


    assert [i for i in PHONE_NUMBERS.split(",")] == ["+aaa", "+bbb", "+ccc"]