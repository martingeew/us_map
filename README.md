# us_map

![Final plot](https://github.com/martingeew/us_map/blob/main/reports/figures/employment_map.png?raw=true)


## Setting Up Environment Variables

To run this project, you need to set up environment variables. Follow the steps below to create a `.env` file and add your FRED API key.

### Step 1: Obtain a FRED API Key

1. Visit the [FRED API Key Registration Page](https://fred.stlouisfed.org/docs/api/api_key.html).
2. If you do not have an account, you will need to create one by clicking on the "Register" link.
3. Once you have an account, log in and navigate to the API key registration page.
4. Follow the instructions to generate a new API key.
5. Copy the generated API key.

### Step 2: Create a `.env` File

1. In the root directory of your project, create a file named `.env`.
2. Open the `.env` file in a text editor.
3. Add the following line to the `.env` file, replacing `your_api_key_here` with the API key you copied in Step 1:

    ```properties
    FRED_API_KEY=your_api_key_here
    ```

### Step 3: Install Required Packages
Make sure you have all the required packages installed. You can install them using the following command:
```sh
pip install -r requirements.txt
```
