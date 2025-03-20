
import time
import btc_keys


def find_vanity(vanity_words: list):
    iteration = 0
    start_time = time.time()
    last_check_speed_time = start_time

    while True:
        private_key, p2pkh_address = btc_keys.generate_key_pair()
        
        # Check if the address starts with any of the vanity words
        for vanity_word in vanity_words:
            if p2pkh_address.startswith('1' + vanity_word):
                end_time = time.time()
                elapsed_time = end_time - start_time
                checks_per_second = iteration / elapsed_time
                print(f"Vanity address found after {iteration} iterations and {elapsed_time:.2f} seconds!")
                print(f"Checks per second: {checks_per_second:.2f}")
                print(f"Vanity Word: {vanity_word}")
                print("Private Key:", private_key)
                print("P2PKH Address:", p2pkh_address)
                return  # Exit the function after finding a match
        
        iteration += 1
        current_time = time.time()
        
        if current_time - last_check_speed_time >= 10.0:  # Print checks per second every 10 seconds
            elapsed_time = current_time - start_time
            checks_per_second = iteration / elapsed_time
            print(f"Iteration: {iteration}, Checks per second: {checks_per_second:.2f}")
            last_check_speed_time = current_time

        if iteration > 100000:
            end_time = time.time()
            elapsed_time = end_time - start_time
            checks_per_second = iteration / elapsed_time
            print(f"No vanity address found within the iteration limit of {iteration} iterations.")
            print(f"Total time: {elapsed_time:.2f} seconds")
            print(f"Checks per second: {checks_per_second:.2f}")
            break


#--------------------------------------------------------------------------
# main
#--------------------------------------------------------------------------

if False:
    vanity_words = ['Bitcoin', 'BitcoinWallet', 'bitcoin', 'Nick', 'Kane', 'NickKane', 'Coffee', 'coffee']
    find_vanity(vanity_words)

if True:
    for tj in range(0, 1):
        wif, p2pkh = btc_keys.generate_key_pair()
        print(wif, p2pkh)

