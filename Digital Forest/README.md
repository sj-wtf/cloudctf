This puzzle has to do with the instance metadata service and .

I can access the metadata service like this:

```bash
curl -vvv -X POST -d 'inputUrl=http://metadata.google.internal/computeMetadata/v1/project/project-id&inputHeader={"Metadata-Flavor": "Google"}' https://leaky-bucket-jobztbckaq-uc.a.run.app/result
```

I can generate an auth token with the metadata service. I can find the account email `leakybucket@optimal-jigsaw-390814.iam.gserviceaccount.com`, and generate an access token with `http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/leakybucket@optimal-jigsaw-390814.iam.gserviceaccount.com/token`

`https://cloud.google.com/compute/docs/access/create-enable-service-accounts-for-instances#applications` tells me how to use that access token

We can use this access token to list buckets and objects, which you can see in `script.py`

We can take those listed buckets and objects and download each file, which is also in `script.py`. One of those downloaded files contained the flag.
