"""test moobot - all cogs"""

import asyncio
import unittest
import discord


client = None  # will become discord.Client()
# TODO: users of this testsuite: please fill in these details (or use a token)
test_server_id = ''
test_channel_id = ''
test_user = {
    'email': '',  # or username
    'password': ''
}
test_user_join_code = ''  # url or invite_code


# ==========================================================
# These tests require sending messages to test functionality
# Set the above to set where the tests will happen
# ==========================================================



# make client
def setUpModule() -> None:
    client = discord.Client()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.accept_invite(test_user_join_code))
    loop.close()

# destroy client
def tearDownModule() -> None:

    if client is not None:
        # it's probably a discord.Client then :P
        # leave the test server
        # then close the connection
        loop = asyncio.get_event_loop()
        loop.run_until_complete(client.leave_server(client.get_server(test_server_id)))
        loop.run_until_complete(client.close())
        loop.close()

    del client

class MoobotTestCase(unittest.TestCase):

    def test_moobot_is_running(self):
        raise NotImplementedError


if __name__ == '__main__':
    unittest.main()
