# @Time    : 2020/11/16 9:07 下午
# @Author  : h0rs3fa11
# @FileName: image_storage.py
# @Software: PyCharm

from qiniu import Auth, put_file, etag, urlsafe_base64_encode, put_data
import qiniu.config

access_key=''
secret_key=''

q=Auth(access_key, secret_key)

bucket_name='horsepicture'

token = q.upload_token(bucket_name, None, 3600)

def image_storage(image_data):
    ret, info=put_data(token, None, image_data)
    if info.status_code==200:
        return ret.get('key')
    else:
        return ''

