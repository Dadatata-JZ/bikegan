CLASS='dows2'  # facades, day2night, edges2shoes, edges2handbags, maps
MODEL='bicycle_gan'
GPU_ID=0
DISPLAY_ID=$((GPU_ID*10+1))
PORT=8097
NZ=8


CHECKPOINTS_DIR=./checkpoints_pub/${CLASS}/
DATE=`date '+%d_%m_%Y_%H'`
NAME=${CLASS} #_${MODEL}_${DATE}


# dataset
NO_FLIP=''
DIRECTION='AtoB'
LOAD_SIZE=286
FINE_SIZE=256
INPUT_NC=3

NITER=100
NITER_DECAY=100
SAVE_EPOCH=25

# command
CUDA_VISIBLE_DEVICES=${GPU_ID} python ./train.py \
  --display_id ${DISPLAY_ID} \
  --dataroot /data \
  --name ${NAME} \
  --model ${MODEL} \
  --display_port ${PORT} \
  --which_direction ${DIRECTION} \
  --checkpoints_dir ${CHECKPOINTS_DIR} \
  --loadSize ${LOAD_SIZE} \
  --fineSize ${FINE_SIZE} \
  --nz ${NZ} \
  --input_nc ${INPUT_NC} \
  --niter ${NITER} \
  --niter_decay ${NITER_DECAY} \
  --use_dropout \
  --blur_a 12
