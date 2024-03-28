<img src="images/box-dev-logo.png" 
alt= “box-dev-logo” 
style="margin-left:-10px;"
width=40%;>


# Box Webhooks and GCP functions
This project contains a workshop on integrating Box webhooks and GCP functions.


## Box configuration steps

1. Create a [Box free account](https://www.box.com/pricing/individual) if you don't already have one.
2. Complete the registration process for a Box developer account.
3. Making sure you're logged in navigate to the [Box Developer Console](https://app.box.com/developers/console). This will activate your developer account.
4. Create a new Box application. Select Custom App, fill in the form and then click Next.
5. Select Client Credentials Grant and then click Create App.
7. Check all boxes in application scopes.
    - (or only what you think will be necessary)
8. Click Save Changes.
9. Flip to the Authorization tab and submit your app for review.
10. Go to the Administrator console, and under Apps, Custom Apps Manager, authorize your app. 
9. Note the Client ID and Client Secret. You will need these later.

## Installation and configuration

### Get the code
```bash
git clone git@github.com:barduinor/box-webhooks-gcp.git
cd box-webhooks-gcp
```

### Set up your virtual environment

#### On MacOS and Linux (Python 3.12)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

##### Create your local application environment file
```bash
cp sample_oauth.env .oauth.env
```

#### On Windows CMD (Python 3.12)
```bash
python3 -m venv .venv
.venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
```

#### On Windows PowerShell (Python 3.12)
```bash
python3 -m venv .venv
.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

##### Create your local and removete application environment file
```bash
copy sample.env.local .env.local
copy sample.env.yaml .env.yaml
```

### Open the code in the code editor of your choice.
```
code .
```

`Update the CLIENT_ID, CLIENT_SECRET, ENTERPRISE_ID, and CCG_USER_ID field values in BOTH env files with the Box application client id and client secret you created on the developer console.
The webhook keys will be available when you create the webhook.`
```bash
export CLIENT_ID=YOUR_CLIENT_ID
export CLIENT_SECRET=YOUR_CLIENT_SECRET
export ENTERPRISE_ID=YOUR_ENTERPRISE_ID
export CCG_USER_ID=YOUR_USER_ID
```

```yaml
CLIENT_ID: "YOUR_CLIENT_ID"
CLIENT_SECRET: "YOUR_CLIENT_SECRET"
ENTERPRISE_ID: "YOUR_ENTERPRISE_ID"
CCG_USER_ID: "YOUR_USER_ID"
```

## Workshop

Reference the article [Working with GCP Functions and Box Webhooks](https://barbosa-rmv.medium.com/5f9a0fb2ae97), and go through the steps to complete the workshop.


### Questions
If you get stuck or have questions, make sure to ask on our [Box Developer Forum](https://forum.box.com/c/box-platform/box-workshops/50)