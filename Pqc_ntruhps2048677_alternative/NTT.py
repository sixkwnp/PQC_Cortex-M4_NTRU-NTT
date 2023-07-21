import random;

Q = 2048; Q_mask = 0x03FF;
N = 677;
size = 1536;

# If newQ = 1536 * k + 1, than it always has 1536-th primitive root;
newq = 0;
newy = 0;
newz = 0;
zetas = [0] * 512;
invzetas = [0] * 512;
brv = [0, 256, 128, 384, 64, 320, 192, 448, 32, 288, 160, 416, 96, 352, 224, 480, 16, 272, 144, 400, 80, 336, 208, 464, 48, 304, 176, 432, 112, 
         368, 240, 496, 8, 264, 136, 392, 72, 328, 200, 456, 40, 296, 168, 424, 104, 360, 232, 488, 24, 280, 152, 408, 88, 344, 216, 472, 56, 312, 
         184, 440, 120, 376, 248, 504, 4, 260, 132, 388, 68, 324, 196, 452, 36, 292, 164, 420, 100, 356, 228, 484, 20, 276, 148, 404, 84, 340, 
         212, 468, 52, 308, 180, 436, 116, 372, 244, 500, 12, 268, 140, 396, 76, 332, 204, 460, 44, 300, 172, 428, 108, 364, 236, 492, 28, 284, 
         156, 412, 92, 348, 220, 476, 60, 316, 188, 444, 124, 380, 252, 508, 2, 258, 130, 386, 66, 322, 194, 450, 34, 290, 162, 418, 98, 354, 226, 
         482, 18, 274, 146, 402, 82, 338, 210, 466, 50, 306, 178, 434, 114, 370, 242, 498, 10, 266, 138, 394, 74, 330, 202, 458, 42, 298, 170, 
         426, 106, 362, 234, 490, 26, 282, 154, 410, 90, 346, 218, 474, 58, 314, 186, 442, 122, 378, 250, 506, 6, 262, 134, 390, 70, 326, 198, 
         454, 38, 294, 166, 422, 102, 358, 230, 486, 22, 278, 150, 406, 86, 342, 214, 470, 54, 310, 182, 438, 118, 374, 246, 502, 14, 270, 142, 
         398, 78, 334, 206, 462, 46, 302, 174, 430, 110, 366, 238, 494, 30, 286, 158, 414, 94, 350, 222, 478, 62, 318, 190, 446, 126, 382, 254, 
         510, 1, 257, 129, 385, 65, 321, 193, 449, 33, 289, 161, 417, 97, 353, 225, 481, 17, 273, 145, 401, 81, 337, 209, 465, 49, 305, 177, 433, 
         113, 369, 241, 497, 9, 265, 137, 393, 73, 329, 201, 457, 41, 297, 169, 425, 105, 361, 233, 489, 25, 281, 153, 409, 89, 345, 217, 473, 57, 
         313, 185, 441, 121, 377, 249, 505, 5, 261, 133, 389, 69, 325, 197, 453, 37, 293, 165, 421, 101, 357, 229, 485, 21, 277, 149, 405, 85, 
         341, 213, 469, 53, 309, 181, 437, 117, 373, 245, 501, 13, 269, 141, 397, 77, 333, 205, 461, 45, 301, 173, 429, 109, 365, 237, 493, 29, 
         285, 157, 413, 93, 349, 221, 477, 61, 317, 189, 445, 125, 381, 253, 509, 3, 259, 131, 387, 67, 323, 195, 451, 35, 291, 163, 419, 99, 355, 
         227, 483, 19, 275, 147, 403, 83, 339, 211, 467, 51, 307, 179, 435, 115, 371, 243, 499, 11, 267, 139, 395, 75, 331, 203, 459, 43, 299, 
         171, 427, 107, 363, 235, 491, 27, 283, 155, 411, 91, 347, 219, 475, 59, 315, 187, 443, 123, 379, 251, 507, 7, 263, 135, 391, 71, 327, 
         199, 455, 39, 295, 167, 423, 103, 359, 231, 487, 23, 279, 151, 407, 87, 343, 215, 471, 55, 311, 183, 439, 119, 375, 247, 503, 15, 271, 
         143, 399, 79, 335, 207, 463, 47, 303, 175, 431, 111, 367, 239, 495, 31, 287, 159, 415, 95, 351, 223, 479, 63, 319, 191, 447, 127, 383, 
         255, 511];

