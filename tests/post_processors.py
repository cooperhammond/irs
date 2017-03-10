from irs.ripper import Ripper
import os

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