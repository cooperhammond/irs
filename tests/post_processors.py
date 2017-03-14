from irs.ripper import Ripper
import os

print ("[*] Testing `post_processors.py`")

if not os.path.exists("test_dir"):
    os.makedirs("test_dir")
Ripper({
    "post_processors": {
        "location": "test_dir/",
        "organize": True,
    }
}).album("Da Frame 2R / Matador")

Ripper({
    "post_processors": {
        "location": "test_dir/",
        "organize": True,
    }
}).playlist("IRS Testing", "prakkillian")

print ("[+] Passed!")