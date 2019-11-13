import requests
import json
import logging
import pandas as pd



BASE_URL = "https://av.cognitiveservices.azure.com/face/v1.0/"
SUBSCRIPTION_KEY  = "6df1df5e892642bbacd897ca656ff5b7"
GROUP_NAME = "avactress"
DMM_AFFILIATE_ID = "sueblocom999-999"
DMM_API_ID = "dAecCaaPMFrXcnTgXhG7"
API_END_POINT = "https://api.dmm.com/affiliate/v3/ActressSearch?api_id=" + DMM_API_ID + "&affiliate_id=" + DMM_AFFILIATE_ID + "&keyword={}" + "&output=json"

def search(name):
    end_point = API_END_POINT.format(name)
    r = requests.get(end_point)
    data = r.json()
    image_url = data["result"]["actress"][0]["imageURL"]["large"]
    link  = data["result"]["actress"][0]["listURL"]["digital"]
    return [image_url,link]


def detectFace(imageUrl):
  """
  学習済みのpersonGroupの中で、送信する画像のURLから似ている候補(candidates)を
  取得できます。
  """
  end_point = BASE_URL + "detect"
  headers = {
      "Ocp-Apim-Subscription-Key" :SUBSCRIPTION_KEY
  }
  payload = {
      "url": imageUrl
  }
  r = requests.post(
      end_point,
      json = payload,
      headers = headers
  )
  try:
      faceId = r.json()[0]["faceId"]
      print ("faceId Found:{}".format(faceId))
      return r.json()[0]
  except Exception as e:
      print("faceId not found:{}".format(e))
      return None

def identify(faceId):
   end_point = BASE_URL + "identify"
   headers = {
       "Ocp-Apim-Subscription-Key" :SUBSCRIPTION_KEY
   }
   faceIds = [faceId]
   payload = {
       "faceIds" :faceIds,
       "personGroupId" :GROUP_NAME,
       #"maxNumOfCandidatesReturned" :maxNumOfCandidatesReturned
   }
   r = requests.post(
       end_point,
       json = payload,
       headers = headers
   )
   return r.json()

def get_info(personId):
    end_point = BASE_URL + "persongroups/" + GROUP_NAME + "/persons/" + personId
    headers = {
        "Ocp-Apim-Subscription-Key" :SUBSCRIPTION_KEY
    }
    payload = {
        "personId" : personId,
        "personGroupId" :GROUP_NAME,
        #"maxNumOfCandidatesReturned" :maxNumOfCandidatesReturned
    }
    r = requests.get(
        end_point,
        json = payload,
        headers = headers
    )
    return r.json()


def main(url):
    #画像から、personを特定するときのサンプルコードです。
    
    image = url
    faceId = detectFace(image)
    person = identify(faceId["faceId"])
    if person[0]["candidates"]: #学習データに候補があれば
        personId = person[0]["candidates"][0]["personId"]
        confidence = person[0]["candidates"][0]["confidence"]
        info = get_info(personId)
        name = info["name"]
        image_url, link = search(name)
    else:
        name = "候補者なしです"
        image_url = ""
        link = ""
    return [name, image_url, link]