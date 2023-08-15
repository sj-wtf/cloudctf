#!/usr/bin/env python3

from google.cloud import storage
import requests

project_id = 'optimal-jigsaw-390814'
access_token = 'ya29.c.b0Aaekm1IGoO2FGSTaqsFh-tzCSRP_DO1po6cfF8bAj5cuCSLmwGDaoChgfUGUhAnxchCKp3sWes2JFwWGWM8fuVTsaTx69mTDc3pfsegFaEttflNA7W6zMCYRjatd064ZSmqrpUgDjJh5q2en63y5i9c3O_Fs8Tb5sqY9HcGXo-D4tqZsyt2iA9DjIluyCNG4aqrN5SLyKOfbmIbFYS1y4nmK4Wa9Fufw3TCn74wN2YzYJkSiXRG6gxue1_w-JaZTy0Tzw2ODToex8_Re3qv1Rti91EQpg3NPiZL1YFvBiPPbfdWMw-gzjNRzyAV3c4xCE3HuKCUoLWVfUcySY2gUgbG3HxEj7XZaj_1iGRyhxuHiVywOrTvrovsZ4sli_nwpR9kSpmuWeKX50bG0PlZGlWFLREMN420A9zqZiy1mi_2dj17iIajVUwqyZcRyOtM_YbrRXhZ3i_Fb5o0SMeSM0fsB3cJRsg_3xwq0Zu2kdkFsit7kfOFv538uxv5SW_kjJBxXutVOWz7RlJUhkFj9JnR6d7quJxnXVywq1kVBkXgWxxQtcgQsY-eRZRwZXfB7ZicwraYsqSiSMmvM6k8J8hmqXUWh0aMscQ-jZowqoIJowlreeZf6jW6zqxSmoSvdmhBgjze_OphS1zq0Rtzfs3u_zouwvx2M9kuZ2ukWJc8OY3YVIqmzxZV3XFfaRl-VMO98xVaRexmSwc8gb8oli1duFW9otVF5x5-Zn3Oxz3tm08JYRueX_91firZOi41mM2BXb7hZJUcbcxSzp4eMwop6cZz1cuFXbybVj-VgSan1pQ0RFlXp0UygIpwua8M6BpB7URz1oZFkpd2_J0avQ_925ezw8yhaIpuuJjM0XmI1oftxZ3do6otOXd-fbhqVsdX2lxV45oMcn6-t_lrZbXeVYWz_Yp-zopdnm0q6FQ4ZVM7OJckbpBpdFybqgaciWWrnBuyepg_sOReoB9fu8S4XtOa_w-u_V6zjXb0pWskI4a_ryv5sXFd'

def list_buckets(project_id: str, access_token: str) -> list:
    url = "https://www.googleapis.com/storage/v1/b"
    params = {"project": project_id}
    headers = {"Authorization": f"Bearer {access_token}"}

    r = requests.get(url, params=params, headers=headers)
    r.raise_for_status()

    rjson = r.json()

    bucket_names = []

    for response in r.json()['items']:
        bucket_names.append(response['name'])

    return bucket_names

def list_objects_in_buckets(project_id: str, access_token: str, bucket_names: list) -> list:
    url = "https://www.googleapis.com/storage/v1/b/"
    headers = {"Authorization": f"Bearer {access_token}"}

    buckets = []

    for bucket_name in bucket_names:
        bucket_url = url + bucket_name + '/o'

        r = requests.get(bucket_url, headers=headers)
        r.raise_for_status()

        buckets.append(r.json())

    retval = []

    for bucket_contents in buckets:
        try:
            for files in bucket_contents['items']:
                retval.append(files['mediaLink'])
        except KeyError:
            print("Nothing in bucket, moving along")
            
    
    print(retval)
    return retval

def download_all_objects(file_urls: list) -> None:
    headers = {"Authorization": f"Bearer {access_token}"}

    for file_url in file_urls:
        try:
            local_filename = file_url.split('/')[-1]
            # NOTE the stream=True parameter below
            with requests.get(file_url, stream=True, headers=headers) as r:
                r.raise_for_status()
                with open(local_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192): 
                        # If you have chunk encoded response uncomment if
                        # and set chunk_size parameter to None.
                        #if chunk: 
                        f.write(chunk)
        except requests.exceptions.HTTPError:
            print("couldn't download {}".format(file_url))

buckets = list_buckets(project_id, access_token)

print(buckets)

objects = list_objects_in_buckets(project_id, access_token, buckets)

print(objects)

download_all_objects(objects)
