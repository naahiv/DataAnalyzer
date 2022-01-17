# TD Data Analyzer
## Instructions for Authentication setup
Necessities:
- A TD Ameritrade (bank) account
- A TD developer account: register at <https://developer.tdameritrade.com/>.
- The latest TD Data Analyzer software zip file

#### Obtaining your API key
- If you do not already have an App setup in your developer account, create one by following the standard wizard on the developer webpage. <http://localhost:8000/> can be used as a URL if needed.
- Next, your product id can be found under the App page, which is your API key.
- Store this for later.

#### Obtaining your OAuth 2.0 Token
- Once logged in to your developer account, choose a random TD API, and click the `Set` button at the bottom of the screen under OAuth 2.0.
- Log in with your TD bank account details.
- Click `Request` and then `Send`, and your token, beginning with `Bearer DK89FI24JRE...`, will appear.
- Store this for later.

#### Generating your `td_auth.txt` verification file.
- Your API key and OAuth 2.0 token are stored locally in encrypted form to maximize security.
- Open the executable labeled DACrypter and paste the key and token.
- Click Encrypt. A file should appear in the directory which DACrypter is called `td_auth.txt`; save this file securely and do not share with anyone. The developer will *not* ask to see this file for debugging purposes.
- Delete DACrypter once this is complete.

## Installing Versions
To install a version, simply go to the releases section of this GitHub page, and choose the latest version's installer file. Download it and run the installer, which will install in your `Program Files (x86)` directory by default. If this is your first time using the software, open this directory, then open `App`, and place your `td_auth.txt` file here. Installing future versions will not require this step.
