import hashlib
import json


# equivalent to the lambda function in crypto_hash(*args)
def stringify(data):
        return json.dumps(data)


def crypto_hash(*args):
    """
    Return the SHA-256 hash of the input arguments
    """
    stringified_args = sorted(map(lambda data: json.dumps(data), args))

    # print(f'stringified_args: {stringified_args}')

    joined_data = ''.join(stringified_args)

    # print(f'joined_data: {joined_data}')

    return hashlib.sha256(joined_data.encode('utf-8')).hexdigest()


def main():
    print(f"crypto_hash('one', 2, '[3]'): {crypto_hash('one', 2, '[3]')}")
    print(f"crypto_hash(2, 'one', '[3]'): {crypto_hash(2, 'one', '[3]')}")


if __name__ == '__main__':
    main()