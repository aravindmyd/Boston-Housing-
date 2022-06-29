from cgi import test
from urllib import response


try:
    import main
    import unittest
except Exception as e :
    print(f"Modules are missing : {e}")



class FlaskTest(unittest.TestCase):
    #Check for response 200
    def test_index(self):
        tester = main.test_client(self)
        response = tester.get("/")
        status_code = response.status_code
        self.assertEqual(status_code,200)


if __name__ == '__main__':
    unittest.main()

