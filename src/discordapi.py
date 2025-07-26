from kivy.logger import Logger

import requests
from typing import List

TAG = "DBDiscordAPI" + ": "

def getMPOfUrls(token: str, applicationId: int, urls: List[str]) -> List[str]:
    requestTo = f"https://discord.com/api/v9/applications/{applicationId}/external-assets"
    Logger.debug(TAG + f"Sending POST to {requestTo}")
    externalAssetsReq = requests.post(
        requestTo,
        headers = {"Authorization": token},
        json = {"urls": urls}
    )

    if externalAssetsReq.status_code != 200:
        Logger.error(TAG + f"Error while getting media proxy of urls, got {externalAssetsReq.status_code}\nText:\n{externalAssetsReq.text}")
        return
    
    return ["mp:" + i["external_asset_path"] for i in externalAssetsReq.json()]

def getUsername(token: str) -> str:
    requestTo = "https://discord.com/api/v9/users/@me"
    Logger.debug(TAG + f"Sending GET to {requestTo}")
    userInfoReq = requests.get(
        requestTo,
        headers = {"Authorization": token}
    )

    if userInfoReq.status_code != 200:
        Logger.error(TAG + f"Error while getting username, got {userInfoReq.status_code}\nText:\n{userInfoReq.text}")
        return  
    
    return userInfoReq.json()["username"]

def logout(token: str):
    # basically make the token useless
    requestTo = "https://discord.com/api/v9/auth/logout"
    Logger.debug(TAG + f"Sending POST to {requestTo}")
    logoutReq = requests.post(
        requestTo,
        json = {"provider": None, "voip_provider": None},
        headers = {"Authorization": token}
    )