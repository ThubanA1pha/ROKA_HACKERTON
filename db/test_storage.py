"""
Storage 버킷 연결이 정상인지 확인하는 테스트 스크립트.
가짜 텍스트 파일 하나만 업로드해보고, 실제 사진 업로드(upload_dataset.py) 전에 연결만 검증한다.
"""
from firebase_config import get_bucket

bucket = get_bucket()
blob = bucket.blob("weapons/_test/connection_check.txt")
blob.upload_from_string("storage connection ok")

print(f"업로드 성공: {blob.name}")
print(f"버킷 이름: {bucket.name}")