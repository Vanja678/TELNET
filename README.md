# TELNET
A tool for scanning IP addresses and ports – designed for educational purposes in ethical hacking and cybersecurity.

# ⚠️ DISCLAIMER
This repository is for educational purposes only.

The tools and methods provided should only be used in authorized environments.

**Unauthorized use is illegal and punishable by law.**

- Always obtain explicit permission before conducting any security tests.
- The creator is not responsible for any misuse of the content.
- This project aims to enhance defensive security measures, not to cause harm.

**By using this repository, you agree to comply with all applicable laws.**

# 🔧 Prerequisites
### Enabling the Telnet Client on Windows
1. Open the **Control Panel**.
   
2. Click **Programs**.
   
3. Select **Programs and Features**.
   
4. On the left-hand side, click **Turn Windows features on or off**.
   
5. Check the box for **Telnet Client** and confirm.

# 📖 Quick Start Guide
1. **Enter the starting IP** and press Enter.
2. **Enter the ending IP** and press Enter.
3. **Select the port** to scan and press Enter.
4. The program will scan the specified IP range on the selected port.
5. Select an IP address by entering its number. The response will be saved to a **.txt** file.
6. Open the Command Prompt **(CMD)** and type:
   
   telnet {ip} {port}

   This may display some output.
7. If no output is shown:
- Try entering the IP address in your web browser.
    
- Alternatively, use **curl** in CMD:

curl {ip}

# 💡 Note
This tool is particularly useful for identifying and understanding potential security vulnerabilities. Use it responsibly and with proper authorization.



