from rest_framework import status, views
from rest_framework.response import Response
from .models import Image
from .serializers import ImageSerializer
from PIL import Image as PILImage, ImageDraw, Image
import PIL
import base64
from io import BytesIO
from rest_framework.generics import  CreateAPIView

class ResizeImageView( CreateAPIView):
    serializer_class = ImageSerializer
    def post(self, request, *args, **kwargs):
        image_serializer = ImageSerializer(data=request.data)
        if image_serializer.is_valid():
            image = image_serializer.save()
            size = (image.width, image.height)
            shape = image.shape  
            img = PILImage.open(image.original.path)
            img = img.resize(size, PIL.Image.Resampling.LANCZOS)

            if shape == 'circle':
                img = self.crop_to_circle(img)
            elif shape == 'oval':
                img = self.crop_to_oval(img)

            processed_path = f'{image.original.path}_resized_{shape}.png'
            img.save(processed_path)
            image.processed.name = processed_path
            image.save()
            return Response(ImageSerializer(image).data, status=status.HTTP_201_CREATED)
        return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def crop_to_circle(self, img):
        mask = PILImage.new('L', img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + img.size, fill=255)
        result = PILImage.new('RGBA', img.size)
        result.paste(img, (0, 0), mask)
        return result

    def crop_to_oval(self, img):
        mask = PILImage.new('L', img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, img.size[0], img.size[1]), fill=255)
        result = PILImage.new('RGBA', img.size)
        result.paste(img, (0, 0), mask)
        return result
