
training  = 0
imgfile   = "train-images-idx3-ubyte" if training else "t10k-images-idx3-ubyte"
labelfile = "train-labels-idx1-ubyte" if training else "t10k-labels-idx1-ubyte"

def bytelist_to_int(bytelist):
    val = 0
    for b in bytelist :
        val = val * 256 + b
    return val

def read_img_file(filename):
    with open(filename, 'rb') as f:
        bytelist = f.read()
        assert(bytelist[0:4] == bytes([0,0,8,3])) # Magic value.
        num_imgs = bytelist_to_int(bytelist[ 4: 8])
        num_rows = bytelist_to_int(bytelist[ 8:12]) # Is this row or col ?
        num_cols = bytelist_to_int(bytelist[12:16])
        print(num_imgs)        
        print(num_rows)        
        print(num_cols)        

def read_label_file(filename):
    with open(filename, 'rb') as f:
        bytelist = f.read()
        assert(bytelist[0:4] == bytes([0,0,8,1])) # Magic value.
        num_imgs = bytelist_to_int(bytelist[ 4: 8])
        print(num_imgs)        


read_img_file(imgfile)
    
