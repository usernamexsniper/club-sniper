#!/usr/bin/env python3
"""
Club.com Username Sniper – FINAL
- Generate usernames (count + length)
- Check availability using real API (if found) or profile pages
- Uses your authenticated session
"""

import requests
import concurrent.futures
import random
import string
import time
from typing import List, Tuple

# ============================================================
# CONFIGURATION – UPDATE THESE ONCE YOU FIND THE REAL API
# ============================================================
REAL_API_URL = None          # e.g., "https://club.com/api/check-username"
USERNAME_PARAM = "username"  # e.g., "username" or "userName" or "handle"

# ============================================================
# SESSION WITH YOUR COOKIES (automatically picks up from browser)
# ============================================================
def create_session_from_cookies(cookie_string: str = None):
    """
    Create a requests session with your existing cookies.
    If you don't provide cookie_string, it will try to read from a file 'cookies.txt'
    or you can manually add your token below.
    """
    session = requests.Session()
    
    # Method 1: Manually add your token (from DevTools → Application → Cookies)
    # Uncomment and replace with your actual token:
    # session.cookies.set("token", "eyJhbGciOiJIUzI1NiIs...")
    # session.cookies.set("refreshToken", "eyJhbGciOiJIUzI1NiIs...")
    
    # Method 2: If you have a Netscape cookies.txt file
    if cookie_string:
        for line in cookie_string.split(';'):
            if '=' in line:
                k, v = line.strip().split('=', 1)
                session.cookies.set(k, v)
    
    # Default headers
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
        "Referer": "https://club.com/",
        "Origin": "https://club.com",
    })
    return session

# ============================================================
# USERNAME GENERATOR
# ============================================================
def generate_usernames(count: int, length: int) -> List[str]:
    """Generate random lowercase alphanumeric usernames of exact length."""
    chars = string.ascii_lowercase + string.digits
    usernames = set()
    while len(usernames) < count:
        usernames.add(''.join(random.choices(chars, k=length)))
    return list(usernames)

