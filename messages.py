import re

result = 'https://exp.cdn-hotels.com/hotels/4000000/3210000/3201400/3201398/d5cfb774_{size}.jpg'

res = re.sub(r'[{size}]\w{4}\D', 'z', result)

print(res)