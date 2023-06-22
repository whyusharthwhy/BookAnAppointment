from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class OtpRequest(BaseModel):
    mobile: str

@app.post("/send-otp")
def send_otp(request: OtpRequest):
    url = "https://control.msg91.com/api/v5/otp"

    payload = {
        "mobile": request.mobile,
        "template_id": "62e3cf52171dae72c42aee47"  # Hardcode your template ID here
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authkey": "345051AJ1qzyS2gr5f8eb02cP1"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return {"message": "OTP sent successfully"}

@app.get("/verify-otp")
async def verify_otp(request: Request, formattedPhoneNumber: str):
    url = f"https://control.msg91.com/api/v5/otp/verify?otp=${otp}mobile=${formattedPhoneNumber}" #put the variable mobile number here
    
    headers = {
        "accept": "application/json",
        "authkey": "345051AJ1qzyS2gr5f8eb02cP1"
    }

    response = requests.get(url, headers=headers) 
    
    if response.status_code == 200:
        # OTP verification successful
        return {"message": "OTP verification successful", "mobile": mobile, "otp": otp}
    else:
        # OTP verification failed
        return {"message": "OTP verification failed"}


@app.get("/get-data")
def get_data():
    url = "http://192.168.200.32:2021/Service.asmx/GetDoctors?loc=1&depart="  # Replace with the actual API endpoint URL
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the request was not successful

        data = response.json()  # Convert the response to JSON
        return data

    except requests.exceptions.RequestException as e:
        # Handle the request exception
        return {"error": str(e)}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)

