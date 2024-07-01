from django.shortcuts import render,redirect
from .splicing import ImageForensics as SplicingForensics
from .copymove import ImageForensics as CopyMoveForensics
from .sign import FeatureMatching
from .compression import CompressionDetector
import os

# def home(request):
#     return render(request, 'forgery_detection/paste.txt')

# # def splicing(request):
# #     if request.method == 'POST' and request.FILES.get('image'):
# #         image_file = request.FILES.get('image')
# #         splicing_forensics = SplicingForensics('splicing_model.h5', ['Forged', 'Authentic'])
# #         splicing_prediction, splicing_confidence = splicing_forensics.predict(image_file.temporary_file_path())
# #         ela_image = splicing_forensics.ela_conversion(image_file.temporary_file_path(), 90)
# #         # ... (your logic for displaying the ELA image and confidence)
# #     return render(request, 'forgery_detection/twocolumnlayout.html')
# def splicing(request):
#     if request.method == 'POST' and request.FILES.get('image'):
#         image_file = request.FILES.get('image')
#         splicing_forensics = SplicingForensics('splicing_model.h5', ['Forged', 'Authentic'])
#         splicing_prediction, splicing_confidence = splicing_forensics.predict(image_file.temporary_file_path())
#         ela_image = splicing_forensics.ela_conversion(image_file.temporary_file_path(), 90)
#         return render(request, 'forgery_detection/twocolumnlayout.html', {
#             'result': splicing_prediction,
#             'confidence': splicing_confidence,
#             'ela_image': ela_image,
#         })
#     print(ela_image)
#     return render(request, 'forgery_detection/twocolumnlayout.html')

# def copy_move(request):
#     if request.method == 'POST' and request.FILES.get('image'):
#         image_file = request.FILES.get('image')
#         copy_move_forensics = CopyMoveForensics('copymovemodel.h5', ['Forged', 'Authentic'])
#         copy_move_prediction, copy_move_confidence = copy_move_forensics.predict(image_file.temporary_file_path())
#         # ... (your logic for displaying the result and confidence)
#     return render(request, 'forgery_detection/twocolumnlayout.html')

# def signature(request):
#     if request.method == 'POST' and request.FILES.get('image'):
#         image_file = request.FILES.get('image')
#         signature_detector = FeatureMatching()
#         signature_result = signature_detector.detect_signature(image_file.temporary_file_path())
#         # ... (your logic for displaying the signature detection result)
#     return render(request, 'forgery_detection/twocolumnlayout.html')

# def compression(request):
#     if request.method == 'POST' and request.FILES.get('image'):
#         image_file = request.FILES.get('image')
#         compression_detector = CompressionDetector()
#         compression_result = compression_detector.check_compression(image_file.temporary_file_path())
#         # ... (your logic for displaying the compression detection result)
#     return render(request, 'forgery_detection/twocolumnlayout.html')



from django.shortcuts import render
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .splicing import ImageForensics as SplicingForensics
from .copymove import ImageForensics as CopyMoveForensics
from .sign import FeatureMatching
from .compression import CompressionDetector
from django.views.decorators.csrf import csrf_protect
# def home(request):
#     return render(request, 'forgery_detection/paste.txt')
from .models import Contact
@csrf_protect
def home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        contact = Contact(name=name, email=email, message=message)
        contact.save()
        return redirect('home')  # Redirect the user to the home page after saving the data
    return render(request, 'forgery_detection/paste.txt')


def splicing(request):
    #print("in splice")
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES.get('image')
        splicing_forensics = SplicingForensics('D:\\RPOOPFINAL\\image_forgery_detection\\models\\splicing_cnn_model.h5', ['Forged', 'Authentic'])
        splicing_prediction, splicing_confidence = splicing_forensics.predict(image_file)
        ela_image = splicing_forensics.ela_conversion(image_file, 90)

        # Convert the ELA image to a Django File object
        # ela_image_data = ela_image.tobytes()
        # ela_image_file = ContentFile(ela_image_data)
        # ela_image_file_name = f"ela_image_{image_file.name}"
        # ela_image_file_path = default_storage.save(ela_image_file_name, ela_image_file)
        ela_image_url = '/forgery_detection/img/ela_image.jpg'
        #print(ela_image_url)
        context = {
            'result': splicing_prediction,
            'confidence': splicing_confidence,
            'original_image': image_file,
            'ela_image_url': ela_image_url,
        }
        print(ela_image_url)
        return render(request, 'forgery_detection/twocolumnlayoutsplice.html', context)
    return render(request, 'forgery_detection/twocolumnlayoutsplice.html')

