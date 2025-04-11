# LIVE STREAM FROM WEBCAM: python detect.py --source 0 --view-img --nosave --device="mps" --vid-stride=1
# LIVE STREAM FROM YOUTUBE: python detect_owls.py --weights runs/train/exp8/weights/best.pt --source 'https://www.youtube.com/watch?v=U1GxnzDw8-w'  --nosave --device="mps"
# PRERECORDED VIDEO: python detect_owls.py --weights runs/train/exp8/weights/best.pt --source '/Volumes/owlNest22/4_2023-05d/4_2023-05-31_23-49-28_468.mkv'  --vid-stride=50 --view-img --nosave --device="mps" 
python detect_owls.py --weights runs/train/exp8/weights/best.pt --source '../../../deeplearningowls/owlstest_babies.mkv'  --vid-stride=50 --view-img --nosave --device="mps"
