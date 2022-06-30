import os
import sys
import time

from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback

from backend.blockchain.block import Block


# pubnub.com
subscribe_key = 'sub-c-c6ff95f5-1609-4bd6-a63f-059496eec326'
publish_key = 'pub-c-734faae7-4604-4933-8d98-be9e5c954820'

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-c6ff95f5-1609-4bd6-a63f-059496eec326'
pnconfig.publish_key = 'pub-c-734faae7-4604-4933-8d98-be9e5c954820'
pnconfig.uuid = 'blockchain-cryptocurrency-full-model'


TEST_CHANNEL = 'TEST_CHANNEL'
BLOCK_CHANNEL = 'BLOCK_CHANNEL'

CHANNELS = {
    'TEST': 'TEST',
    'BLOCK': 'BLOCK'
}


class Listener(SubscribeCallback):
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def message(self, pubnub, message_object):
        print(f'\n-- Channel: {message_object.channel} | Message: {message_object.message}')

        # check if the message is received in the BLOCK channel
        if message_object.channel == CHANNELS['BLOCK']:
            block_received = Block.from_dictionary(message_object.message)

            # append the received block to a copy of the current local chain
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block_received)

            # check if the new potential chain (which includes the received block) will replace the local chain
            try:
                self.blockchain.replace_chain(potential_chain)
                print(f'\n-- Local chain replaced successfully')
            except Exception as exception:
                print(f'\n-- Local chain was NOT replaced: {exception} ')


class PubSub():
    """
    Manages the publish/subscribe layer of the application.
    This layer provides communication capabilities between the nodes of the blockchain network.
    """
    def __init__(self, blockchain):
        """
        Constructor:
        - subscribe to CHANNELS
        - start the listener
        """
        self.pubnub = PubNub(pnconfig)

        # sends an HTTP request to PubNub.com informing that the instance pubnub is now subscribed to TEST_CHANNEL
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()

        self.my_listener = Listener(blockchain)

        self.pubnub.add_listener(self.my_listener)

    def publish(self, channel, message):
        """
        Publish a message object to the given channel
        """
        self.pubnub.publish().channel(channel).message(message).sync()

    def remove_listener(self):
        """
        Stops the listener
        """
        self.pubnub.remove_listener(self.my_listener)

    def broadcast_block(self, block):
        """
        Broadcast a block to all nodes of the blockchain network subscribed to the BLOCK channel
        """
        self.publish(CHANNELS['BLOCK'], block.to_dictionary())


def main():
    pubsub = PubSub()

    time.sleep(1)
    pubsub.publish(TEST_CHANNEL, {'foo': 'bar'})
    time.sleep(1)
    pubsub.publish(TEST_CHANNEL, {'foo': 'bar2'})
    time.sleep(1)
    pubsub.remove_listener()


if __name__ == '__main__':
    print('Main() starting')
    main()
    print('Main() finished')
    # sys.exit()
    os._exit(0)