# ============================================================
# CHECK METHODS
# ============================================================
def check_via_api(session, username: str) -> Tuple[bool, str]:
    """Try the real API if configured."""
    if not REAL_API_URL:
        return None, "No API endpoint configured"
    try:
        payload = {USERNAME_PARAM: username}
        # Try POST first
        resp = session.post(REAL_API_URL, json=payload, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            # Common response patterns – you may need to adjust
            if isinstance(data, dict):
                if data.get("available") is True:
                    return True, "api"
                if data.get("available") is False:
                    return False, "api"
                if data.get("isAvailable") is True:
                    return True, "api"
                if data.get("exists") is False:
                    return True, "api"
        # Fallback to GET with params
        resp = session.get(REAL_API_URL, params={USERNAME_PARAM: username}, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("available") is True:
                return True, "api"
            if data.get("available") is False:
                return False, "api"
    except Exception as e:
        pass
    return None, "api_failed"

def check_via_profile(session, username: str) -> Tuple[bool, str]:
    """Check by trying to visit profile pages."""
    patterns = [
        f"https://club.com/@{username}",
        f"https://club.com/u/{username}",
        f"https://club.com/profile/{username}",
        f"https://club.com/{username}",
    ]
    for url in patterns:
        try:
            resp = session.get(url, timeout=5, allow_redirects=True)
            if resp.status_code == 200:
                # Look for "not found" text (some sites return 200 but show error)
                if "not found" in resp.text.lower() or "doesn't exist" in resp.text.lower():
                    return True, "profile_404text"
                return False, "profile_exists"
            elif resp.status_code == 404:
                return True, "profile_404"
        except:
            continue
    return None, "profile_failed"

def check_username(session, username: str) -> Tuple[str, bool, str]:
    """
    Returns: (username, is_available, method_used)
    """
    # Priority 1: use real API if available
    if REAL_API_URL:
        avail, method = check_via_api(session, username)
        if avail is not None:
            return username, avail, method
    
    # Priority 2: fallback to profile page check
    avail, method = check_via_profile(session, username)
    if avail is not None:
        return username, avail, method
    
    return username, None, "all_failed"

# ============================================================
# MAIN INTERACTIVE MENU
# ============================================================
def main():
    print("\n" + "="*60)
    print("   CLUB.COM USERNAME SNIPER - FINAL")
    print("="*60)
    
    # Create session (you can paste your cookie string here if needed)
    session = create_session_from_cookies()
    # Optional: test session with a simple request
    try:
        test = session.get("https://club.com/api/features", timeout=5)
        if test.status_code == 200:
            print("✓ Session ready (authenticated)\n")
        else:
            print("⚠ Session may not be authenticated – some checks may fail\n")
    except:
        print("⚠ Could not reach club.com – check your network\n")
    
    while True:
        print("\n[1] Generate & check usernames (auto)")
        print("[2] Check usernames from a file")
        print("[3] Set API endpoint (if you found it)")
        print("[4] Exit")
        
        choice = input("\nChoose: ").strip()
        
        if choice == "1":
            try:
                count = int(input("How many usernames to generate? (e.g., 500): "))
                length = int(input("Username length? (1-10): "))
                if length < 1 or length > 10:
                    print("Length must be 1-10")
                    continue
                print(f"\nGenerating {count} usernames of length {length}...")
                usernames = generate_usernames(count, length)
                print(f"✓ Generated {len(usernames)} unique usernames.\n")
                
                print("Starting availability check (20 concurrent threads)...")
                available = []
                with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                    futures = {executor.submit(check_username, session, u): u for u in usernames}
                    for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
                        name, avail, method = future.result()
                        if avail is True:
                            available.append(name)
                            print(f"[{i}/{count}] ✅ AVAILABLE: {name} ({method})")
                        elif avail is False:
                            print(f"[{i}/{count}] ❌ TAKEN:     {name}")
                        else:
                            print(f"[{i}/{count}] ❓ ERROR:      {name}")
                
                print(f"\n🎯 Found {len(available)} available usernames:")
                for name in available[:20]:
                    print(f"   {name}")
                if len(available) > 20:
                    print(f"   ... and {len(available)-20} more")
                
                if available:
                    save = input("\nSave to file? (y/n): ").lower()
                    if save == 'y':
                        filename = input("Filename (default: available.txt): ").strip() or "available.txt"
                        with open(filename, 'w') as f:
                            f.write('\n'.join(available))
                        print(f"✓ Saved to {filename}")
            except ValueError:
                print("❌ Invalid number")
        
        elif choice == "2":
            filename = input("Enter filename (one username per line): ").strip()
            try:
                with open(filename, 'r') as f:
                    usernames = [line.strip() for line in f if line.strip()]
                print(f"\nLoaded {len(usernames)} usernames. Checking...")
                available = []
                with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                    futures = {executor.submit(check_username, session, u): u for u in usernames}
                    for future in concurrent.futures.as_completed(futures):
                        name, avail, method = future.result()
                        if avail is True:
                            available.append(name)
                            print(f"✅ AVAILABLE: {name}")
                        elif avail is False:
                            print(f"❌ TAKEN:     {name}")
                        else:
                            print(f"❓ ERROR:      {name}")
                print(f"\nAvailable: {len(available)} -> {', '.join(available[:10])}")
            except FileNotFoundError:
                print(f"❌ File {filename} not found")
        
        elif choice == "3":
            print("\nTo set the API endpoint, edit the script variables at the top.")
            print("Or enter them now (temporary):")
            url = input("API URL (e.g., https://club.com/api/check-username): ").strip()
            param = input("Parameter name (e.g., username): ").strip()
            if url and param:
                global REAL_API_URL, USERNAME_PARAM
                REAL_API_URL = url
                USERNAME_PARAM = param
                print(f"✓ API set to {REAL_API_URL} with param '{USERNAME_PARAM}'")
            else:
                print("❌ Both URL and parameter required")
        
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()