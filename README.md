# CropPanoramaImage-forDL
### 원본 이미지는 8000 * 4000 등의 큰 이미지
학습할때 사용하기에는 이미지 크기 대비 오브젝트의 크기가 작아 적절하지 않음<br>
[파일명, x, y, w, h, label] 데이터를 가지는 csv와 파노라마 원본 이미지를 활용해<br>
각 오브젝트 별로 (현재는)800*800 사이즈로 크롭하고 포지션을 랜덤으로 주어 5개의 이미지를 생성함.<br>

크롭해서 생성한 이미지에 대한 csv를 생성함.<br>
크롭했을 때 이미지 안에 다른 오브젝트가 포함되어 있을 경우 threshold 이상 일때 csv에 포함시켜서 저장함.
