ALLOWED_IMAGE_EXTENSIONS = ('png', 'jpg', 'jpeg')


def allowed_image_file(filename, _return=None):
    ext = get_file_ext(filename)
    if _return == 'ext':
        return ext in ALLOWED_IMAGE_EXTENSIONS, ext
    return ext in ALLOWED_IMAGE_EXTENSIONS


def get_file_ext(filename):
    return filename.split('.')[-1]
