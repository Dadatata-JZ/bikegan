import os.path
import random
import torchvision.transforms as transforms
import torch
from data.base_dataset import BaseDataset
from data.image_folder import make_dataset
from PIL import Image
import numpy as np
import skimage.transform as transform

class BlurDataset(BaseDataset):
    def initialize(self, opt):
        self.opt = opt
        self.root = opt.dataroot
        self.center_crop = opt.center_crop
        self.dir_AB = os.path.join(opt.dataroot, opt.phase)
        self.AB_paths = sorted(make_dataset(self.dir_AB))
        assert(opt.resize_or_crop == 'resize_and_crop')

    def __getitem__(self, index):
        AB_path = self.AB_paths[index]
        A = Image.open(AB_path).convert('RGB')

        A = A.resize( (self.opt.loadSize, self.opt.loadSize), Image.BICUBIC)

        small = random.randint(16, 64)

        B = A.resize((small, small), Image.BICUBIC)
        B += np.random.normal(0, random.randint(3, 10), (small, small, 3))
        B = transform.resize(B, A.size)

        w = A.size[1]
        h = A.size[0]

        A = transforms.ToTensor()(A)
        B = transforms.ToTensor()(B).float()
        B= B.clamp(0,1)

        if self.center_crop:
            w_offset = int(round((w - self.opt.fineSize) / 2.0))
            h_offset = int(round((h - self.opt.fineSize) / 2.0))
        else:
            w_offset = random.randint(0, max(0, w - self.opt.fineSize - 1))
            h_offset = random.randint(0, max(0, h - self.opt.fineSize - 1))

        A = A[:, h_offset:h_offset + self.opt.fineSize,
                   w_offset:w_offset + self.opt.fineSize]
        B = B[:, h_offset:h_offset + self.opt.fineSize,
                   w_offset:w_offset + self.opt.fineSize]

        # tiletype = random.random()
        # tileoverlap = 26
        # moverlap = self.opt.fineSize - tileoverlap
        # 
        # if tiletype < 0.66: # blur bottom overlap
        #     B = torch.cat( ( B[:,0:moverlap,:],A[:,moverlap:self.opt.fineSize,:] ), dim = 1 )
        #     if tiletype < 0.33: # blur right overlap
        #         B = torch.cat( ( B[:,:,0:moverlap],A[:,:,moverlap:self.opt.fineSize] ), dim = 2 )

        if random.random() < 0.2:
            top = random.randint(1,64)
            B[:,0:top,:] = 0
            A[:,0:top,:] = 0

        if random.random() < 0.2:
            left = random.randint(1,64)
            B[:,:,0:left] = 0
            A[:,:,0:left] = 0

        A = transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))(A)
        B = transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))(B)

        if self.opt.which_direction == 'BtoA':
            input_nc = self.opt.output_nc
            output_nc = self.opt.input_nc
        else:
            input_nc = self.opt.input_nc
            output_nc = self.opt.output_nc

        if (not self.opt.no_flip) and random.random() < 0.5:
            idx = [i for i in range(A.size(2) - 1, -1, -1)]
            idx = torch.LongTensor(idx)
            A = A.index_select(2, idx)
            B = B.index_select(2, idx)

        if input_nc == 1:
            tmp = A[0, ...] * 0.299 + A[1, ...] * 0.587 + A[2, ...] * 0.114
            A = tmp.unsqueeze(0)

        if output_nc == 1:
            tmp = B[0, ...] * 0.299 + B[1, ...] * 0.587 + B[2, ...] * 0.114
            B = tmp.unsqueeze(0)

        return {'A': A, 'B': B,
                'A_paths': AB_path, 'B_paths': AB_path}

    def __len__(self):
        if self.opt.phase == 'val':
            return len(self.AB_paths )
        else:
            return len(self.AB_paths ) // 2 * 2

    def name(self):
        return 'AlignedDataset'
