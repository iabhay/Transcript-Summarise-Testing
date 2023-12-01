import pytest
from unittest.mock import patch
from src.utils.input_validator import username_validation, password_validation, url_validation, pattern_ret

@patch('src.utils.input_validator.pattern_ret')
def test_username_validation_pass(mock_pattern_ret):
    mock_pattern_ret.return_value = "^([A-z0-9@_\-\.]{4,20})"
    res = username_validation("dfgjhkkj")
    assert res == True
    

@pytest.mark.parametrize("username, expected_result", [("abcde",True), pytest.param("abc",False, marks=pytest.mark.xfail(reason="Meri Marji"))])
def test_username_by_pytest(username,expected_result):
    assert username_validation(username) == expected_result
    
@pytest.mark.parametrize("password, expected_result", [("abc", False), ("123", False), ("abc123", False), ("abc123!@#", False), ("abc123!@#ABC", True), ("abc123!@#ABCabc123!@#ABC", False), ("#ABCabc123!@#ABC", True)])
def test_password_by_pytest(password,expected_result):
    assert password_validation(password) == expected_result
    
# url_test_cases = [
#                     ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", True),
#                     ("https://youtube.com/watch?v=dQw4w9WgXcQ", True),
#                     ("http://www.youtube.com/watch?v=dQw4w9WgXcQ", True),
#                     ("www.youtube.com/watch?v=dQw4w9WgXcQ", False),
#                     ("youtube.com/watch?v=dQw4w9WgXcQ", False),
#                     ("https://youtu.be/dQw4w9WgXcQ", True),
#                     ("youtu.be/dQw4w9WgXcQ", False),
#                     ("http://youtu.be/dQw4w9WgXcQ", True),
#                     ("www.youtu.be/dQw4w9WgXcQ", False),
#                     ("https://youtube.com/embed/dQw4w9WgXcQ", True),
#                     ("youtube.com/embed/dQw4w9WgXcQ", False),
#                     ("https://www.youtube.com/channel/UCBR8-60-B28hp2BmDPdntcQ", True),
#                     ("https://youtube.com/channel/UCBR8-60-B28hp2BmDPdntcQ", True),
#                     ("www.youtube.com/channel/UCBR8-60-B28hp2BmDPdntcQ", False),
#                     ("youtube.com/channel/UCBR8-60-B28hp2BmDPdntcQ", False),
#                     ("https://www.youtube.com/user/username", True),
#                     ("https://youtube.com/user/username", True),
#                     ("www.youtube.com/user/username", False),
#                     ("youtube.com/user/username", False),
#                     ("https://www.youtube.com/playlist?list=PLA7ZcagI0frCq0zKz_LbUdL5FQgJLkDB9", True),
#                     ("https://youtube.com/playlist?list=PLA7ZcagI0frCq0zKz_LbUdL5FQgJLkDB9", True),
#                     ("youtube.com/playlist?list=PLA7ZcagI0frCq0zKz_LbUdL5FQgJLkDB9", False),
#                     ("https://m.youtube.com/watch?v=dQw4w9WgXcQ", True),
#                     ("m.youtube.com/watch?v=dQw4w9WgXcQ", True),
#                     ("https://youtu.be", False),
#                     ("https://youtube.com/watchv=dQw4w9WgXcQ", False),
#                     ("http://www.youtu.be.com/dQw4w9WgXcQ", False),
#                     ("youtube/watch?v=dQw4w9WgXcQ", False),
#                     ("https://www.youtube/watch?v=dQw4w9WgXcQ", False),
#                     ("https://youtube.com/watch?video=dQw4w9WgXcQ", False),
#                     ("https://www.youtubedotcom/watch?v=dQw4w9WgXcQ", False),
#                     ("www-youtube.com/watch?v=dQw4w9WgXcQ", False),
#                     ("youtube.comwatch?v=dQw4w9WgXcQ", False),
#                     ("htp://www.youtube.com/watch?v=dQw4w9WgXcQ", False),
#                     ("https:/youtube.com/watch?v=dQw4w9WgXcQ", False),
#                     ("https://www.youtubecom/watch?v=dQw4w9WgXcQ", False),
#                     ("https://www.youtube.com/watch?", False),
#                     ("https://www.youtube.com/watch", False),
#                     ("https://www.youtube.com/watch?=dQw4w9WgXcQ", False),
#                     ("https://www.youtube.com/watch?video=dQw4w9WgXcQ", False),
#                     ("https://www.youtube.com/watch?v=", False),
#                     ("https://www.you.tube.com/watch?v=dQw4w9WgXcQ", False),
#                     ("https://youtube.com /watch?v=dQw4w9WgXcQ", False),
#                     ("https://www.youtube/watch?v=dQw4w9WgXcQ", False),
#                     ("https://www.youtube.com/v/dQw4w9WgXcQ", True),
#                     ("https://www.youtube.com/watch#v=dQw4w9WgXcQ", False),
#                     ("https://www.youtube.com?watch=v=dQw4w9WgXcQ", False),
#                     ("www.youtube.com/watch?v=dQw4w9WgXcQ&feature=youtu.be", True),
#                     ("https://www.youtubecom/watch?v=dQw4w9WgXcQ", False),
#                     ("https://www.youtube.com/watch?v=dQw4w9WgXc", True)
                        # ("www.youtu.be/watch?v=abcd1234", False),
                        # ("https://youtube.com/watch?v=", False),
                        # ("youtube.com/watch?v=ab!cd1234", False),
                        # ("https://youtube.com/watch?v=ab cd1234", False),
                        # ("www.youtube.com/watch?v=abc", False),
                        # ("youtube.com/watch?v=abcd123", False),
                        # ("https://www.youtube.com/watch?=abcd1234", False),
                        # ("https://youtube.com/watchv=abcd1234", False),
                        # ("www.youtube.com/watch?v=abcd12345&feature=youtu.be", False),
                        # ("youtube.com/watch?v=abcd1234#t=10s", False),
                        # ("https://www.youtu.be/watch?v=abcd1234", False),
                        # ("https://youtube.com/watch=abcd1234", False),
                        # ("www.youtube.comwatch?v=abcd1234", False),
                        # ("youtube.com/watch?v=123", False),
                        # ("https://www.youtube.com/watch?abcd1234", False),
                        # ("https://youtube.com/watch?v=abcd_1234%", False),
                        # ("www.youtube.com/watch?v=abcd-1234$", False),
                        # ("youtube.com/watch?v=abcd1234&list=PLA", False),
                        # ("https://www.youtube.com/watch?v=", False),
                        # ("https://youtube.com/watch?v=1234abcd?", False),
                        # ("www.youtube.com/watch?v=abcd_1234!", False),
                        # ("youtube.com/watch?video=abcd1234", False),
                        # ("https://www.youtube.com/watch#v=abcd1234", False),
                        # ("https://youtube.com /watch?v=abcd1234", False),
                        # ("www.youtube.com/watch?v=abcd1234?list=PL312", False),
                        # ("https://www.youtube.com/watch?v=abcd1234", False),
                        # ("https://youtube.com/watch?v=abcd_1234", False),
                        # ("www.youtube.com/watch?v=abcd-1234", False),
                        # ("youtube.com/watch?v=abcdABCD", False),
                        # ("https://www.youtube.com/watch?v=1234abcd", False),
                        # ("http://youtube.com/watch?v=1234_abcd", False),
                        # ("https://www.youtube.com/watch?v=abcd-ABCD", False),
                        # ("https://www.youtube.com/watch?v=1234-5678", False),
                        # ("http://www.youtube.com/watch?v=_abcd1234", False),
                        # ("youtube.com/watch?v=abcd1234", False),
                        # ("https://youtube.com/watch?v=ABCDabcd", False),
                        # ("www.youtube.com/watch?v=1234ABCD", False),
                        # ("youtube.com/watch?v=abcd-1234", False),
                        # ("https://www.youtube.com/watch?v=abcD1234", False),
                        # ("https://youtube.com/watch?v=1234abcd", False),
                        # ("www.youtube.com/watch?v=abcd_1234", False),
                        # ("youtube.com/watch?v=ABCD-1234", False),
                        # ("https://www.youtube.com/watch?v=1234_ABCD", False),
                        # ("https://youtube.com/watch?v=abcd1234", False),
                        # ("www.youtube.com/watch?v=1234abcd", False),
                        # ("youtube.com/watch?v=abcd1234ABCD", True),
                        # ("https://www.youtube.com/watch?v=_ABCD1234", False),
                        # ("https://youtube.com/watch?v=1234-abcd", False),
                        # ("www.youtube.com/watch?v=abcd1234_", False),
                        # ("youtube.com/watch?v=abcd1234-", False)
                        # ("https://www.youtube.com/watch?v=1a2B3c4D5eF", True),
                        # ("https://youtube.com/watch?v=1a2B3c4D5eF", True),
                        # ("www.youtube.com/watch?v=1a2B3c4D5eF", True),
                        # ("youtube.com/watch?v=1a2B3c4D5eF", True),
                        # ("https://www.youtube.com/watch?v=gH7dMb9s8gg", True),
                        # ("https://www.youtube.com/watch?v=_aBcDeFgH12", True),
                        # ("www.youtube.com/watch?v=-aB1cD2eF3g", True),
                        # ("youtube.com/watch?v=aB1cD2eF3gH", True),
                        # ("https://youtube.com/watch?v=1A2b3C4d5E6", True),
                        # ("https://www.youtube.com/watch?v=ghIj_123456", True),
                        # ("www.youtube.com/watch?v=abcdefABCDEF", True),
                        # ("youtube.com/watch?v=1234567890A", True),
                        # ("https://www.youtube.com/watch?v=a-Bc_dEfGhi", True),
                        # ("https://youtube.com/watch?v=AbCdEfGhIjk", True),
                        # ("www.youtube.com/watch?v=LmNoPqRsTuV", True),
                        # ("youtube.com/watch?v=WxYzZ_aBcDe", True), 
#                 ]

url_test_cases = [
                    
                    ("https://www.youtube.com/watch?v=fG1_h2IJKlM", True),
                    ("https://youtube.com/watch?v=nOpQ_W_4Z5U", True),
                    ("www.youtube.com/watch?v=VwXy_tU1234", True),
                    ("youtube.com/watch?v=1a2B_3c4D5e", True)
]
    
@pytest.mark.parametrize("url, expected_result", url_test_cases)
def test_url_by_pytest(url,expected_result):
    assert url_validation(url) == expected_result
