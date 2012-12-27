
training  = 0
imagefile = "train-images-idx3-ubyte" if training else "t10k-images-idx3-ubyte"
labelfile = "train-labels-idx1-ubyte" if training else "t10k-labels-idx1-ubyte"

def bytelist_to_uint(bytelist):
    val = 0
    for b in bytelist :
        val = val * 256 + b
    return val

def read_idx_file(filename):
    with open(filename, 'rb') as f:
        bytelist = f.read()
        assert(bytelist[0:2] == bytes([0,0])) # Magic value.
        datatype = bytelist[2]
        num_dims = bytelist[3]
        num_imgs = bytelist_to_uint(bytelist[ 4: 8])
        start_pos = 8
        dim_sizes = [num_imgs]
        for i in range(num_dims - 1):
            dim_sizes.append( bytelist_to_uint(bytelist[8+4*i:12+4*i]) )
            start_pos += 4
            
        print(num_dims)
        print(dim_sizes)

        results, bytes_read = get_one_idx_entry(bytelist, start_pos, num_dims, dim_sizes, datatype)
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
    c = ' '
    if p > 128:
        c = '#'
    return c


image_list = read_idx_file(imagefile)
label_list = read_idx_file(labelfile)
idx = 402
i = image_list[idx]
l = label_list[idx]

print (l)
print (image_to_str(i))
