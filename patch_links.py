import os
import re

base_path = r"c:\Users\abdul\.gemini\antigravity\scratch\Queue iq"

# 1. Staff Login Page: Fix "Forgot Password" link
staff_login = os.path.join(base_path, 'queueiq-staff', 'index.html')
if os.path.exists(staff_login):
    with open(staff_login, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = content.replace('href="#"', 'href="javascript:void(0)" onclick="alert(\'Password reset link sent to registered email.\')"')
    if new_content != content:
        with open(staff_login, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Fixed staff login link.")

# 2. Patient App: Fix Bottom Nav active links
app_pages = ['Post_Visit_Screen.html', 'Your_Health_Brief.html', 'Token_Registration_Welcome.html', 'Symptom_Voice_Input.html']
for page in app_pages:
    path = os.path.join(base_path, 'queueiq-app', page)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Bottom nav active states don't need alerts, just prevent jump
        new_content = content.replace('href="#"', 'href="javascript:void(0)"')
        if new_content != content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Fixed {page} bottom nav.")

# 3. Analytics Page: Fix Dashboard dummy links, if any? Wait, I fixed those manually.
# Let's make sure there are no other dead button clicks inside queueiq-staff that do absolutely nothing.
