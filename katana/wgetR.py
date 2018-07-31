import requests

result  = requests.get("https://sumologictest-my.sharepoint.com/:w:/g/personal/collection_sumologictest_onmicrosoft_com/Eca9n_c_44tNj8PqwH3XTaQBrA7kABYAdfHtY-f4LnGCBA?e=WyKHzE")
with open("file.html","w") as file:
    file.write( result.text)