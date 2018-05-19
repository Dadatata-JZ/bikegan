import os.path
import random
import torchvision.transforms as transforms
import torch
from data.base_dataset import BaseDataset
from data.image_folder import make_dataset
from PIL import Image

class TripleDataset(BaseDataset):
    def initialize(self, opt):
        self.opt = opt
        self.root = opt.dataroot
        self.center_crop = opt.center_crop
        self.dir_AB = os.path.join(opt.dataroot, opt.phase)
        self.AB_paths = sorted(make_dataset(self.dir_AB))
        assert(opt.resize_or_crop == 'resize_and_crop')

        self.root_additional = self.opt.dataroot_additional

    def __getitem__(self, index):
        AB_path = self.AB_paths[index]
        AB = Image.open(AB_path).convert('RGB')
        AB = AB.resize(
            (self.opt.loadSize * 2, self.opt.loadSize), Image.BICUBIC)

        AB = transforms.ToTensor()(AB)

        C_path = os.path.join(self.root_additional, os.path.relpath(self.AB_paths[index], self.root))
        C = Image.open(C_path).convert('RGB')
        C = C.resize(
            (self.opt.loadSize, self.opt.loadSize), Image.BICUBIC)
        C = transforms.ToTensor()(C)

        w_total = AB.size(2)
        w = int(w_total / 2)
        h = AB.size(1)
        if self.center_crop:
            w_offset = int(round((w - self.opt.fineSize) / 2.0))
            h_offset = int(round((h - self.opt.fineSize) / 2.0))
        else:
            w_offset = random.randint(0, max(0, w - self.opt.fineSize - 1))
            h_offset = random.randint(0, max(0, h - self.opt.fineSize - 1))

        A = AB[:, h_offset:h_offset + self.opt.fineSize,
               w_offset:w_offset + self.opt.fineSize]
        B = AB[:, h_offset:h_offset + self.opt.fineSize,
               w + w_offset:w + w_offset + self.opt.fineSize]

        A = transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))(A)
        B = transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))(B)

        if C.size(2) != w or C.size(1) != h:
            raise ValueError('the additional input does not have the right size.')
        C = C[:, h_offset:h_offset + self.opt.fineSize, w_offset:w_offset + self.opt.fineSize]
        C = transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))(C)

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
            C = C.index_select(2, idx)

        if input_nc == 1:
            tmp = A[0, ...] * 0.299 + A[1, ...] * 0.587 + A[2, ...] * 0.114
            A = tmp.unsqueeze(0)

        if output_nc == 1:
            tmp = B[0, ...] * 0.299 + B[1, ...] * 0.587 + B[2, ...] * 0.114
            B = tmp.unsqueeze(0)

        return {'A': A, 'B': B, 'C': C,
                'A_paths': AB_path, 'B_paths': AB_path, 'C_paths': C_path}

    def __len__(self):
        if self.opt.phase == 'val':
            return len(self.AB_paths )
        else:
            return len(self.AB_paths ) // 2 * 2

    def name(self):
        return 'TripleDataset'