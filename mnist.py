import random

training  = 0
imagefile = "train-images-idx3-ubyte" if training else "t10k-images-idx3-ubyte"
labelfile = "train-labels-idx1-ubyte" if training else "t10k-labels-idx1-ubyte"

def bytelist_to_uint(bytelist):
    val = 0
    for b in bytelist :
        val = val * 256 + b
    return val

def read_idx_file(filename, imgs_to_read=0):
    with open(filename, 'rb') as f:
        bytelist = f.read()
        assert(bytelist[0:2] == bytes([0,0])) # Magic value.
        datatype = bytelist[2]
        num_dims = bytelist[3]
        num_imgs = bytelist_to_uint(bytelist[ 4: 8])
        full_list = 1
        if 0 < imgs_to_read < num_imgs:
            num_imgs = imgs_to_read
            full_list = 0
        start_pos = 8
        dim_sizes = [num_imgs]
        for i in range(num_dims - 1):
            dim_sizes.append( bytelist_to_uint(bytelist[8+4*i:12+4*i]) )
            start_pos += 4
            
        print(num_dims)
        print(dim_sizes)

        results, bytes_read = get_one_idx_entry(bytelist, start_pos, num_dims, dim_sizes, datatype)
        if full_list :
            assert (start_pos + bytes_read == len(bytelist)) # Whole list consumed.

        return results       

def get_one_idx_entry(bytelist, start_pos, num_dims, dim_sizes, datatype):
        assert(datatype == 8) # Only support unsigned bytes right now.
        datasize = 1
        if num_dims == 0:
            v = bytelist_to_uint(bytelist[start_pos:start_pos+datasize])
            #print (start_pos, v)
            return v, datasize
        else :
            results = []
            sp = start_pos
            for i in range(dim_sizes[0]):
                r, sp_inc = get_one_idx_entry(bytelist, sp, num_dims-1, dim_sizes[1:], datatype)
                results.append(r)
                sp += sp_inc
            return results, sp - start_pos
                

def image_to_str(img):
    """ Assumes img is a 2 array with values in range 0 - 255 """
    s = ""
    for y in range(len(img)):
        row = img[y]
        for x in range(len(row)):
            p = row[x]
            s += val_to_char(p)
        s += "\n"

    return s

def val_to_char(p):
    c = '.'
    if p > 128:
        c = '#'
    return c


num_imgs = 10000
image_list = read_idx_file(imagefile, num_imgs)
label_list = read_idx_file(labelfile, num_imgs)

if 0 :
    for i in range(10):
        idx = random.randrange(num_imgs)
        i = image_list[idx]
        l = label_list[idx]
        print (idx)
        print (l)
        print (image_to_str(i))


import difflib
import pprint
def compare_images (img1, img2):
    """ This function seems to be useless"""
    s1 = image_to_str(img1)
    s2 = image_to_str(img2)
    dsm = difflib.SequenceMatcher(None, s1, s2)
    score = dsm.ratio()
    # print(s1)
    # print(s2)
    # dd = difflib.Differ()
    # difflines = list(dd.compare(s1.splitlines(1), s2.splitlines(1)))
    # pprint.pprint(difflines)
    
    return score

# Diff two 3's.
# score = compare_images(image_list[6107], image_list[5573])
# print(score)
# Result is 0.19. Pah!
    




# Possible way to approach this problem :
# Writer :
    # Create a parameterized generator for each writing convention for each digit.
    # It will have ~ 10 parameters.
    # After that one can perturb the edges to account for variations in thickness.
    # Of course, if the generator can generate the image one is trying to recognize, then we have a match.
    # But it seems hard to solve this multi-variable vector equation.
    # So, we'll just use this for testing and checking.
# Reader :
    # for each candidate character :
        # for each writing style :
            # Try to get a close initial condition :
            # Set up rules to extract a good starting set of values for the writer parameters for each digit.
            # Use starting set as seed and randomize (or search?) about that point to get a good match.
            # Then perturb thickness to get a really good match.
            # Finally yield a match score.
    # Pick and return best or top few.    