a = [random.randrange(0, Q, 1) for p in range(0, N)];
b = [random.randrange(0, Q, 1) for p in range(0, N)];

def schoolbook_multiplication(poly1, poly2):

    result = [0] * N;
    for i in range (0, N):
        for j in range(0, N):
            idx = 0;
            idx = i + j;
            if(idx >= N):
                idx = idx - N;
            result[idx] += poly1[i] * poly2[j];
            if(result[idx] >= Q):
                result[idx] = result[idx] % Q;
    #print("a      = ",poly1);
    #print("b      = ",poly2);
    #print("result = ",result);

    return result

def good_thomas_permutation(poly1, poly2):

    pad_poly1 = poly1 + [0] * (size-N);
    pad_poly2 = poly2 + [0] * (size-N);
    #(len(pad_a));
    reorder_poly1 = [[0] * 512] * 3;
    reorder_poly2 = [[0] * 512] * 3;
    for i in range(0, 3):
        for j in range(0, 512):
            reorder_poly1[i][j] = pad_poly1[(i*512 + j*3)%1536];
            reorder_poly2[i][j] = pad_poly2[(i*512 + j*3)%1536];

    return reorder_poly1, reorder_poly2;

def inv_good_thomas_permutation(poly):

    reorder_poly = [0] * 1536;
    for i in range(0, 3):
        for j in range(0, 512):
            idx = (1024 * i + 513 * j) % 1536;
            reorder_poly[idx] = poly[i][j];

    return reorder_poly;

def ntt_512(poly):

    win_len = 256; brv_idx = 1;
    while(win_len >= 1):
        start = 0;
        while(start < 512):
            zeta = zetas[brv[brv_idx]];
            brv_idx += 1;
            i = start;
            while(i < start + win_len):
                b               = (zeta * poly[i+win_len]) % newq;
                poly[i+win_len] = poly[i] - b;
                poly[i]         = poly[i] + b;
                i += 1;
            start = win_len + i;
        win_len = win_len / 2;

    return poly;

def intt_512(poly):

    win_len = 1; brv_idx = 512;
    while(win_len <= 256):
        start = 0;
        while(start < 512):
            zeta = invzetas[brv[brv_idx]];
            brv_idx -= 1;
            i = start;
            while(i < start + win_len):
                a               = (poly[i] + poly[i+win_len]) / 2;
                b               = (poly[i] - poly[i+win_len]) / 2;
                poly[i]         = a;
                poly[i+win_len] = (b * zeta) % newq;
                i += 1;
            start = win_len + i;
        win_len = win_len * 2;

    return poly;

def conv(poly1,poly2):

    result = [0] * 512;
    for i in range(0,3):
        for j in range(0,3):
            idx = i + j;
            if(idx >= 3):
                idx = idx - 3;
            result[idx] = poly1[i] * poly2[j];
            if(result[idx] >= newq):
                result[idx] %= newq;

    return result;

def final_state(poly):

    for i in range(N, size):
        idx = i - N;
        for j in range(0, 2):
            if(idx >= 2 * N):
                idx -= 677;
            else:
                break;
        poly[idx] += poly[i];
    for i in range(0, N):
        poly[i] = poly[i] & Q_mask;

    return poly[0:677];

schoolbook_result = [0] * N;
schoolbook_result = schoolbook_multiplication(a, b);

reorder_poly1 = [[0] * 512] * 3; ntt_poly1 = [[0] * 512] * 3;
reorder_poly2 = [[0] * 512] * 3; ntt_poly2 = [[0] * 512] * 3;
ntt_conv      = [[0] * 512] * 3; ntt_1536_result = [0] * 1536;
ntt_result    = [0] * 677;
(reorder_poly1, reorder_poly2) = good_thomas_permutation(a, b);

for i in range(0, 3):
    ntt_poly1[i][:] = ntt_512(reorder_poly1[i][:]);
    ntt_poly2[i][:] = ntt_512(reorder_poly2[i][:]);

for i in range(0, 512):
    ntt_conv[:][i] = conv(reorder_poly1[:][i], reorder_poly2[:][i]);

ntt_1536_result = inv_good_thomas_permutation(ntt_conv);
ntt_result = final_state(ntt_1536_result);


print("finish");