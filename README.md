# Data Analyzer
Data Analyzer is a market data analysis tool meant for day/swing traders which utilizes the polygon.io data tool as well as TD Ameritrades APIs to create a customizable backtesting software. The primary usage of the software is to take lists of stock symbols from a specific date, pull data about that list for certain times, and filter the list based on certain criteria, as well as calculate success rates based on certain inputs. A secondary use case is to make the active trading process easier for traders who use a time-based strategy.
## Installation & Setup
### Installing Versions
To install a version, simply:
- Go to the releases section of this GitHub page
- Choose the latest version's installer file. Download it and run the installer (named `DataAnalyzerInstallerXXX.exe`), which will install to your `Program Files (x86)` directory by default
  - *Note: it is highly recommended to keep this as the installation directory. If you do not, see the next section to obtain your `td_auth.txt` file.*
- If this is first time installing the software (i.e. you are not updating):
  - See the next section for setting up your authentication file

### Setting up your TD Authentication File
If this is your first install, complete the following steps to properly authenticate yourself into the TD Ameritrade system to allow Data Analyzer to place automated trades for you. If you do not have a TD Ameritrade trading acount or would not like to give this permission to Data Analyzer, skip these steps and go to the next subsection.
- From the releases page, download and run the `DACrypter.exe` file
- Get your TD account number from [https://invest.ameritrade.com/](https://invest.ameritrade.com/) or directly from the thinkorswim application; make sure this is the account you want to trade through DataAnalyzer with; paste the account number into the first field in the software
- Click **Generate Refresh Token**, login into your TD Ameritrade account, complete any verification required, and choose **Allow**. The program should read `[REFRESH TOKEN CAPTURED]`
- Click **Create Auth File**. This will generate a customized file named `td_auth.txt` and place it in your `Data Analyzer` app directory. **Do not** share this file: it can be used to trade from your TD account

*Note: If you chose to install to different directory then the default, complete the following steps:*
- Create a temporary subdirectory in your `Program Files (x86)` folder called `Data Analyzer`, and make a directory in that called `App`.
- Complete the steps directly above - the `td_auth.txt` file will be generated in this temporary directory. 
- Copy the `td_auth.txt` file into the chosen install directory. Make sure it is copied *into* the `App` folder

*Note: if you do not want to use the TD automated trading feature/authenticate with TD, follow the steps below instead of the above:*
- Open your install directory - if you used the default, it will be in your `Program Files (x86)` folder
- Open the `App` subdirectory, and place a *blank* text file here named `td_auth.txt`.
  - *Note that the software **will not** run without this step*
  
You only need to complete these steps upon the first installation, not every time you update. Note that the custom refresh token that you generated using DACrypter will expire every 90 days - in other words, you should reopen DACrypter and redo the above steps every 90 days to make sure you can continue using the software properly.

## Usage & Examples
### Getting Started
The most basic use of Data Analyzer is as follows:
