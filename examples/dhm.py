from sps_c.dh_mitm import (
    is_prime,
    is_primitive_root,
    find_primitive_roots,
    mod_exp,
    generate_private_key,
    generate_public_key,
    generate_shared_secret,
    encrypt_message,
    decrypt_message,
    simulate_mitm_attack,
    simulate_normal_exchange
)

def main():
    # Choose a prime number and its primitive root
    p = 23  # A small prime for demonstration
    g = 5   # A primitive root modulo 23
    
    print(f"Public parameters: prime p = {p}, generator g = {g}")
    
    # First simulate normal exchange
    simulate_normal_exchange(p, g)
    
    # Then simulate with man-in-the-middle attack
    simulate_mitm_attack(p, g)

if __name__ == "__main__":
    main()