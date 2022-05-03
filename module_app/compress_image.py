from PIL import Image, ImageFilter

file = ""

def apply_padding(im):
    current_width, current_height = im.size
    if current_width > current_height:
        # add vertical padding
        new_im = Image.new(im.mode,  (int(current_width), int(current_width)), (255,255,255))
        padding = int((current_width - current_height)/2)
        new_im.paste(im, (0, padding))
        return new_im
    
    elif current_width < current_height:
        # add padding on sides
        new_im = Image.new(im.mode,  (int(current_height), int(current_height)), (255,255,255))
        padding = int((current_height - current_width)/2)
        new_im.paste(im, (padding, 0))
        return new_im

    else:
        return im
        # do not pad at all

def resample_image(filepath, filename, isize, qual, blur, usePadding, destination_folder):
    im = Image.open(filepath)
    im = im.convert('RGB')
    width, height = im.size
    ratio = width/height
    isize = int(isize)


    if ratio > 1:
        # resize in width to 1200
        new_width = isize
        new_height = int(new_width/ratio)
    elif ratio < 1:
        # resize in height to 1200
        new_height = isize
        new_width = int(new_height*ratio)
    elif ratio == 1:
        new_height = isize
        new_width = isize
    if blur > 0 :
        im_resampled = im.resize((new_width, new_height), Image.Resampling.LANCZOS).filter(ImageFilter.BoxBlur(blur))
    else:
        im_resampled = im.resize((new_width, new_height), Image.Resampling.LANCZOS)
    if usePadding:
        im_padded = apply_padding(im_resampled)
        im_padded.save(destination_folder + "\\" + "res_" + filename + ".jpg", quality=qual, subsampling=0, optimize=True)
    else:
        im_resampled.save(destination_folder + "\\" + "res_" + filename + ".jpg", quality=qual, subsampling=0, optimize=True)
    print(f"Processed file {filename}.")
    return "res_" + filename + ".jpg"