def copy_move(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES.get('image')
        copy_move_forensics = CopyMoveForensics('D:\\RPOOPFINAL\\image_forgery_detection\\models\\copymovemodel.h5', ['Forged', 'Authentic'])
        copy_move_prediction, copy_move_confidence = copy_move_forensics.predict(image_file)
        ela_image = copy_move_forensics.ela_conversion(image_file, 90)
        ela_image_url ='/forgery_detection/img/ela_image.jpg'
        # Convert the ELA image to a Django File object
        # ela_image_data = ela_image.tobytes()
        # ela_image_file = ContentFile(ela_image_data)
        # ela_image_file_name = f"ela_image_{image_file.name}"
        # ela_image_file_path = default_storage.save(ela_image_file_name, ela_image_file)
        # ela_image_url = default_storage.url(ela_image_file_path)

        context = {
            'result': copy_move_prediction,
            'confidence': copy_move_confidence,
            'original_image': image_file,
            'ela_image_url': ela_image_url,
        }
        return render(request, 'forgery_detection/twocolumnlayoutcopymove.html', context)
    return render(request, 'forgery_detection/twocolumnlayoutcopymove.html')


def signature(request):
    if request.method == 'POST' and request.FILES.get('image1') and request.FILES.get('image2'):
        image1_file = request.FILES.get('image1')
        image2_file = request.FILES.get('image2')
        image1_data = image1_file.read()
        image2_data = image2_file.read()

        signature_detector = FeatureMatching(image1_data, image2_data)
        signature_detector.preprocess_images()
        signature_detector.find_features()
        signature_detector.match_features()
        signature_detector.filter_matches()
        signature_detector.calculate_match_percentage()
        result = signature_detector.check_authenticity()

        # Convert the matched image to a Django File object
        matched_image = signature_detector.draw_matches()
        # matched_image_data = matched_image.tobytes()
        # matched_image_file = ContentFile(matched_image_data)
        # matched_image_file_name = f"matched_image_{image1_file.name}_{image2_file.name}"
        # matched_image_file_path = default_storage.save(matched_image_file_name, matched_image_file)
        matched_image_url = '/forgery_detection/img/matched.jpg'

        context = {
            'result': result,
            'matched_image_url': matched_image_url,
        }
        return render(request, 'forgery_detection/signcheck.html', context)
    return render(request, 'forgery_detection/signcheck.html')
def compression(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES.get('image')
        compression_detector = CompressionDetector()
        compression_result = compression_detector.check_compression(image_file)

        context = {
            'original_image': image_file,
            'compression_result': compression_result,
        }
        return render(request, 'forgery_detection/twocolumnlayoutcompression.html', context)
    return render(request, 'forgery_detection/twocolumnlayoutcompression.html')


# from django.shortcuts import render
# from django.core.files.base import ContentFile
# from django.core.files.storage import default_storage
# from .splicing import ImageForensics as SplicingForensics
# from .copymove import ImageForensics as CopyMoveForensics
# from .sign import FeatureMatching
# from .compression import CompressionDetector

# def home(request):
#     return render(request, 'forgery_detection/paste.txt')

# def splicing(request):
#     if request.method == 'POST' and request.FILES.get('image'):
#         image_file = request.FILES.get('image')
        
#         # Save the uploaded image locally
#         image_file_name = f"uploaded_image_{image_file.name}"
#         image_file_path = default_storage.save(image_file_name, image_file)
        
#         splicing_forensics = SplicingForensics('image_forgery_detection/models/splicing_cnn_model.h5', ['Forged', 'Authentic'])
#         splicing_prediction, splicing_confidence = splicing_forensics.predict(image_file.temporary_file_path())
#         ela_image = splicing_forensics.ela_conversion(image_file.temporary_file_path(), 90)

#         # Convert the ELA image to a Django File object
#         ela_image_data = ela_image.tobytes()
#         ela_image_file = ContentFile(ela_image_data)
#         ela_image_file_name = f"ela_image_{image_file.name}"
#         ela_image_file_path = default_storage.save(ela_image_file_name, ela_image_file)
#         ela_image_url = default_storage.url(ela_image_file_path)

#         context = {
#             'result': splicing_prediction,
#             'confidence': splicing_confidence,
#             'original_image': image_file,
#             'ela_image_url': ela_image_url,
#         }
#         return render(request, 'forgery_detection/twocolumnlayout.html', context)
#     return render(request, 'forgery_detection/twocolumnlayout.html')

# def copy_move(request):
#     if request.method == 'POST' and request.FILES.get('image'):
#         image_file = request.FILES.get('image')
        
#         # Save the uploaded image locally
#         image_file_name = f"uploaded_image_{image_file.name}"
#         image_file_path = default_storage.save(image_file_name, image_file)
        
#         copy_move_forensics = CopyMoveForensics('copymovemodel.h5', ['Forged', 'Authentic'])
#         copy_move_prediction, copy_move_confidence = copy_move_forensics.predict(image_file.temporary_file_path())
#         ela_image = copy_move_forensics.ela_conversion(image_file.temporary_file_path(), 90)

#         # Convert the ELA image to a Django File object
#         ela_image_data = ela_image.tobytes()
#         ela_image_file = ContentFile(ela_image_data)
#         ela_image_file_name = f"ela_image_{image_file.name}"
#         ela_image_file_path = default_storage.save(ela_image_file_name, ela_image_file)
#         ela_image_url = default_storage.url(ela_image_file_path)

#         context = {
#             'result': copy_move_prediction,
#             'confidence': copy_move_confidence,
#             'original_image': image_file,
#             'ela_image_url': ela_image_url,
#         }
#         return render(request, 'forgery_detection/twocolumnlayout.html', context)
#     return render(request, 'forgery_detection/twocolumnlayout.html')